# Dashboard — Technische Umsetzung und Inhalt

> **Ziel des Dashboards:** Die Ergebnisse der Datenanalyse interaktiv erkunden — Zusammenhänge filtern, Häuser vergleichen und das Machine-Learning-Modell direkt ausprobieren.

**Technologie:** Streamlit (`Dashboard/streamlit_dashboard.py`) + Plotly für alle Grafiken
**Datengrundlage:** `Data/analysetabelle.csv` (1.821 Krankenhäuser, Qualitätsberichte 2023, IQTIG)
**Modell:** `Data/modell_krankenhaus.pkl` (Decision Tree, `max_depth=3`)
**Deployment:** Streamlit Cloud

Dieses Dokument hat zwei Kapitel: Kapitel 1 erklärt, **wie** das Dashboard technisch gebaut ist (Code, Funktionen, Architekturentscheidungen). Kapitel 2 beschreibt, **was** jede Seite zeigt und wie sie zu lesen ist.

---

# Kapitel 1 — Technische Umsetzung

## 1.1 Architektur: drei Dateien, klare Trennung

Das Dashboard verteilt sich bewusst auf drei Dateien mit unterschiedlicher Verantwortung:

| Datei | Verantwortung |
|---|---|
| `Dashboard/streamlit_dashboard.py` | UI-Layout, Widgets, Seitenaufbau — was der Nutzer sieht und anklickt |
| `Dashboard/dashboard_utils.py` | Datenlogik, Berechnungen, Plot-Erstellung — reine Funktionen ohne Streamlit-Widgets |
| `model/modell_klasse.py` | Die `KrankenhausModell`-Klasse — identisch genutzt beim Training (`03_Decision_Tree.ipynb`) und beim Laden im Dashboard |

Der Grund für diese Trennung: `dashboard_utils.py` lässt sich unabhängig vom Dashboard testen und wiederverwenden (siehe Abschnitt 1.9), und `streamlit_dashboard.py` bleibt übersichtlich, weil es nur noch Layout-Code enthält, keine Berechnungslogik. Der Import am Kopf von `streamlit_dashboard.py` macht diese Trennung sichtbar:

```python
from dashboard_utils import (
    lade_daten, validiere_daten, berechne_kpis,
    erstelle_karte, erstelle_quote_histogramm, erstelle_bundesland_balken,
    erstelle_traeger_vergleich, erstelle_boxplot_aerzte,
    erstelle_streudiagramm, erstelle_pivot_traeger_uni,
    finde_aehnliche, haus_steckbrief,
    lade_modell, berechne_risiko,
    get_traeger_optionen, get_bundesland_optionen,
    FARBE_VIELE, FARBE_WENIGE, MEDIAN_QUOTE, DT_SPLIT, TRAEGER_COL,
)
```

Jede Funktion, die im Dashboard sichtbar wird, ist einzeln benannt importiert (kein `import *`) — das macht in der Datei selbst auf einen Blick sichtbar, welche Bausteine aus `dashboard_utils.py` tatsächlich verwendet werden.

## 1.2 Daten laden und cachen

Ohne Caching würde Streamlit `analysetabelle.csv` bei **jeder** Nutzerinteraktion (jeder Klick, jeder Dropdown-Wechsel) neu von der Festplatte laden — Streamlit führt das komplette Skript bei jeder Interaktion erneut aus. Die Dekoratoren `@st.cache_data` und `@st.cache_resource` verhindern das:

```python
@st.cache_data
def get_daten():
    return lade_daten()

@st.cache_resource
def get_modell():
    return lade_modell()

df     = get_daten()
modell = get_modell()
```

`@st.cache_data` ist für Daten gedacht, die man vergleichen/kopieren kann (hier: der DataFrame) — Streamlit merkt sich das Ergebnis anhand der Funktionsargumente. `@st.cache_resource` ist für Objekte, die nicht sinnvoll kopiert werden sollten (hier: das geladene ML-Modell) — es wird einmal geladen und danach für alle Nutzer:innen wiederverwendet.

Die eigentliche Ladefunktion `lade_daten()` in `dashboard_utils.py` macht mehr als nur `pd.read_csv()`:

