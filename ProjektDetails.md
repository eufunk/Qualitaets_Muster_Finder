# 📁 Projektstruktur — QualitaetsMusterFinderProjekt

> **Projektfrage:** Welche Krankenhausmerkmale hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme aufweist?
>
> **Datenbasis:** IQTIG Qualitätsberichte 2023 — 1.821 deutsche Krankenhäuser mit auswertbarer Qualitätsbewertung

> ℹ️ **Hinweis zu diesem Dokument:** Es listet ausschließlich Dateien, die tatsächlich per Git versioniert werden (Stand `.gitignore`, 2026-08-30). Lokal vorhandene, aber bewusst nicht eingecheckte Inhalte — u. a. der komplette `scripts/`-Ordner, die Rohdaten in `Data/CSV/` und `Data/Excel/` sowie einzelne Zusatzdateien — sind hier nicht aufgeführt. Ausnahme: `Doku/PPT/` ist inzwischen **teilweise** versioniert — `Projektbegleitende_Praesentation.pptx` wird per `.gitignore`-Ausnahme eingecheckt, alle anderen Dateien in diesem Ordner (u. a. das Teamvortrag-Deck) bleiben lokal.

---

## 🏗️ Aufbau nach Bausteinen

Das Projekt folgt einer **5-Baustein-Struktur** plus einem optionalen Erweiterungs-Notebook:

| Baustein | Status | Hauptdatei (versioniert) |
|----------|--------|------------|
| 1 — Daten vorbereiten | ✅ Abgeschlossen | `Notebooks/01_Exploration.ipynb` |
| 2 — Deskriptive Analyse | ✅ Abgeschlossen | `Notebooks/02_Analyse.ipynb` |
| 3 — Streamlit-Dashboard | ✅ Live | `Dashboard/streamlit_dashboard.py` |
| 4 — Entscheidungsbaum (Bonus) | ✅ Abgeschlossen | `Notebooks/03_Decision_Tree.ipynb` |
| 5 — Abschluss & Präsentation | 🟡 Unterlagen fertig, Vortrag noch offen | `Doku/PPT/Projektbegleitende_Praesentation.pptx` |
| Bonus — Potenzielle Erweiterungen | ✅ Analysiert, **nicht ins Hauptmodell übernommen** | `Notebooks/04_Potenzielle_Erweiterungen.ipynb` |

---

## 🏗️ Projektstruktur (versionierter Stand — 2026-08-30)

