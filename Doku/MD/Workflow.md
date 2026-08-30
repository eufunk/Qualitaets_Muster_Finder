# 🗂️ Workflow — Qualitäts-Muster-Finder

> Dieses Dokument beschreibt zu jedem Baustein: was gemacht wurde, welche Entscheidungen getroffen wurden und warum.

**Projektfrage:** Welche Krankenhausmerkmale hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme aufweist?

---

## <span style="color:#27ae60">📦 Baustein 1 — Daten vorbereiten</span>

<span style="background:#d4edda;color:#155724;padding:2px 8px;border-radius:4px;font-weight:bold">✅ Abgeschlossen</span> &nbsp; **Datum:** 2026-07-27 &nbsp; **Datei:** `01_Exploration.ipynb`

---

### 1.1 Setup

**Entscheidung:** Kein GitHub — das Projekt wird lokal geteilt (per USB / ZIP). Rohdaten bleiben im `Data/`-Ordner und werden nicht weitergegeben. Alle anderen Dateien (Notebooks, CSVs, Dokumentation) können direkt kopiert werden.

---

### 1.2 Datensatz erkunden

**Werkzeug:** Direkte Dateilese-Operationen (erste 3–5 Zeilen jeder CSV-Datei). CSV-Dateien sind Textdateien — Header + Beispieldaten reichen für die Strukturanalyse. Python wird erst für Berechnungen oder Dateien **>50 MB** benötigt.

**Vorgehen:**
1. Alle **86 CSV-Dateien** im `Data/`-Ordner aufgelistet
2. Von jeder Datei Header und 2–5 Beispielzeilen gelesen
3. Präfix-Logik: `SO.*` = Standort, `QS.*` = Qualitätssicherung, `FA.*` = Fachabteilung
4. Verknüpfung: **`SO.QBID`** taucht in fast allen Tabellen auf → universeller Join-Key

**Relevanz-Kriterium:**

| Kategorie | Kriterium |
|-----------|-----------|
| <span style="color:#27ae60">✅ Relevant</span> | Strukturmerkmal (Betten, Träger, Personal, Region, Uni, Fortbildung) ODER QI-Bewertungen |
| <span style="color:#e67e22">⚠️ Möglicherweise</span> | QS-relevante Infos, aber Bedeutung unklar oder nur für Teilgruppen |
| <span style="color:#e74c3c">❌ Nicht relevant</span> | Lookup-Tabellen, nicht-medizinische Angebote, Verwaltungsdaten |

**Ergebnis:** Vollständige Tabelle in `Daten_Inhaltsverzeichnis.md`

> 📄 **Weiterführende Dokumentation:** Die vollständige Analyse aller 86 Dateien mit Begründungen, Analysemethode und farbiger Klassifikationstabelle ist in **`Datensatz_Analyse_Bericht.docx`** dokumentiert.

**Schlüssel-Erkenntnisse:**
- Haupttabelle für Merkmale: **`SO.csv`** (Betten, Bundesland, Trägerart, Uni, Koordinaten)
- Ziel-Variable: **`QS.Qualitätsindikator.csv`** (>50 MB — nur per Python lesbar)
- Fortbildungsquote = `Erbracht / Pflichtige` aus `QS.Fortbildung.csv`

> ⚠️ **DSGVO-Hinweis: Personenbezogene Daten im Data/-Ordner**  
> Zwei Dateien enthalten echte Personendaten (Namen, E-Mail, Telefon von Krankenhauspersonal):
> - **`Personen.csv`** — Kontaktpersonen der Krankenhäuser (Vorname, Nachname, E-Mail, Telefon, Funktion)
> - **`FA.Personen.csv`** — Ärztliche Leitungen der Fachabteilungen (Vorname, Nachname, E-Mail, Telefon)
>
> Diese Dateien sind im `Data/`-Ordner, der per `.gitignore` **nicht** auf GitHub hochgeladen wird. Sie wurden **nicht** in die Analyse einbezogen und sind nicht in `analysetabelle.csv` enthalten. Die Daten stammen aus den öffentlich zugänglichen Qualitätsberichten 2023.

---

### 1.3 Ziel-Variable erstellen

**Quelle:** `QS.Qualitätsindikator.csv` — 29 Spalten, >50 MB

