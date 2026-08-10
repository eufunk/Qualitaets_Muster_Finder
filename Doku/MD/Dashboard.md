# Dashboard — Was zeigen wir, und wie?

> **Ziel des Dashboards:** Die Ergebnisse der Datenanalyse interaktiv erkunden — Zusammenhänge filtern, Häuser vergleichen und das Machine-Learning-Modell direkt ausprobieren.

**Technologie:** Streamlit (`Dashboard/streamlit_dashboard.py`) + Plotly für alle Grafiken  
**Datengrundlage:** `Data/analysetabelle.csv` (1.824 Krankenhäuser, Qualitätsberichte 2023, IQTIG)  
**Modell:** `Data/modell_krankenhaus.pkl` (Decision Tree, `max_depth=3`)  
**Deployment:** Streamlit Cloud

---

## Navigation

Die Navigation liegt **im blauen Header-Banner**, unten rechts — vier Links nebeneinander. Der aktive Link ist weiß hervorgehoben. Ein Klick lädt die neue Seite; die URL (`?seite=...`) speichert den Seitenstand sodass Browser-Reload auf derselben Seite bleibt.

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
| Ø auffällig-Quote pro Haus | Untertitel: „Anteil auffälliger Indikatoren" |
| Ø Ärzte pro Bett | Untertitel: „Vollzeitstellen / Bettenzahl" |

### Deutschland-Karte

- Plotly `scatter_mapbox`, Stil `open-street-map` (kein Token nötig)
- Farbe = wenige (grün) / viele Probleme (rot), Punktgröße = Bettenzahl (Min. 30)
- Koordinaten-Konvertierung: bedingungslos (kein dtype-Check, da dieser auf Linux-Servern fehlschlägt)

### Histogramm + Bundesland-Balkendiagramm

- Histogramm: 30 Balken, gestrichelte Linie bei Median (76,92 %)
- Bundesland-Diagramm: **nur wenn kein Bundesland-Filter aktiv** — sonst Hinweismeldung

---

## Seite 2 — Einflussfaktoren

**Immer ungefilterter Gesamtdatensatz** — Filter von Seite 1 gelten hier nicht.

Vier Tabs:

**Tab 1 — Trägerschaft:** Grouped Bar Chart + ausführlicher Erklärungstext (ANOVA, p-Wert, Störfaktor Hausgröße)

**Tab 2 — Ärzte pro Bett:** Zwei Boxplots + gestrichelte Linie bei Split 0,271 + Erklärungstext (T-Test, Feature Importance 53,6 %)

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
- Ergebnis: Ø auffällig-Quote als HTML-Karte ohne Pfeil — z. B. „12,1 % unter Median" (grün)

### Einzelhaus-Steckbrief

- 8 HTML-Karten: Betten, Träger, Bundesland, Uni-Status, auffällig-Quote, Kategorie, Ärzte/Bett, Fortbildungsquote
- Abstandswert: z. B. „17,8 % über Median" (rot) — kein Pfeil, kein Vorzeichen

---

## Seite 4 — Qualitäts-Vorhersage

- Intro-Text + Warnbox (Accuracy 63,6 %, Basislinie 50,7 %, Grenzen des Modells)
- Eingabe-Formular: 7 Merkmale in zwei Spalten
- Button **„Ergebnis anzeigen"** — in der linken Spalte unter „Konzernhaus?"
- Ergebnis-Block: Vorhersage-Kasten (grün/rot), P(Wenige/Viele), Erklärung des Schwellenwerts 0,271
- Feature-Importance-Diagramm mit lesbaren Labels, Titel „Welche Merkmale nutzt das Modell?"

---

## Technische Entscheidungen

| Entscheidung | Begründung |
|---|---|
| Navigation per HTML-Links + `st.query_params` | Seite überlebt Browser-Reload; keine Sidebar nötig |
| Filter nur auf Seite 1 | Andere Seiten zeigen immer den Gesamtdatensatz |
| `scatter_mapbox` mit `open-street-map` | Funktioniert ohne Mapbox-Token auf Streamlit Cloud |
| Koordinaten-Konvertierung bedingungslos | `dtype == object`-Check schlägt auf Linux-Servern fehl |
| Lesbare Labels im Streudiagramm-Dropdown | Technische Spaltennamen durch beschreibende Texte ersetzt |
| HTML-Karten statt `st.metric` für Steckbrief | `st.metric` erzwingt Pfeil + Vorzeichen — nicht entfernbar |
| `vertical_alignment="bottom"` für Reset-Button | Sauberste Lösung für Höhenausrichtung mit Selectboxen |