```
QualitaetsMusterFinderProjekt/
│
├── 📒 Notebooks/ (5) — Datenanalyse & ML
│   ├── 01_Exploration.ipynb              → Datenaufbereitung (86 CSVs → Data/analysetabelle.csv)
│   ├── 01_Exploration_Ref.ipynb          → Referenz-Konkordanzanalyse: Python-Nachrechnung vs. offizielle Bewertungsspalte
│   ├── 02_Analyse.ipynb                  → Deskriptive Analyse (12 Grafiken, T-Test, Chi²-Test, ANOVA, Gesamtquote)
│   ├── 03_Decision_Tree.ipynb            → ML: Decision Tree, Feature Importance (importiert KrankenhausModell aus model/)
│   └── 04_Potenzielle_Erweiterungen.ipynb → prüft 3 bisher ungenutzte CSVs auf zusätzliches Signal (siehe Kern-Ergebnisse)
│
├── 🖥️ Dashboard/ — Streamlit-App (2)
│   ├── streamlit_dashboard.py    → Haupt-App: 4 Seiten (Gesamtüberblick, Einflussfaktoren, Häuser vergleichen, Qualitäts-Vorhersage)
│   └── dashboard_utils.py        → Hilfsfunktionen: Daten laden, KPIs, Plots (u. a. interaktive Bundesland-Kachelkarte), Modell-Vorhersage (importiert modell_klasse aus model/ via sys.path)
│
├── 🧠 model/ — Modell-Logik (1)
│   └── modell_klasse.py          → OOP-Wrapper KrankenhausModell (prepare, fit, evaluate, save, load)
│
├── 📊 Data/ (2) — liegt größtenteils in Data/, per .gitignore-Ausnahme trotzdem im Repo
│   ├── analysetabelle.csv        → Zentrale Analysetabelle (1.821 Häuser × 18 Spalten)
│   └── modell_krankenhaus.pkl    → Trainiertes Decision-Tree-Modell
│
├── 🖼️ grafiken/ (19) — 15 PNG-Grafiken + 4 Dashboard-Screenshots
│   ├── g1_auffaellig_quote.png … g13_feature_importance.png (durchgehend g+Nummer benannt, 12 Grafiken für Notebooks/Doku)
│   ├── g2_bettenzahl_nebeneinander.png → Histogramm+Boxplot nebeneinander statt untereinander, nur für die breite Foliendarstellung
│   ├── g14_bettenanzahl.png, g15_auffaellig_verteilung_kreis.png → zusätzliche, nur für den Teamvortrag erzeugte Grafiken
│   └── screenshots/ → 4 Dashboard-Screenshots (einflussfaktoren, gesamtuberblick, haeuser_vergleichen, qualitaets_vorhersage.png)
│
├── 📄 Dokumentation
│   ├── README.md                 → Hauptdokumentation mit Startanleitung
│   ├── ProjektDetails.md         → Detaillierte Projektstruktur & Entscheidungen (dieses Dokument)
│   ├── ToDo.md                   → Aufgabenliste + IHK-Abgleich
│   ├── Doku/MD/ (11 Dateien)      → Markdown-Dokumentation
│   │   ├── Workflow.md, 01_Exploration.md, 01_Exploration_Ref.md, 02_Analyse.md, 03_Decision_Tree.md
│   │   ├── 04_Potenzielle_Erweiterungen.md → Walkthrough zum Bonus-Notebook
│   │   ├── 05_Dashboard.md                 → Doku zur Dashboard-Bedienung/Layout
│   │   ├── Daten_Inhaltsverzeichnis.md     → Übersicht aller 86 CSV-Dateien
│   │   ├── Fragen_und_Antworten.md         → 30 vorbereitete Fragen & Antworten für Rückfragen
│   │   ├── IQTIG.md                        → Auswertung des offiziellen IQTIG-Bundesqualitätsberichts 2023
│   │   └── Qualitätsindikator.md           → Deep-Dive zur größten Rohdatei (QS.Qualitätsindikator.csv, 911,7 MB)
│   ├── Doku/Word/ (7 Dateien)     → Word-Exporte, siehe Datei-Übersicht unten
│   └── Doku/PPT/ (1 Datei)        → Projektbegleitende_Praesentation.pptx — einzige versionierte Foliendatei
│
└── ⚙️ Konfiguration
    ├── .gitignore                → Schließt Data/* aus (außer den 2 !-Ausnahmen), sowie scripts/, Doku/PPT/* (außer 1 Ausnahme), .devcontainer/, Doku/Archiv/, Aufgabenstellung/* (außer den 2 Fragestellung-Ausnahmen) und weitere Einzeldateien
    └── requirements.txt          → 12 Pakete (streamlit, plotly, nbformat, ipykernel, pandas, scikit-learn, joblib, scipy, numpy, matplotlib, seaborn, statsmodels)
```

---

## 📂 Datei-Übersicht

### 📒 Notebooks (5) — im Ordner `Notebooks/`

- `Notebooks/01_Exploration.ipynb` — Datenaufbereitung: 86 CSV-Dateien erkunden, Ziel-Variable bauen, Merkmale zusammenführen → `Data/analysetabelle.csv`
- `Notebooks/01_Exploration_Ref.ipynb` — Referenz-Konkordanzanalyse: eigene Python-Nachrechnung der Auffälligkeit gegen die offizielle Bewertungsspalte verglichen (96,0 % Zeilen-Übereinstimmung, 75,9 % Gruppen-Übereinstimmung) — begründet, warum `QSErgBewStrukDialog` direkt übernommen statt selbst nachgerechnet wird
- `Notebooks/02_Analyse.ipynb` — Deskriptive Analyse: 12 Grafiken, T-Test, Chi²-Test, ANOVA, Konfidenzintervalle, Korrelationen, indikator-/hausgewichtete Gesamtquote
- `Notebooks/03_Decision_Tree.ipynb` — ML: Decision Tree (max_depth=3), Metriken, R², Feature Importance, joblib
- `Notebooks/04_Potenzielle_Erweiterungen.ipynb` — Prüft 3 der bisher ungenutzten 79 CSV-Dateien (`QS.Leistungsbereich.csv`, `Notfallversorgung.csv`, `MM.csv`) auf zusätzliches Erklärungssignal für `hat_viele_Probleme`. Ergebnis: zwei empfohlene, aber **noch nicht integrierte** Merkmale (siehe Kern-Ergebnisse)

### 🖥️ Dashboard (2) — im Ordner `Dashboard/`

- `Dashboard/streamlit_dashboard.py` — Haupt-App mit 4 Seiten (Gesamtüberblick, Einflussfaktoren, Häuser vergleichen, Qualitäts-Vorhersage)
- `Dashboard/dashboard_utils.py` — Hilfsfunktionen: Daten laden, KPIs, Plots, Modell-Vorhersage (Trennung Logik/UI); lädt `Data/analysetabelle.csv` & `Data/modell_krankenhaus.pkl`; importiert `KrankenhausModell` aus `model/modell_klasse.py` (Pfad wird zur Laufzeit über `sys.path` ergänzt, da beide Ordner getrennt sind). Deutschland-Karte nutzt `px.scatter_map` (nicht mehr das veraltete `scatter_mapbox`); der Bundesland-Vergleich ist eine interaktive Kachelkarte (`erstelle_bundesland_kachelkarte`) statt eines Balkendiagramms