**Bewertungsspalte:** **`QSErgBewStrukDialog`**
- <span style="color:#27ae60">`R10` = Ergebnis liegt im Referenzbereich → **nicht auffällig**</span>
- `N01`/`N02`/`N99` = Bewertung nicht vorgesehen → **nicht bewertbar, ausgeschlossen** (nicht bewertet ≠ unauffällig!)
- <span style="color:#e74c3c">Alle übrigen Codes (H20/H99, U30–33/U99, A40–42/A99, D50/51/99, S90/91/99) = **auffällig**</span>, sobald sie überhaupt bewertbar sind

> ⚠️ **Wichtige Entscheidung:** `QSQI.AEKey` ist eine Haus-ID, kein Indikator-Schlüssel! Deduplizierung über `(SO.QBID, QSQI.Indikator)` — ein Fehler hier hätte zu 1 Zeile pro Haus geführt statt ~55 Zeilen.

**Berechnungsschritte:**

| Schritt | Code | Erklärung |
|---------|------|-----------|
| 1 | `QSQI.ArtDesWertes == 'QI'` | Nur echte QI, keine Zählkennzahlen |
| 2 | `~QSErgBewStrukDialog.str.startswith('N')` | Alle N\*-Codes raus (N01/N02/N99), nicht bewertbar |
| 3 | `drop_duplicates(['SO.QBID','QSQI.Indikator'])` | Je Haus+Indikator eine Zeile |
| 4 | `~str.startswith('R')` | Auffällig-Flag setzen: alles außer R10 zählt als auffällig |
| 5 | `groupby('SO.QBID').agg(count, sum)` | Pro Haus aggregieren |
| 6 | `auffaellig_n / total_qi` | Quote berechnen |
| 7 | `quote > Median → 1` | Binäre Ziel-Variable |

**Ergebnis:** Median-Quote = **5,88 %** | **1.821 Häuser** | ausgewogene Verteilung (905 vs. 916)

---

### 1.4 Merkmale auswählen & Analysetabelle zusammenführen

**Merkmale:**

| Merkmal | Quelle | Berechnung |
|---------|--------|-----------|
| `SO.Betten` | SO.csv | Direkt |
| `KH.Träger.Art` | SO.csv | Direkt |
| `SO.Bundesland` | SO.csv | Direkt |
| `SO.Uni` | SO.csv | Direkt |
| `SO.Latitude / SO.Longitude` | SO.csv | Direkt (für Karte) |
| `fortbildungsquote` | QS.Fortbildung.csv | `Erbracht / Pflichtige` |
| `aerzte_pro_bett` | FA.Personalliste.csv | `Σ Ärzte / SO.Betten` |
| `pflege_pro_bett` *(2026-07-29)* | SO.Personalliste.csv | `Σ Pflegekräfte / SO.Betten` |
| `ist_konzern` *(2026-07-29)* | Konzern.csv | `SO.Standortnummer` in Konzern.csv? → 0/1 |

**Entscheidung:** Zusammenführung vollständig per Skript reproduzierbar — kein manuelles Klicken.

**Analysetabelle (`Data/analysetabelle.csv`):**

| Kennzahl | Wert |
|----------|------|
| Zeilen (Krankenhäuser) | **1.821** |
| Spalten | 18 |
| Ziel-Variable = 1 (viele Probleme) | 905 (49,7 %) |
| Ziel-Variable = 0 (wenige Probleme) | 916 (50,3 %) |
| Fehlende Werte KH.Träger.Art | 28 (1,5 %) |
| Fehlende Werte fortbildungsquote | 33 (1,8 %) |
| Fehlende Werte aerzte_pro_bett | 5 (0,3 %) |
| Fehlende Werte pflege_pro_bett | 4 (0,2 %) |
| Konzernhäuser (ist_konzern=1) | 358 (19,7 %) |

**Wozu wird die Analysetabelle genutzt?** → Rohdaten → Analysetabelle → **alles andere.**

| Baustein | Nutzung |
|----------|---------|
| Baustein 2 | Grafiken direkt aus Tabelle erzeugen |
| Baustein 3 Seite 1 | `hat_viele_Probleme` + Koordinaten → Karte |
| Baustein 3 Seite 2 | Merkmale gruppiert → Vergleichsdiagramme |
| Baustein 3 Seite 3 | Filter → ähnliche Häuser |
| Baustein 4 | `X` = Merkmale, `y` = `hat_viele_Probleme` |