```python
def lade_daten(pfad: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(pfad, low_memory=False)

    # Koordinaten reparieren — bedingungslos, da dtype-Check auf manchen Servern fehlschlägt
    for col in ["SO.Latitude", "SO.Longitude"]:
        df[col] = (
            df[col].astype(str)
            .str.replace(",", ".", regex=False)
            .pipe(pd.to_numeric, errors="coerce")
        )

    # Hilfsspalten fuer Dashboard-Anzeige
    df["Problemkategorie"] = df["hat_viele_Probleme"].map(LABEL_MAP)
    df["Uni_Label"]        = df["SO.Uni"].map({0: "Normale Klinik", 1: "Uni-Klinik"})
    df["Groessenklasse"]   = df["SO.Betten"].apply(_groesse_kategorie)
    df["Aerzte_Kategorie"] = df["aerzte_pro_bett"].apply(_aerzte_risikoklasse)

    df[TRAEGER_COL] = df[TRAEGER_COL].fillna("Unbekannt")
    return df
```

Zwei Details sind hier bewusst so gewählt:

- **Koordinaten-Konvertierung bedingungslos statt mit `dtype`-Prüfung.** Ein ursprünglicher Ansatz prüfte erst `if df[col].dtype == object`, bevor Komma durch Punkt ersetzt wird. Das schlug auf Streamlit Cloud (Linux) fehl, weil pandas die Spalte dort anders typisiert einliest als lokal unter Windows. Die bedingungslose Variante (immer erst zu String, dann zu Punkt-Dezimal, dann zu Zahl konvertieren) funktioniert auf beiden Plattformen identisch.
- **Hilfsspalten statt Neuberechnung in der UI.** `Problemkategorie`, `Uni_Label`, `Groessenklasse` und `Aerzte_Kategorie` werden einmal beim Laden berechnet, nicht jedes Mal neu in `streamlit_dashboard.py` — Anzeige-Code und Datenlogik bleiben so getrennt.

## 1.3 Navigation ohne Sidebar

Die vier Seiten liegen als String-Liste vor, der aktuelle Seitenstand wird über die URL gehalten:

```python
SEITEN = ["Gesamtüberblick", "Einflussfaktoren", "Häuser vergleichen", "Qualitäts-Vorhersage"]

_seite_aus_url = st.query_params.get("seite", SEITEN[0])
seite = _seite_aus_url if _seite_aus_url in SEITEN else SEITEN[0]

def _gehe_zu_seite(s):
    st.query_params["seite"] = s
```

`st.query_params` bildet den URL-Parameter `?seite=...` ab — dadurch bleibt beim Browser-Reload dieselbe Seite aktiv, statt auf die Startseite zurückzuspringen. Die Navigation selbst besteht aus echten Streamlit-Buttons, nicht aus HTML-Links:

```python
_nav_cols = st.columns(len(SEITEN))
for _i, _s in enumerate(SEITEN):
    with _nav_cols[_i]:
        st.button(
            _s, key=f"nav_{_s}", on_click=_gehe_zu_seite, args=(_s,),
            type="primary" if _s == seite else "secondary",
            width="stretch",
        )
```

**Warum keine `<a href="?seite=...">`-Links?** Ein erster Ansatz nutzte genau solche HTML-Links über `st.markdown(..., unsafe_allow_html=True)`. Problem: Streamlits Markdown-Renderer injiziert bei jedem `<a href>`-Tag automatisch `target="_blank"` — jeder Klick öffnete einen neuen Browser-Tab, unabhängig davon, welche HTML-Attribute im Quellcode standen. Das ist eine Plattform-Eigenheit von Streamlit, nicht per HTML-Attribut abschaltbar. Die Lösung: `st.button()` mit `on_click`-Callback, der `st.query_params` setzt — technisch kein `<a href>` mehr im Spiel, dadurch öffnet sich nie ein neuer Tab.

## 1.4 Seitenaufbau: eine if/elif-Kette

Der komplette Seiteninhalt hängt an einer einzigen Verzweigung:

```python
if seite == "Gesamtüberblick":
    ...
elif seite == "Einflussfaktoren":
    ...
elif seite == "Häuser vergleichen":
    ...
elif seite == "Qualitäts-Vorhersage":
    ...
```

Streamlit hat kein eingebautes Multi-Page-Routing im klassischen Sinn (keine separaten URLs pro Seite) — stattdessen läuft bei jeder Interaktion das komplette Skript von oben nach unten neu durch, und nur der zur aktuellen `seite`-Variable passende Block wird tatsächlich Widgets/Inhalte erzeugen. Header-Banner und Navigation liegen **vor** dieser Verzweigung, weil sie auf jeder Seite gleich aussehen sollen.