### 🧠 Modell-Logik (1) — im Ordner `model/`

- `model/modell_klasse.py` — OOP-Wrapper `KrankenhausModell` (prepare, fit, evaluate, save, load); Default-Modellpfad `Data/modell_krankenhaus.pkl`. Einzige Quelle der Wahrheit für Features & Modell-Logik — wird von `Dashboard/dashboard_utils.py` und `Notebooks/03_Decision_Tree.ipynb` ordnerübergreifend importiert (`sys.path`-Ergänzung, kein echtes Python-Package)

> **Hinweis:** Die Word-Dokumente in `Doku/Word/` (siehe unten) werden von Python-Skripten in `scripts/` erzeugt. Dieser Ordner ist per `.gitignore` bewusst nicht versioniert (lokales Arbeitswerkzeug) — die daraus erzeugten `.docx`-Ergebnisse sind es aber, damit die Dokumentation ohne lokalen Skript-Lauf einsehbar bleibt.

### 📊 Daten (2) — im Ordner `Data/`

- `Data/analysetabelle.csv` — Zentrale Analysetabelle: 1.821 Häuser × 18 Spalten (Basis für alles)
- `Data/modell_krankenhaus.pkl` — Trainiertes Decision-Tree-Modell (joblib)

> Diese 2 Dateien sind die einzigen Inhalte von `Data/`, die per `.gitignore`-Ausnahme (`!Data/...`) trotzdem versioniert werden — die Rohdaten-CSVs/-Excels in `Data/CSV/` und `Data/Excel/` sowie `Data/analysetabelle.xlsx` bleiben ausgeschlossen.

### 📄 Dokumentation (Markdown)

- `README.md` — Hauptdokumentation mit Startanleitung & "Wichtige Entscheidungen"
- `ProjektDetails.md` — Detaillierte Projektstruktur & Entscheidungen (dieses Dokument)
- `ToDo.md` — Aufgabenliste mit Haken + IHK-Abgleich
- `Doku/MD/Workflow.md` — Vollständige Workflow-Dokumentation pro Baustein
- `Doku/MD/01_Exploration.md` — Schritt-für-Schritt-Erklärung von `01_Exploration.ipynb`
- `Doku/MD/01_Exploration_Ref.md` — Schritt-für-Schritt-Erklärung von `01_Exploration_Ref.ipynb` (Konkordanzanalyse)
- `Doku/MD/02_Analyse.md` — Schritt-für-Schritt-Erklärung von `02_Analyse.ipynb`
- `Doku/MD/03_Decision_Tree.md` — Schritt-für-Schritt-Erklärung von `03_Decision_Tree.ipynb`
- `Doku/MD/04_Potenzielle_Erweiterungen.md` — Walkthrough zu `04_Potenzielle_Erweiterungen.ipynb` inkl. Hypothesen, Ergebnissen und Empfehlungen je geprüfter Datei
- `Doku/MD/05_Dashboard.md` — Doku zu Aufbau, Navigation und Seiten des Streamlit-Dashboards
- `Doku/MD/Daten_Inhaltsverzeichnis.md` — Übersicht aller 86 CSV-Dateien
- `Doku/MD/Fragen_und_Antworten.md` — 30 vorbereitete Fragen & Antworten zur Absicherung gegen Rückfragen des Dozenten
- `Doku/MD/IQTIG.md` — Auswertung des offiziellen IQTIG-Bundesqualitätsberichts 2023 (Methodik, Beleg für IQTIG/G-BA-Herkunft der Rohdaten)
- `Doku/MD/Qualitätsindikator.md` — Deep-Dive zu `QS.Qualitätsindikator.csv` (911,7 MB, größte Rohdatei, 29 Spalten)

### 📄 Dokumentation (Word) — im Ordner `Doku/Word/`

- `Dokumentation_Qualitaets_Muster_Finder.docx` — Hauptdokumentation
- `Datensatz_Uebersicht.docx` — Datei-Klassifikation aller 86 Rohdaten
- `Grafiken_Dokumentation.docx` — Erklärung aller 12 Analyse-Grafiken
- `Analysetabelle_Zusammenfassung.docx` — Merkmale, Ziel-Variable, Quelltabellen, Merge-Kriterien, Endgröße
- `Dashboard_Uebersicht.docx` — Word-Fassung von `Doku/MD/05_Dashboard.md`
- `ML_Doku.docx` — Word-Fassung des Decision-Tree-Walkthroughs
- `Projektbegleitende_Dokumentation.docx` — Großes, kapitelweise gewachsenes Begleitdokument (6 Kapitel: Aufgabenstellung, Datenaufbereitung, Deskriptive Analyse, ML-Modell, Dashboard, Fazit/Grenzen/Ausblick)