---

### 1.5 Ärzte pro Bett (Ergänzung)

**Quelle:** `FA.Personalliste.csv` × `FA.csv` über `ABTID`

**Vorgehen:**
- Filter: `FA.Personal.Bereich == "Ärzte"`
- `FA.Personal.Anzahl` = Komma-Dezimal → `.str.replace(",", ".")` → float
- Aggregation: Summe pro `ABTID` → pro `FA.QBID` → `aerzte_gesamt / SO.Betten`
- SO.Betten = 0 (Tageskliniken) → NaN — wird nicht aufgefüllt (kein echtes Verhältnis)

**Ergebnisse:** Ø **0,451** Ärzte/Bett | 5 fehlende Werte (4 Tageskliniken)

---

### 1.6 Pflegekräfte pro Bett (Ergänzung, 2026-07-29)

**Hintergrund:** Explizit in `Fragestellung.docx` gefordertes Merkmal — stand lange als offener Punkt in `ToDo.md`. Kollegen im BI-Tool-Vergleich (`BI_Datenanalyse.docx`) empfahlen dafür `AQ.Pflege.csv` oder `FA.Personalliste.csv` mit Pflege-Filter.

**Quelle:** `SO.Personalliste.csv` (direkt, kein Umweg über `FA.csv` nötig)

**Vorgehen:**
- Filter: `SO.Personal.Bereich == "Pflege"`
- Aggregation: Summe pro `SO.QBID` → `pflege_gesamt / SO.Betten`
- **Warum `SO.Personalliste.csv` statt `AQ.Pflege.csv`?** `AQ.Pflege.csv` enthält nur Qualifikationsnachweise, keine Personal-Anzahlen. `SO.Personalliste.csv` hat direkt `SO.QBID` + `SO.Personal.Anzahl`.

**Ergebnisse:** Ø **1,01** Pflegekräfte/Bett | 4 fehlende Werte | Feature Importance im Decision Tree: **10,75 %** (3. wichtigstes Merkmal, nach `aerzte_pro_bett` und `SO.Betten`)

---

### 1.7 Konzernzugehörigkeit (Ergänzung, 2026-07-29)

**Hintergrund:** Von den Kollegen im BI-Tool-Vergleich als „interessante Ergänzung" identifiziert (Konzernhäuser könnten durch zentrale Qualitätssicherung andere QI-Profile haben).

**Quelle:** `Konzern.csv`

> ⚠️ **Bug gefunden und behoben:** `Konzern.csv` nutzt `SO.Standortnummer` als Schlüssel — **nicht** `SO.QBID`. Der erste Join-Versuch verglich versehentlich `Konzern.csv`s `SO.Standortnummer` gegen `SO.csv`s `SO.QBID` → **0 Treffer**, `ist_konzern` war für alle Häuser 0. `SO.csv` hat aber selbst eine `SO.Standortnummer`-Spalte, die im ersten Anlauf nicht mit ausgewählt wurde. Nach Korrektur (Vergleich `SO.Standortnummer` gegen `SO.Standortnummer`): **358 von 1.821 Häusern (19,7 %)** sind Konzernhäuser.

**Ergebnis:** Chi²-Test zeigt **keinen** signifikanten Zusammenhang zwischen `ist_konzern` und `hat_viele_Probleme` (χ²=1,277, p=0,2585). Der Decision Tree bestätigt das mit **0 % Feature Importance**. Bewusst trotzdem im Modell gelassen — das Modell soll selbst entscheiden, kein Zusammenhang ist ein valider Befund.

---

## <span style="color:#2980b9">📊 Baustein 2 — Deskriptive Analyse</span>

<span style="background:#d4edda;color:#155724;padding:2px 8px;border-radius:4px;font-weight:bold">✅ Abgeschlossen</span> &nbsp; **Datum:** 2026-07-27 &nbsp; **Datei:** `02_Analyse.ipynb`

---

### 2.1 Vorgehen