## 1.5 Wiederverwendbare Plot-Funktionen

Jede Grafik hat eine eigene Funktion in `dashboard_utils.py`, die einen fertigen Plotly-`Figure` zurückgibt. Beispiel — das Histogramm der Auffälligkeitsquote:

```python
def erstelle_quote_histogramm(df: pd.DataFrame) -> go.Figure:
    data_all   = df["auffaellig_quote"].dropna().values
    data_wenig = df[df["hat_viele_Probleme"] == 0]["auffaellig_quote"].dropna().values
    data_viel  = df[df["hat_viele_Probleme"] == 1]["auffaellig_quote"].dropna().values

    counts_all,   bin_edges = np.histogram(data_all,   bins=30)
    counts_wenig, _         = np.histogram(data_wenig, bins=bin_edges)
    counts_viel,  _         = np.histogram(data_viel,  bins=bin_edges)
    ...
```

Der Trick hier: `bin_edges` wird **einmal** aus allen Daten berechnet und dann für die beiden Gruppen-Histogramme (`data_wenig`, `data_viel`) **wiederverwendet** (`bins=bin_edges` statt erneut `bins=30`). Ohne diesen Schritt würden die drei Histogramme leicht unterschiedliche Balkengrenzen bekommen, und die überlagerte Linie („Verlauf") würde nicht exakt auf den Balkenspitzen sitzen.

Ein zweites Beispiel — das Bundesland-Balkendiagramm mit sprechendem Hover-Text:

```python
fig = px.bar(
    stats, x="pct", y="SO.Bundesland", orientation="h",
    text=stats["n"].apply(lambda x: f"n={x} Häuser"),
    custom_data=["n"],
    ...
)
fig.update_traces(
    marker_color=farben, textposition="outside",
    hovertemplate="<b>%{y}</b><br>Anteil 'Viele Probleme': %{x:.1%}<br>Anzahl Häuser (n): %{customdata[0]}<extra></extra>",
)
```

`custom_data=["n"]` macht die Fallzahl `n` im `hovertemplate` über `%{customdata[0]}` verfügbar — ohne diesen Schritt könnte die Maus-Over-Anzeige die Häuseranzahl je Bundesland nicht anzeigen, obwohl sie schon als Balkenbeschriftung sichtbar ist. Diese explizite Beschriftung wurde nachträglich ergänzt, weil unklar war, wofür die Zahl an jedem Balken steht.

Alle übrigen Plot-Funktionen (`erstelle_karte`, `erstelle_traeger_vergleich`, `erstelle_boxplot_aerzte`, `erstelle_streudiagramm`, `erstelle_pivot_traeger_uni`) folgen demselben Muster: DataFrame rein, fertige Plotly-Figur (oder `pivot_table`) raus, keine Streamlit-Aufrufe innerhalb der Funktion. Das macht sie einzeln testbar (siehe Abschnitt 1.9) und in der UI-Datei zu einer einzigen `st.plotly_chart(...)`-Zeile verkürzbar.

## 1.6 Das Modell laden und für Live-Vorhersagen nutzen

Das trainierte Modell liegt als `Data/modell_krankenhaus.pkl` vor, gespeichert mit `joblib` in `03_Decision_Tree.ipynb`. Geladen wird es so:

```python
def lade_modell(pfad: Path = MODEL_PATH):
    try:
        return joblib.load(pfad)
    except FileNotFoundError:
        return None
```

Damit `joblib.load()` funktioniert, muss die Klasse `KrankenhausModell` zum Zeitpunkt des Ladens importierbar sein — pickle (worauf `joblib` aufbaut) speichert nicht die Klasse selbst, sondern nur einen Verweis darauf. Deshalb importiert `dashboard_utils.py` ganz oben:

```python
sys.path.insert(0, str(PROJEKT_ROOT / "model"))
from modell_klasse import KrankenhausModell  # noqa: E402, F401 – wird fuer joblib benoetigt
```

Der `# noqa`-Kommentar markiert bewusst, dass dieser Import nie direkt im Code aufgerufen wird (daher würde ein Linter ihn sonst als „ungenutzt" melden) — er muss trotzdem da stehen, damit `joblib.load()` die Klasse findet.

**Ein behobener Bug am Rande:** `modell_klasse.py` enthält einen Kompatibilitäts-Alias:

```python
if "__main__" in sys.modules and not hasattr(sys.modules["__main__"], "KrankenhausModell"):
    sys.modules["__main__"].KrankenhausModell = KrankenhausModell
```

Grund: Das Modell wurde ursprünglich gespeichert, als die Klasse noch **inline im Notebook** definiert war (Modul `__main__`). Pickle sucht die Klasse beim Laden weiterhin unter `__main__` — ohne diesen Alias schlug `joblib.load()` in jedem Kontext fehl, der nicht selbst `__main__` ist, was das Dashboard beim Start crashen ließ.

Die eigentliche Vorhersage übernimmt `berechne_risiko()`:

```python
def berechne_risiko(modell, betten, uni, fortbildung, aerzte, traeger_enc,
                     pflege=1.0, konzern=0) -> dict:
    eingabe = pd.DataFrame([{
        "SO.Betten": betten, "SO.Uni": uni, "fortbildungsquote": fortbildung,
        "aerzte_pro_bett": aerzte, "pflege_pro_bett": pflege,
        "ist_konzern": konzern, "traeger_enc": traeger_enc,
    }])
    vorhersage = modell.model.predict(eingabe)[0]
    proba      = modell.model.predict_proba(eingabe)[0]
    ...
```

Die Nutzereingaben aus dem Formular werden als Ein-Zeilen-DataFrame mit exakt denselben Spaltennamen wie beim Training zusammengesetzt — `predict()` liefert die binäre Klasse, `predict_proba()` zusätzlich die Wahrscheinlichkeit je Klasse, aus der die Unsicherheits-Einstufung (`hoch`/`mittel`/`gering`, je nach `max(proba)`) abgeleitet wird.

## 1.7 Ähnliche Häuser finden und Einzelhaus-Steckbrief

`finde_aehnliche()` baut eine boolesche Maske schrittweise aus mehreren Filterbedingungen zusammen:

```python
mask = pd.Series([True] * len(df), index=df.index)
if betten > 0:
    toleranz = max(betten * toleranz_pct, 30)
    mask &= df["SO.Betten"].between(betten - toleranz, betten + toleranz)
if bundesland != "Alle":
    mask &= df["SO.Bundesland"] == bundesland
if traeger != "Alle":
    mask &= df[TRAEGER_COL] == traeger
```

Jede Filterbedingung wird nur angewendet, wenn sie aktiv ist (Bettenzahl > 0, Bundesland/Träger ≠ „Alle") — die `&=`-Verknüpfung kombiniert beliebig viele optionale Filter zu einer einzigen Maske. `toleranz = max(betten * toleranz_pct, 30)` sorgt zusätzlich dafür, dass die Toleranz nie kleiner als 30 Betten wird, selbst wenn die Prozent-Toleranz bei einem kleinen Haus rechnerisch weniger ergäbe.

`haus_steckbrief()` liefert alle Kennzahlen eines einzelnen Hauses als `dict`, inklusive dem vorab berechneten Abstand zum Median (`delta_median`), der in der UI direkt für die grün/rot-Einfärbung genutzt wird — die Farblogik selbst steht in `streamlit_dashboard.py`, nicht in dieser Funktion.

## 1.8 Warum HTML statt eingebauter Streamlit-Elemente?

An zwei Stellen wird bewusst rohes HTML über `st.markdown(..., unsafe_allow_html=True)` statt eingebauter Streamlit-Widgets verwendet:

| Stelle | Eingebaute Alternative | Warum verworfen |
|---|---|---|
| KPI-Tabelle (Seite 1) und Einzelhaus-Steckbrief (Seite 3) | `st.metric()` | `st.metric()` erzwingt einen Pfeil (▲/▼) plus Vorzeichen bei jedem Delta-Wert — für „X % über/unter Median" ohne Pfeil und mit frei wählbarer Formulierung gibt es keine eingebaute Option |
| Kopfbanner + Navigation | Streamlit-Standardtitel + Sidebar | Ein durchgehendes Farbschema (blauer Banner) über Titel und Navigation hinweg lässt sich mit reinen Streamlit-Elementen nicht einheitlich stylen |

Der Preis dieser Entscheidung: HTML-Strings sind fehleranfälliger zu pflegen als native Widgets und werden nicht automatisch responsiv wie `st.metric()`. Der Nutzen überwiegt hier, weil die visuelle Konsistenz (kein ungewolltes Pfeil-Symbol, einheitliches Farbschema) für ein Abschlussprodukt wichtiger ist als die Pflegeleichtigkeit.

## 1.9 Eigenständig testbar

`dashboard_utils.py` endet mit einem `if __name__ == "__main__":`-Block, der die wichtigsten Funktionen ohne laufendes Dashboard durchtestet:

```python
if __name__ == "__main__":
    df = lade_daten()
    kpis = berechne_kpis(df)
    aehnliche = finde_aehnliche(df, betten=300, bundesland="Bayern", traeger="Alle", n=5)
    modell = lade_modell()
    if modell:
        risiko = berechne_risiko(modell, betten=200, uni=0, fortbildung=0.7,
                                  aerzte=0.25, traeger_enc=1, pflege=1.0, konzern=0)
```

Aufruf direkt per `python Dashboard/dashboard_utils.py` — das prüft Datenladen, KPI-Berechnung, Ähnliche-Häuser-Suche und Modellvorhersage in wenigen Sekunden, ohne den Streamlit-Server zu starten. Genau diese Trennung (Logik testbar ohne UI) ist der praktische Nutzen der Drei-Dateien-Architektur aus Abschnitt 1.1.

---

# Kapitel 2 — Was zeigt das Dashboard?

## Navigation

Die Navigation liegt **im blauen Header-Banner**, darunter als vier Buttons nebeneinander. Der aktive Button ist farblich hervorgehoben (`type="primary"`). Ein Klick lädt die neue Seite; die URL (`?seite=...`) speichert den Seitenstand, sodass ein Browser-Reload auf derselben Seite bleibt.

---

## Seite 1 — Gesamtüberblick

### Filter (oben auf der Seite)

Drei Dropdowns in einer Zeile direkt auf der Seite — nicht in der Sidebar:
- **Bundesland** — alle 16 + „Alle"
- **Trägerschaft** — freigemeinnützig / öffentlich / privat + „Alle"
- **Klinik-Typ** — Alle / Normale Klinik / Uni-Klinik

Daneben ein **„↺ Zurücksetzen"-Button** (gleiche Höhe, `vertical_alignment="bottom"`).

### KPI-Tabelle

KPI = Key Performance Indicator — die wichtigsten Kennzahlen auf einen Blick. HTML-Tabelle mit dunklem Header und einer Datenzeile:

| Spalte | Besonderheit |
|---|---|
| Krankenhäuser gesamt | — |
| Anteil mit vielen Qualitätsproblemen | Abstandswert zum 50 %-Median, grün/rot ohne Pfeil |
| Ø auffällig-Quote pro Haus | Mittelwert der `auffaellig_quote` je Haus — jedes Haus zählt gleich viel (8,6 % über alle 1.821 Häuser) |
| Gesamtquote | Summe `auffaellig_n` ÷ Summe `total_qi` über alle Häuser — jeder Indikator zählt gleich viel (7,7 %) |
| Ø Ärzte pro Bett | Untertitel: „Vollzeitstellen / Bettenzahl" |

**Ø auffällig-Quote vs. Gesamtquote — warum zwei unterschiedliche Zahlen?** Beide messen denselben Sachverhalt (Anteil auffälliger Indikatoren), aber mit unterschiedlicher Gewichtung. Die **Ø auffällig-Quote** mittelt zuerst pro Haus, dann über die Häuser — ein Haus mit nur 2 bewerteten Indikatoren zählt genauso viel wie ein Haus mit 80. Die **Gesamtquote** summiert zuerst alle auffälligen und alle bewerteten Indikatoren über den gesamten Datensatz und teilt erst danach — hier zählt jeder einzelne Indikator gleich viel, unabhängig davon, zu welchem Haus er gehört. Da kleine Häuser mit wenigen Indikatoren im Schnitt eine volatilere (und tendenziell höhere) Quote haben, liegt die Ø auffällig-Quote (8,6 %) etwas über der Gesamtquote (7,7 %).

### Deutschland-Karte

- Plotly `scatter_mapbox`, Stil `open-street-map` (kein Token nötig)
- Farbe = wenige (grün) / viele Probleme (rot), Punktgröße = Bettenzahl (Min. 30)
- Koordinaten-Konvertierung: bedingungslos (kein dtype-Check, da dieser auf Linux-Servern fehlschlägt)

### Histogramm + Bundesland-Balkendiagramm

- Histogramm: 30 Balken, gestrichelte Linie bei Median (5,88 %)
- Bundesland-Diagramm: **nur wenn kein Bundesland-Filter aktiv** — sonst Hinweismeldung

---

## Seite 2 — Einflussfaktoren

**Immer ungefilterter Gesamtdatensatz** — Filter von Seite 1 gelten hier nicht.

Vier Tabs:

**Tab 1 — Trägerschaft:** Grouped Bar Chart + ausführlicher Erklärungstext (ANOVA — p=0,969, NICHT signifikant; Störfaktor Hausgröße als Zusatzhinweis)

**Tab 2 — Ärzte pro Bett:** Zwei Boxplots + gestrichelte Linie bei Split 0,271 + Erklärungstext (T-Test, Feature Importance 72,8 %)

**Tab 3 — Streudiagramm:**
- Dropdown mit lesbaren Labels inkl. Beschreibung (z. B. `aerzte_pro_bett (Ärzte je Bett — Personalintensität)`)
- Zwei OLS-Regressionslinien (eine je Gruppe)
- **Kontextsensitiver Erklärungstext** — wechselt automatisch je Merkmal

**Tab 4 — Pivot-Tabelle:** Träger × Uni-Status, Heatmap-Formatierung, Erklärungstext

---

## Seite 3 — Häuser vergleichen

### Ähnliche Häuser suchen

- `select_slider` für Bettenzahl-Toleranz: ±10 % / ±20 % / **±30 % (Standard)** / ±50 %
- Label des Bettenzahl-Inputs zeigt gewählte Toleranz dynamisch an
- Button **„↪ Suchen"**
- Ergebnis: Ø auffällig-Quote als HTML-Karte ohne Pfeil — z. B. „2,1 % unter Median" (grün)

### Einzelhaus-Steckbrief

- 8 HTML-Karten: Betten, Träger, Bundesland, Uni-Status, auffällig-Quote, Kategorie, Ärzte/Bett, Fortbildungsquote
- Abstandswert: z. B. „5 % über Median" (rot) — kein Pfeil, kein Vorzeichen

---

## Seite 4 — Qualitäts-Vorhersage

- Intro-Text + Warnbox (Accuracy 57,0 %, Basislinie 50,4 %, Grenzen des Modells)
- Eingabe-Formular: 7 Merkmale in zwei Spalten
- Button **„Ergebnis anzeigen"** — in der linken Spalte unter „Konzernhaus?"
- Ergebnis-Block: Vorhersage-Kasten (grün/rot), P(Wenige/Viele), Erklärung des Schwellenwerts 0,271
- Feature-Importance-Diagramm mit lesbaren Labels, Titel „Welche Merkmale nutzt das Modell?"

---

## Technische Entscheidungen im Überblick

| Entscheidung | Begründung |
|---|---|
| Navigation per `st.button()` + `st.query_params` (kein `<a href>`) | Streamlit erzwingt bei `<a href>`-Links `target="_blank"` — mit echten Buttons öffnet sich nie ein neuer Browser-Tab; Seite überlebt trotzdem den Browser-Reload |
| Filter nur auf Seite 1 | Andere Seiten zeigen immer den Gesamtdatensatz |
| `scatter_mapbox` mit `open-street-map` | Funktioniert ohne Mapbox-Token auf Streamlit Cloud |
| Koordinaten-Konvertierung bedingungslos | `dtype == object`-Check schlägt auf Linux-Servern fehl |
| Lesbare Labels im Streudiagramm-Dropdown | Technische Spaltennamen durch beschreibende Texte ersetzt |
| HTML-Karten statt `st.metric` für Steckbrief | `st.metric` erzwingt Pfeil + Vorzeichen — nicht entfernbar |
| `vertical_alignment="bottom"` für Reset-Button | Sauberste Lösung für Höhenausrichtung mit Selectboxen |
| Drei-Dateien-Architektur (UI / Logik / Modell) | Datenlogik und Plots eigenständig testbar, ohne Streamlit-Server zu starten |