### 🖼️ Doku/PPT/ — im Ordner `Doku/PPT/`

- `Projektbegleitende_Praesentation.pptx` — Foliengenerierte Entsprechung der Projektbegleitenden Dokumentation, 6 Kapitel. Einzige Datei aus `Doku/PPT/`, die per `.gitignore`-Ausnahme versioniert wird — das separate Teamvortrag-Deck bleibt bewusst lokal

### 🖼️ Grafiken (`grafiken/`)

15 PNG-Dateien (siehe Kern-Ergebnisse unten für Details) — `g1`–`g13` durchgehend nummeriert (12 Grafiken für Notebooks/Doku, `g5_6` als eine Datei für beide Grafiken), plus `g2_bettenzahl_nebeneinander.png` (Histogramm+Boxplot nebeneinander für breite Folien) sowie `g14_bettenanzahl.png` und `g15_auffaellig_verteilung_kreis.png` (nur für den Teamvortrag). Dazu:

- `grafiken/screenshots/` — 4 Dashboard-Screenshots (`einflussfaktoren.png`, `gesamtuberblick.png`, `haeuser_vergleichen.png`, `qualitaets_vorhersage.png`) — **Stand 2026-08-30**, per Playwright gegen das laufende Dashboard neu aufgenommen, zeigen die aktuellen Kennzahlen (1.821 Häuser, 8,6 % Ø auffällig-Quote, 57,0 % Accuracy)

### ⚙️ Konfiguration

- `.gitignore` — Schließt `Data/*` aus (Rohdaten, 86 CSVs/Excels sowie `analysetabelle.xlsx`) außer den 2 `!`-Ausnahmen; schließt zusätzlich `scripts/`, `.devcontainer/`, `Doku/Archiv/` (rein manuell gepflegtes persönliches Archiv), zwei externe IQTIG-Quell-PDFs und `Aufgabenstellung/` aus. `Doku/PPT/*` ist ebenfalls ausgeschlossen, mit einer gezielten `!`-Ausnahme für `Projektbegleitende_Praesentation.pptx`
- `requirements.txt` — 12 Pakete: streamlit, plotly, nbformat, ipykernel, pandas, scikit-learn, joblib, scipy, numpy, matplotlib, seaborn, statsmodels (statsmodels wird von Plotly fuer die Trendlinien im Streudiagramm-Tab benoetigt)

> `.devcontainer/devcontainer.json` (GitHub-Codespaces-Konfiguration) liegt lokal vor, ist aber bewusst nicht versioniert — Codespaces wird für dieses Projekt nicht genutzt, das Deployment läuft über Streamlit Community Cloud.

---

## 🔗 Datenfluss

```
Rohdaten (Data/CSV, Data/Excel — 86 Dateien, nicht im Repo)
    ↓ Notebooks/01_Exploration.ipynb
Data/analysetabelle.csv (1.821 Häuser × 18 Spalten)
    ↓                          ↓                              ↓ (nur read-only, Ergebnisse nicht zurückgeführt)
Notebooks/02_Analyse.ipynb  Notebooks/03_Decision_Tree.ipynb  Notebooks/04_Potenzielle_Erweiterungen.ipynb
(Grafiken → grafiken/)    (modell_krankenhaus.pkl)            (nur Analyse, keine neue Ausgabedatei)
    ↓                          ↓
    └──────────┬───────────────┘
               ↓
    Dashboard/streamlit_dashboard.py (Live-Dashboard)
    ├── Dashboard/dashboard_utils.py (Logik)
    └── model/modell_klasse.py (Modell-Wrapper, ordnerübergreifend importiert)
```

> `04_Potenzielle_Erweiterungen.ipynb` liest `analysetabelle.csv` nur lesend und joint testweise zusätzliche Merkmale hinzu — die Ergebnisse fließen **nicht automatisch** zurück in `01_Exploration.ipynb`, `Data/analysetabelle.csv` oder das trainierte Modell. Eine Übernahme wäre ein manueller Folgeschritt (siehe Kern-Ergebnisse & Offene Punkte).

---

## 🎯 Kern-Ergebnisse