10 Grafiken aus `Data/analysetabelle.csv`. Jede Grafik mit automatisch berechnetem Befundsatz. Farbschema: 🟢 grün = wenige Probleme, 🔴 rot = viele Probleme. Grafiken gespeichert in `grafiken/`. Pflegekräfte/Bett am 2026-07-29 ergänzt (mittlerweile in Grafik 5+6 zusammen mit Ärzte/Bett dargestellt); Konzernvergleich (Grafik 9) ebenfalls am 2026-07-29 ergänzt, Fortbildungsquote (Grafik 10) später als eigene Grafik ausgegliedert.

---

### 2.2 Befunde

| Grafik | Merkmal | Befund |
|--------|---------|--------|
| 1 | auffällig-Quote | Median **5,88 %**, rechtsschief — meisten Häuser zwischen 0 % und 11 % |
| 2 | Bettenzahl | Median: wenige=166, viele=220 — viele Probleme bei größeren Häusern |
| 3 | Trägerschaft | Privat 43,8 % vs. freigemeinnützig 50,6 % vs. öffentlich **53,5 %** — optisch sichtbar, aber ANOVA (2.3) nicht signifikant |
| 4 | Uni-Klinik | Uni **68,5 %** vs. Normal 48,7 % — ein deutlicher Unterschied |
| 5+6 | Fortbildung & Ärzte/Bett | Fortbildung: kein Unterschied; Ärzte/Bett: wenige=0,382, viele=0,470 |
| 7 | Bundesland | Rheinland-Pfalz höchster Anteil **(64,0 %)**, Thüringen niedrigster (36,0 %) |
| 8 | Korrelation | Stärkste Korrelation: `total_qi` **(r=+0,241)**, `aerzte_pro_bett` (r=+0,210) — alle Vorzeichen positiv |
| 9 | Scatter | Kein klares Trennmuster — starke Überlappung |
| 10 | Störfaktor | Private Häuser kleiner (Md=125 Betten) |
| 11 *(2026-07-29)* | Pflegekräfte/Bett | Wenige=0,891, Viele=1,047 — gleiches Muster wie Ärzte/Bett |
| 12 *(2026-07-29)* | Konzernvergleich | Konzern 52,5 % vs. unabhängig 49,0 % viele Probleme — praktisch kein Unterschied |

### 2.3 Inferenzstatistik (ergänzt)

| Test | Ergebnis | Befund |
|------|----------|--------|
| **T-Test** Ärzte/Bett (Wenige vs. Viele) | t=−9,13, **p<0,0001** | Unterschied statistisch **signifikant** |
| **T-Test** Pflegekräfte/Bett (Wenige vs. Viele) *(2026-07-29)* | t=−7,51, **p<0,0001** | Unterschied statistisch **signifikant** |
| **Chi²-Test** Konzernzugehörigkeit vs. viele Probleme *(2026-07-29)* | χ²=1,277, **p=0,2585** | **Kein** signifikanter Zusammenhang |
| **ANOVA** auffällig-Quote nach Träger | F=0,031, **p=0,969** | **Nicht signifikant**, obwohl Grafik 3 einen Unterschied zeigt |
| **95%-KI** Ärzte/Bett Wenige | [0,389–0,416] | Keine Überlappung mit Viele-Gruppe |
| **95%-KI** Ärzte/Bett Viele | [0,484–0,516] | Bestätigt signifikanten Unterschied |
| **pivot_table** Träger × Uni | Gemischtes Bild: bei freigemeinnützig/privat Uni niedriger, bei öffentlich Uni höher | Kein einheitlicher Effekt |

### 2.4 Gesamteinschätzung

Es zeigen sich mehrere statistisch signifikante Einzelzusammenhänge (Ärzte/Bett, Pflege/Bett, Uni-Status), aber der optisch auffällige Trägerschaftseffekt ist statistisch nicht abgesichert (ANOVA nicht signifikant). Stärkster Prädiktor bleibt `total_qi`, ein **Strukturmerkmal**, kein Qualitätsmerkmal. Kernbefund: mehr Personal pro Bett hängt mit **mehr**, nicht weniger, Qualitätsproblemen zusammen — am ehesten dadurch erklärbar, dass besser ausgestattete Häuser komplexere Fälle behandeln und dadurch mehr/andere Indikatoren auslösen (vgl. `total_qi`-Korrelation).

> 💡 **Kein Zusammenhang ist ein valides Ergebnis.** *(Quelle: Text_Presentation.docx, Folie 7)*

---

## <span style="color:#8e44ad">🖥️ Baustein 3 — Dashboard bauen</span>

<span style="background:#d4edda;color:#155724;padding:2px 8px;border-radius:4px;font-weight:bold">✅ Live</span> &nbsp; **Werkzeug:** Streamlit &nbsp; **Dateien:** `Dashboard/streamlit_dashboard.py`, `Dashboard/dashboard_utils.py`

**Umgesetzt:**
- Seite 1 „Übersicht": Kennzahlen + Deutschland-Karte + Verteilung
- Seite 2 „Vergleiche": Dropdown → Verteilung MIT vs. OHNE viele Probleme, Pivot-Tabelle
- Seite 3 „Ähnliche Häuser": Filter nach Betten / Region / Träger + Einzelhaus-Steckbrief
- Seite 4 „Risiko-Rechner" *(Bonus)*: Decision Tree Vorhersage — seit 2026-07-29 inkl. Eingabefelder für Pflegekräfte/Bett und Konzernstatus

**Deployment:** Streamlit Community Cloud — live unter [Qualitäts-Muster-Finder Dashboard](https://appdashboardpy-dkgplgkkzczyvnwpfjjcsp.streamlit.app/)

**Technischer Hinweis:** `streamlit_dashboard.py` und `dashboard_utils.py` wurden am 2026-07-29 von `scripts/` in einen eigenen `Dashboard/`-Ordner verschoben. `modell_klasse.py` wiederum wurde am 2026-07-30 von `scripts/` in einen eigenen `model/`-Ordner verschoben. Alle drei Ordner sind getrennt — der Import von `modell_klasse` läuft über eine `sys.path`-Ergänzung zur Laufzeit. Der Main-File-Pfad in den Streamlit-Cloud-Einstellungen muss entsprechend aktualisiert werden.

---

## <span style="color:#e67e22">🤖 Baustein 4 — Entscheidungsbaum</span> *(Bonus)*

<span style="background:#d4edda;color:#155724;padding:2px 8px;border-radius:4px;font-weight:bold">✅ Abgeschlossen</span> &nbsp; **Datum:** 2026-07-27, neu trainiert 2026-07-29 &nbsp; **Datei:** `03_Decision_Tree.ipynb`

- **OOP:** Klasse `KrankenhausModell` mit `prepare()`, `fit()`, `evaluate()`, `save()`, `load()` — Notebook importiert die Klasse jetzt aus `model/modell_klasse.py`, statt sie inline zu duplizieren *(behebt einen `__main__`-Pickle-Bug, der das Dashboard beim Laden des Modells crashen ließ)*

- **Train-Test-Split:** 80/20 (1.456/365), stratifiziert | Basislinie: 50,4 %
- **Metriken:** Accuracy=0,570 | Precision=0,552 | Recall=0,702 | F1=0,618 | CV=0,616±0,037
- **R²=−0,007** (auf `auffaellig_quote`) — Strukturmerkmale erklären die Varianz linear **nicht**, schlechter als die reine Durchschnittsvorhersage → deutlich ernüchternder als vorher
- **Feature Importance:** `aerzte_pro_bett` 72,8 %, `SO.Betten` 16,5 %, `pflege_pro_bett` 10,8 % — alle anderen (inkl. `traeger_enc`, `ist_konzern`) 0 %
- **Wichtigster Split:** `aerzte_pro_bett ≤ 0,271`
- **`joblib`:** Modell gespeichert als `Data/modell_krankenhaus.pkl`

---

## <span style="color:#c0392b">🏁 Baustein 5 — Abschluss & Präsentation</span>

<span style="background:#fff3cd;color:#856404;padding:2px 8px;border-radius:4px;font-weight:bold">🟡 Teilweise erledigt</span>

**Erledigt:** Startanleitung (`README.md`), Entscheidungen dokumentiert (`README.md`, `ProjektDetails.md`, dieses Dokument), Komplett-Durchlauf getestet (Rohdaten → Notebooks 1–3 → Dashboard, fehlerfrei)

**Noch offen:** Randfälle im Dashboard testen, Code aufräumen, Entscheidungsbegründungen für Präsentation ausformulieren, Präsentation mit Live-Demo + Generalprobe

---

*Zuletzt aktualisiert: 2026-08-14*

---

## 📁 Erstellte Projektdateien

> Übersicht aller Dateien, die im Laufe des Projekts erstellt wurden — mit Zweck und Baustein-Zuordnung. Diese Übersicht wurde am 2026-08-14 gegen den tatsächlichen Datei-Bestand abgeglichen (vorher enthielt sie mehrere zwischenzeitlich umbenannte/gelöschte Dateien).

### 📒 Notebooks

| Datei | Baustein | Zweck |
|-------|----------|-------|
| `01_Exploration.ipynb` | Baustein 1 | Datenaufbereitung: Ziel-Variable, Merkmale, Analysetabelle, Ärzte/Pflege pro Bett, Konzernzugehörigkeit |
| `02_Analyse.ipynb` | Baustein 2 | Deskriptive Analyse: 12 Grafiken, T-Test, Chi²-Test, ANOVA, Konfidenzintervalle, pivot_table |
| `03_Decision_Tree.ipynb` | Baustein 4 | Decision Tree, OOP (importiert aus model/modell_klasse.py), Metriken, R², Feature Importance, joblib |
| `04_Potenzielle_Erweiterungen.ipynb` | Baustein 5 (Bonus) | Prüft zusätzliche Merkmale (Dokumentationsrate, Notfallstufe, Mindestmengen) als mögliche Modellerweiterung |

### 🖥️ Dashboard

| Datei | Baustein | Zweck |
|-------|----------|-------|
| `Dashboard/streamlit_dashboard.py` | Baustein 3 | Haupt-App: 4 Seiten (Gesamtüberblick, Einflussfaktoren, Häuser vergleichen, Qualitäts-Vorhersage) |
| `Dashboard/dashboard_utils.py` | Baustein 3 | Hilfsfunktionen: Daten laden, KPIs, Plots, Modell-Vorhersage |

### 🧠 Modell-Logik (`model/`)

| Datei | Baustein | Zweck |
|-------|----------|-------|
| `modell_klasse.py` | Baustein 4 | OOP-Wrapper `KrankenhausModell` — einzige Quelle der Wahrheit für Features & Modell-Logik |

### 🐍 Python-Module (`scripts/`)

| Datei | Baustein | Zweck |
|-------|----------|-------|
| `projekt_doku.py` | Baustein 1 | Generiert `Dokumentation_Qualitaets_Muster_Finder.docx` (Hauptdokumentation) |
| `datensatz_uebersicht.py` | Baustein 1 | Generiert `Datensatz_Uebersicht.docx` (Datei-Klassifikation aller 86 CSVs) |
| `analysetabelle_zusammenfassung.py` | Baustein 1 | Generiert `Analysetabelle_Zusammenfassung.docx`: Merkmale, Ziel-Variable, Quelltabellen, Merge-Kriterien, Endgröße |
| `grafiken_doku.py` | Baustein 2 | Generiert `Grafiken_Dokumentation.docx`: alle 12 Grafiken aus `02_Analyse.ipynb` erklärt, Zahlen live berechnet |
| `erstelle_dozenten_doku.py` | Baustein 1+2 | Erzeugte den Fortschrittsbericht für den Dozenten (Zwischenpräsentation); `Doku/Dozent/` wurde nach der Zwischenpräsentation wieder entfernt |
| `erstelle_praesentationsskript.py` | Baustein 5 | Generiert `Doku/PPT/Praesentationsskript_Qualitaets_Muster_Finder.docx` (Sprechertext je Folie) |

### 📊 Datendateien

| Datei | Baustein | Zweck |
|-------|----------|-------|
| `Data/analysetabelle.csv` / `.xlsx` | Baustein 1 | Finale Analysetabelle: 1.821 Häuser × 18 Spalten — Basis für alles weitere |
| `Data/modell_krankenhaus.pkl` | Baustein 4 | Trainiertes Decision-Tree-Modell (joblib) — bereit für Dashboard |

### 📄 Dokumentation (Word, `Doku/Word/`)

| Datei | Inhalt |
|-------|--------|
| `Dokumentation_Qualitaets_Muster_Finder.docx` | Hauptdokumentation: Projektübersicht, Baustein 1+2 komplett mit Ergebnissen und Grafiken |
| `Datensatz_Uebersicht.docx` | Analyse aller 86 CSV-Dateien: Klassifikation, Analysemethode, Datenmodell |
| `Analysetabelle_Zusammenfassung.docx` | Merkmale, Ziel-Variable, Quelltabellen, Merge-Kriterien, Endgröße der Analysetabelle |
| `Grafiken_Dokumentation.docx` | Alle 12 Grafiken aus Baustein 2 erklärt |
| `Dashboard_Uebersicht.docx` | Überblick über das Streamlit-Dashboard |
| `ML_Doku.docx` | Machine-Learning-Dokumentation (Decision Tree) |
| `Praesentation_Folienvorschlag.docx` | Folienvorschlag für die Abschlusspräsentation |

### 📄 Dokumentation (Dozent & Präsentation)

| Datei | Inhalt |
|-------|--------|
| `Doku/PPT/Praesentationsskript_Qualitaets_Muster_Finder.docx` | Vollständiges Präsentationsskript mit Sprechertext je Folie |
| `Doku/PPT/Qualitaets_Muster_Finder.pptx` | Foliensatz (Einzelpräsentator) |
| `Doku/PPT/Qualitaets_Muster_Finder_Teamvortrag.pptx` | Foliensatz (Team-Variante, 3 Präsentatoren) |

### 📝 Markdown-Dateien (`Doku/MD/`)

| Datei | Zweck |
|-------|-------|
| `Workflow.md` | Dieses Dokument: Vorgehen, Entscheidungen, Verweise |
| `01_Exploration.md` | Schritt-für-Schritt-Erklärung von `01_Exploration.ipynb` — was gemacht wurde und warum |
| `02_Analyse.md` | Schritt-für-Schritt-Erklärung von `02_Analyse.ipynb` — was gemacht wurde und warum |
| `03_Decision_Tree.md` | Schritt-für-Schritt-Erklärung von `03_Decision_Tree.ipynb` — was gemacht wurde und warum |
| `04_Potenzielle_Erweiterungen.md` | Schritt-für-Schritt-Erklärung von `04_Potenzielle_Erweiterungen.ipynb` |
| `05_Dashboard.md` | Erklärung des Streamlit-Dashboards: technische Umsetzung, Seiten, Zweck, Bedienung |
| `Daten_Inhaltsverzeichnis.md` | Tabellarische Übersicht aller 86 CSV-Dateien mit Relevanz-Einstufung |
| `Qualitätsindikator.md` | Detaildokumentation von `QS.Qualitätsindikator.csv` und seiner Rolle als Ziel-Variable |
| `Praesentation_Folien_Beschreibung.md` | Folienbeschreibung für die Einzelpräsentator-Variante |
| `Praesentation_Team_Folien_Beschreibung.md` | Folienbeschreibung für die Team-Variante (3 Präsentatoren) |

*(`ToDo.md` und `ProjektDetails.md` liegen im Projekt-Root, nicht in `Doku/MD/`.)*

### 🖼️ Grafiken

| Ordner/Datei | Inhalt |
|-------------|--------|
| `grafiken/g1_auffaellig_quote.png` | Verteilung der auffällig-Quote |
| `grafiken/g2_bettenzahl.png` | Bettenzahl MIT vs. OHNE Probleme |
| `grafiken/g3_traegerschaft.png` | Trägerschaft-Vergleich |
| `grafiken/g4_uni.png` | Uni-Kliniken vs. normale Häuser |
| `grafiken/g5_6_aerzte_pflege.png` | Ärzte/Bett & Pflegekräfte/Bett |
| `grafiken/g7_bundesland_kachelkarte.png` | Anteil je Bundesland (Kachelkarte) |
| `grafiken/g8_korrelation.png` | Korrelationsmatrix |
| `grafiken/g9_konzern_vergleich.png` | Konzernhaus vs. unabhängiges Haus |
| `grafiken/g10_fortbildungsquote.png` | Fortbildungsquote MIT vs. OHNE viele Probleme |
| `grafiken/g11_confusion_matrix.png` | Confusion Matrix Decision Tree |
| `grafiken/g12_decision_tree.png` | Visualisierung Entscheidungsbaum |
| `grafiken/g13_feature_importance.png` | Feature Importance Balkendiagramm |