| Kennzahl | Wert |
|----------|------|
| Häuser analysiert | 1.821 |
| Ø Indikatoren pro Haus | 42,6 |
| Median auffällig-Quote | **5,88 %** |
| Träger mit höchstem Anteil | Öffentlich: **53,5 %** — laut ANOVA aber NICHT signifikant (p = 0,969) |
| Signifikantester Unterschied (Baustein 2) | Ärzte/Bett (T-Test p < 0,0001, r = +0,21) |
| Konzernhäuser | 358 von 1.821 (19,7 %) — kein signifikanter Zusammenhang mit Qualitätsproblemen (Chi² p = 0,2585) |
| Decision Tree Accuracy | **57,0 %** (Basislinie: 50,4 %) |
| R² (lineare Regression auf auffaellig_quote) | **−0,007** — kein linear nutzbarer Zusammenhang |
| Wichtigster Prädiktor im aktuellen Modell | `aerzte_pro_bett` (Feature Importance 72,8 %), gefolgt von `SO.Betten` (16,5 %) und `pflege_pro_bett` (10,8 %) |

> **Fazit Baustein 1–4:** Keine starken, eindeutigen Zusammenhänge zwischen Strukturmerkmalen und Qualitätsproblemen. Mehr Personal pro Bett hängt mit mehr, nicht weniger, Qualitätsproblemen zusammen — die Trägerschaft zeigt trotz optisch sichtbarem Unterschied laut ANOVA keinen statistisch abgesicherten Zusammenhang. **Kein Zusammenhang ist ein valides Ergebnis.**

### Zusatzbefunde aus `04_Potenzielle_Erweiterungen.ipynb` (noch nicht integriert)

| Geprüfte Datei | Neues Merkmal | Korrelation mit `hat_viele_Probleme` | Empfehlung |
|---|---|---|---|
| `QS.Leistungsbereich.csv` | `mittl_doku_rate` (Dokumentationsrate) | **r = +0,208**, p < 0,0001 — vergleichbar stark wie `aerzte_pro_bett` (r = +0,21) | ✅ Einbinden — starker Zusammenhang, erklärt sich wie `total_qi` über die Anzahl bewertbarer Indikatoren |
| `Notfallversorgung.csv` | `notfall_stufe` (0–3) | **r = +0,181**, p < 0,0001 | ✅ Einbinden — erklärt jetzt direkt (ohne Paradox), dass Häuser mit Notfallversorgung komplexere Fälle behandeln |
| `MM.csv` (Mindestmengen) | `mm_compliance_rate` | r = −0,011, p = 0,7155 — nicht signifikant, Median 100 % in beiden Gruppen | ❌ Nicht einbinden — kein Effekt, nur 1.013/1.821 Häuser abgedeckt |

> Würden `mittl_doku_rate` und `notfall_stufe` in `analysetabelle.csv` aufgenommen, wäre laut Notebook 04 ein spürbarer Effekt auf Feature-Ranking und Modellgüte plausibel — sicher ist das aber erst nach einem tatsächlichen Nachtraining. Dieser Schritt ist bewusst (noch) nicht umgesetzt.

---

## 🚀 Lokal starten

```bash
pip install -r requirements.txt
streamlit run Dashboard/streamlit_dashboard.py
```

→ Dashboard öffnet sich unter `http://localhost:8501`

**Benötigte Dateien für den Dashboard-Betrieb:**

- `Dashboard/streamlit_dashboard.py` — Haupt-App
- `Dashboard/dashboard_utils.py` — Funktionen & Plots
- `model/modell_klasse.py` — Decision Tree Klasse (wird von `dashboard_utils.py` ordnerübergreifend importiert)
- `Data/modell_krankenhaus.pkl` — Trainiertes Modell
- `Data/analysetabelle.csv` — Datenbasis (1.821 Häuser)
- `requirements.txt`
- `grafiken/` — PNG-Grafiken (optional)

> ⚠️ Die Rohdaten in `Data/CSV/` und `Data/Excel/` sind **nicht** im Repository. Für den Dashboard-Betrieb reichen `Data/analysetabelle.csv` und `Data/modell_krankenhaus.pkl` — diese beiden sind über eine `.gitignore`-Ausnahme trotzdem versioniert, obwohl sie im sonst ausgeschlossenen `Data/`-Ordner liegen.

> Live-Dashboard: [Qualitäts-Muster-Finder Dashboard](https://appdashboardpy-dkgplgkkzczyvnwpfjjcsp.streamlit.app/)

---

## ⚠️ Offene Punkte

**Präsentation:**
- [ ] Fragestellung vorstellen, Hürden & Erkenntnisse, Befunde der deskriptiven Analyse benennen
- [ ] Live-Demo des Dashboards (alle 4 Seiten)
- [ ] Grenzen der Analyse ehrlich benennen
- [ ] Generalprobe mit Stoppuhr
- [ ] Abschlusspräsentation halten + gemeinsame Retrospektive

**Code-/Doku-Aufräumen:**
- [ ] Entscheiden, ob `mittl_doku_rate` und `notfall_stufe` aus `04_Potenzielle_Erweiterungen.ipynb` in `analysetabelle.csv` und das Modell übernommen werden
- [ ] Toter Verweis in `Doku/MD/01_Exploration.md` auf die inzwischen gelöschte `BI_Analyse/`-Dokumentation bereinigen

**Erledigt (Auswahl, Stand 2026-08-30):**
- ✅ Ziel-Variable in `01_Exploration.ipynb` berechnet: `QSErgBewStrukDialog`-Code `R10` bedeutet „nicht auffällig"
- ✅ `02_Analyse.ipynb`, `03_Decision_Tree.ipynb` und `04_Potenzielle_Erweiterungen.ipynb` inkl. aller MD-Dokus gegen die aktuelle `analysetabelle.csv` ausgeführt
- ✅ Alle Word-Dokument-Generatoren in `scripts/` und deren Ausgabedateien auf die aktuellen Kennzahlen abgestimmt
- ✅ Fehlendes `scripts/Grafiken_Speichern.py` neu erstellt und alle 12 PNG-Grafiken erzeugt
- ✅ `.gitignore` überarbeitet: `scripts/`, `Doku/PPT/`, `.devcontainer/` (ungenutzte Codespaces-Konfiguration) und weitere lokale Arbeitsdateien vollständig von der Versionierung ausgeschlossen
- ✅ `Dashboard/` (`streamlit_dashboard.py`, `dashboard_utils.py`) zeigt durchgehend die aktuellen Kennzahlen — u. a. Trägerschafts-Tab (ANOVA nicht signifikant), Feature Importance, Risiko-Rechner-Richtung (mehr Ärzte/Bett → höheres Risiko). Dabei zwei unabhängige Bugs gefunden und behoben: fehlendes `statsmodels` (Streudiagramm-Trendlinien crashten) und veraltetes `Styler.applymap` (Ähnliche-Häuser-Suche crashte). Alle 4 Seiten inkl. Kern-Interaktionen per `streamlit.testing.v1.AppTest` verifiziert (keine Exceptions)
- ✅ *(2026-08-27/28)* Grafiken durchgehend `g`+Nummer benannt (u. a. Decision-Tree-Grafiken, Bundesland-Kachelkarte statt Balken), `01_Exploration_Ref` als Konkordanzanalyse-Referenz ergänzt, indikator-/hausgewichtete Gesamtquote (7,71 % / 8,62 %) in `02_Analyse.md`/`.ipynb` nachgerechnet und dokumentiert
- ✅ *(2026-08-28)* D50/S90-Codes zählen durchgehend als auffällig (`01_Exploration.md`, `01_Exploration.ipynb`, `Fragen_und_Antworten.md`) — bestätigt durch eine Summenprobe H+U+A+D+S gegen die offizielle IQTIG-Zahl. `Doku/MD/IQTIG.md` neu: Auswertung des offiziellen IQTIG-Bundesqualitätsberichts 2023. `Doku/PPT/Projektbegleitende_Praesentation.pptx` erstmals eingecheckt (gezielte `.gitignore`-Ausnahme)
- ✅ *(2026-08-29/30)* Dashboard-Fix: veraltetes `px.scatter_mapbox` (brach auf Streamlit Cloud, lokal unauffällig) durch das aktiv gepflegte `px.scatter_map` ersetzt; Bundesland-Vergleich von abgeschnittenem Balkendiagramm auf interaktive Kachelkarte mit Hover-Tooltips umgestellt
- ✅ *(2026-08-30)* Abschließender Doku-Audit: `05_Dashboard.md`, `Workflow.md` und `README.md` auf aktuelle Seitennamen/Technik (`scatter_map`, Kachelkarte) gebracht. Dieselbe D50/S90-Anpassung wie 2026-08-28 auch im `Doku/Dozent/Fortschrittsbericht_...`-Generator vorgenommen. Für `Dashboard_Uebersicht.docx` und `ML_Doku.docx` fehlten die Generator-Skripte komplett (vermutlich mit `Doku/PPT/Designs/` verloren gegangen) — `scripts/erstelle_dashboard_doku.py` und `scripts/erstelle_ml_doku.py` neu geschrieben und beide docx mit aktuellen Kennzahlen neu erzeugt (u. a. Median 5,88 % statt 77 %, Accuracy 57,0 % statt 63,6 %, Feature Importance Ärzte/Bett 72,8 % statt 53,6 %, 1.821 statt 1.824 Häuser)
- ✅ *(2026-08-30)* `Aufgabenstellung/Fragestellung.docx` per `.gitignore`-Ausnahme eingecheckt (Ordner war zuvor komplett ausgeschlossen). Zusätzlich `use_container_width` (11 Stellen in `Dashboard/streamlit_dashboard.py`) proaktiv auf `width="stretch"` umgestellt — Streamlit hatte das Entfernungsdatum (2025-12-31) bereits überschritten und `requirements.txt` pinnt Streamlit nicht, dasselbe Risikomuster wie beim `scatter_mapbox`-Vorfall. Alle 4 Seiten inkl. Reset-/Such-/Vorhersage-Button-Interaktionen erneut per `AppTest` verifiziert (keine Exceptions, keine Deprecation-Warnungen mehr)
- ✅ *(2026-08-30)* `Projektbegleitende_Praesentation.pptx` Folien 15–43 visuell überarbeitet: Aufzählungen durch farbige Befund-Panels, nummerierte Karten und gerahmte Fazit-Boxen ersetzt (neue Hilfsfunktionen `panel_reihe`, `karten_reihe`, `rahmen_box` in `erstelle_projektbegleitende_ppt.py`). Grafiken mit schmalem/quadratischem/Hochformat-Seitenverhältnis (u. a. Folie 18 Bundesland-Kachelkarte, Korrelationsmatrix, Confusion Matrix, Dashboard-Screenshots) wirkten im Bild-oben/Panels-unten-Layout zu klein — dafür neues Layout `bild_folie_seitlich()`: Bild groß links über die volle Inhaltshöhe, Panels gestapelt rechts. Breite Grafiken (Boxplot-Paar, Entscheidungsbaum) blieben bewusst im alten Bild-oben-Layout, da dort bereits breiter dargestellt
- ✅ *(2026-08-30)* `grafiken/screenshots/` (4 Dateien, zeigten seit 2026-08-09 veraltete Kennzahlen) per Playwright gegen das lokal gestartete Dashboard neu aufgenommen — inkl. Klick auf „Suchen“/„Ergebnis anzeigen“, damit die Screenshots echte Ergebnisse statt Platzhalter zeigen. `Projektbegleitende_Praesentation.pptx` mit den neuen Screenshots neu erzeugt (Folien 37–40)
- ✅ *(2026-08-30)* `Doku/Dozent/` (Fortschrittsbericht für die Dozenten-Zwischenpräsentation, Woche-4-Stand) auf Wunsch komplett entfernt — Referenzen darauf in `README.md`, `Doku/MD/Workflow.md`, `Doku/MD/Fragen_und_Antworten.md` und dieser Datei bereinigt. Der Generator `scripts/erstelle_dozenten_doku.py` bleibt unangetastet in `scripts/` (gitignored, nicht Teil der Löschung)
- ✅ *(2026-08-30)* `Projektbegleitende_Praesentation.pptx` von 43 auf 35 Folien verdichtet (8 Folienpaare zusammengelegt, jeweils inkl. neu verfasster, zusammenhängender Sprechernotiz): 1.4a+b Herkunft/Anzahl der Häuser, 2.2c+d Filterkaskade/Ergebnis, 3.1 Grafik 9+10 Konzernvergleich/Fortbildungsquote, 3.4+3.5 Inferenzstatistik/Pivot-Tabelle, 4.2 Datenaufbereitung/Split/Basislinie, 4.3 Metriken/Confusion Matrix, 4.5+4.6 R²-Metrik/Modell speichern, 6.2+6.3 Grenzen der Analyse/Ausblick. Alle 35 Folien per Skript verifiziert (Sprechernotizen vollständig) und die 8 zusammengelegten Folien einzeln als PNG gerendert und auf Textüberlauf geprüft — dabei zwei Layout-Fehler gefunden und behoben: zu knapp bemessene Tabellenhöhe (Folie „4.2", überlappte mit der Kachel-Reihe darunter) und zu enger Abstand zwischen Zwischenüberschrift und Kartenreihe (Folie „6.2+6.3")

---

## 🔑 Wichtige Entscheidungen

| Entscheidung | Begründung |
|--------------|------------|
| **Median als Grenzwert** für Ziel-Variable | Robust gegenüber Ausreißern, teilt Häuser in zwei etwa gleich große Gruppen (49,7 % vs. 50,3 %) |
| **`QSErgBewStrukDialog`** als Bewertungsspalte | Offizieller Bewertungscode des Strukturierten Dialogs — einziger objektiver, vergleichbarer Indikator |
| **R10 = nicht auffällig, alle N\*-Codes ausschließen** | Laut offiziellem IQTIG-Bericht bedeutet R10 „im Referenzbereich"; N01/N02/N99 bedeuten „nicht bewertet" — Grundlage der zentralen Ziel-Variable des gesamten Projekts |
| **Deduplizierung über `(SO.QBID, QSQI.Indikator)`** | `QSQI.AEKey` ist Haus-ID, kein Indikator-Schlüssel — Fehler hätte zu 1 Zeile/Haus statt ~55 geführt |
| **`aerzte_pro_bett` als wichtigstes Merkmal** | Vom Decision Tree gelernt: Feature Importance 72,8 %, T-Test bestätigt (p < 0,0001) |
| **`max_depth=3` beim Decision Tree** | Bewusst einfach: erklärbarer Baum, verhindert Overfitting |
| **R² negativ (−0,007)** | Valides Ergebnis — die Strukturmerkmale erklären die stetige Auffälligkeitsquote linear nicht besser als der reine Durchschnittswert |
| **NaN bei `aerzte_pro_bett` nicht auffüllen** | 4 von 5 fehlenden Werten sind Tageskliniken mit 0 Betten — NaN ist korrekt ("nicht anwendbar") |
| **`SO.Standortnummer` statt `SO.QBID` für Konzern-Join** | `Konzern.csv` nutzt `SO.Standortnummer` als Schlüssel — ursprünglicher Code verglich versehentlich gegen `SO.QBID` (0 Treffer), korrigiert |
| **`ist_konzern` trotz fehlendem Signal ins Modell aufgenommen** | Chi²-Test zeigt keinen Zusammenhang (p=0,2585), Decision Tree bestätigt mit 0 % Feature Importance. Bewusst drin gelassen: „Kein Zusammenhang" ist selbst ein dokumentiertes, vom Modell empirisch bestätigtes Ergebnis |
| **`pflege_pro_bett` über `SO.Personalliste.csv` statt `AQ.Pflege.csv`** | `AQ.Pflege.csv` enthält nur Qualifikationsnachweise, keine Personal-Anzahlen. `SO.Personalliste.csv` hat direkt `SO.QBID` + `SO.Personal.Anzahl` mit Bereich `'Pflege'` |
| **Erweiterungs-Merkmale aus Notebook 04 (noch) nicht ins Hauptmodell übernommen** | Bewusst als separate Explorationsanalyse dokumentiert statt spontan ins laufende Modell gemergt — Übernahme würde `01_Exploration.ipynb`, `analysetabelle.csv` und das trainierte Modell neu durchlaufen lassen und ist als expliziter Folgeschritt vorgesehen |
| **`scripts/` nicht versioniert, `Doku/PPT/` größtenteils nicht** | Lokale Arbeitswerkzeuge bzw. Präsentationsunterlagen; die daraus erzeugten `.docx`-Ergebnisse (in `Doku/Word/`) sind versioniert, die Erzeuger-Skripte selbst nicht. Ausnahme seit 2026-08-28: `Projektbegleitende_Praesentation.pptx` wird gezielt eingecheckt, das Teamvortrag-Deck bleibt lokal |
| **D50/S90-Codes zählen als auffällig** | Bestätigt durch eine Summenprobe: H+U+A+D+S ergibt exakt die offizielle IQTIG-Zahl. Der Code (`~str.startswith('R')` nach N*-Ausschluss) setzt das direkt um |
| **`px.scatter_map` statt `px.scatter_mapbox`** *(2026-08-29)* | `scatter_mapbox` ist bei Plotly offiziell veraltet; unpinnte `plotly>=5.18.0`-Version in `requirements.txt` ließ Streamlit Cloud eine neuere, mit dem kaum noch gepflegten Mapbox-Codepfad inkompatible Version installieren — lokal unauffällig, auf Cloud AttributeError |
| **Bundesland-Vergleich als Kachelkarte statt Balkendiagramm** *(2026-08-29)* | Balken hatten abgeschnittene Beschriftungen bei langen Balken und stellten kleine Bundesländer (z. B. Bremen n=14) optisch gleichwertig zu großen (NRW n=397) dar — dieselbe schematische Deutschlandkarte wie `grafiken/g7_bundesland_kachelkarte.png`, jetzt interaktiv mit Hover-Tooltip |
| **Fehlende Generator-Skripte neu geschrieben statt `.docx` direkt gepatcht** *(2026-08-30)* | `Dashboard_Uebersicht.docx` und `ML_Doku.docx` hatten keine zugehörigen Skripte mehr in `scripts/` (vermutlich zusammen mit `Doku/PPT/Designs/` verloren gegangen) und enthielten veraltete Kennzahlen. Bewusst `erstelle_dashboard_doku.py`/`erstelle_ml_doku.py` neu geschrieben statt nur die `.docx` zu patchen, damit beide Dateien wie alle anderen Word-Dokumente reproduzierbar aus Quelldaten neu erzeugbar bleiben |
| **`use_container_width` proaktiv auf `width="stretch"` umgestellt** *(2026-08-30)* | Streamlit-Entfernungsdatum für `use_container_width` (2025-12-31) lag bereits in der Vergangenheit, `requirements.txt` pinnt Streamlit nicht — dasselbe Risikomuster, das den `scatter_mapbox`-Vorfall auf Streamlit Cloud verursacht hat. Vorsorglich behoben statt auf den nächsten Cloud-Crash zu warten |

---

*Datenbasis: IQTIG Qualitätsberichte 2023 | Projekt: Qualitäts-Muster-Finder | Diese Übersicht aktualisiert: 2026-08-30*
