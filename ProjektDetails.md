# 📁 Projektstruktur — QualitaetsMusterFinderProjekt

> **Projektfrage:** Welche Krankenhausmerkmale hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme aufweist?
>
> **Datenbasis:** IQTIG Qualitätsberichte 2023 — 1.824 deutsche Krankenhäuser

---

## 🏗️ Aufbau nach Bausteinen

Das Projekt folgt einer **5-Baustein-Struktur**:

| Baustein | Status | Hauptdatei |
|----------|--------|------------|
| 1 — Daten vorbereiten | ✅ Abgeschlossen | `Notebooks/01_Exploration.ipynb` |
| 2 — Deskriptive Analyse | ✅ Abgeschlossen | `Notebooks/02_Analyse.ipynb` |
| 3 — Streamlit-Dashboard | ✅ Live | `Dashboard/streamlit_dashboard.py` |
| 4 — Entscheidungsbaum (Bonus) | ✅ Abgeschlossen | `Notebooks/03_Decision_Tree.ipynb` |
| 5 — Abschluss & Präsentation | ⬜ Offen | — |

---

## 🏗️ Projektstruktur (finale Version)

```
QualitaetsMusterFinderProjekt/
│
├── 📒 Notebooks/ (3) — Datenanalyse & ML
│   ├── 01_Exploration.ipynb      → Datenaufbereitung (86 CSVs → analysetabelle.csv)
│   ├── 02_Analyse.ipynb          → Deskriptive Analyse (10 Grafiken, T-Test, ANOVA)
│   └── 03_Decision_Tree.ipynb    → ML: Decision Tree, Feature Importance
│
├── 🖥️ Dashboard/ — Streamlit-App (2)
│   ├── streamlit_dashboard.py    → Haupt-App: 4 Seiten (Übersicht, Vergleiche, Ähnliche Häuser, Risiko-Rechner)
│   └── dashboard_utils.py        → Hilfsfunktionen: Daten laden, KPIs, Plots, Modell-Vorhersage (importiert modell_klasse aus scripts/ via sys.path)
│
├── 🐍 scripts/ — Python-Module (7)
│   ├── modell_klasse.py          → OOP-Wrapper KrankenhausModell (prepare, fit, evaluate, save, load)
│   ├── bi_datenanalyse.py        → Generiert Word-Dokument: BI-Tool-Vergleich
│   ├── datei_uebersicht_a4.py    → Generiert Word-Dokument: Datei-Klassifikation (A4)
│   ├── grafiken_speichern.py     → (intern, gitignored) Grafiken aus analysetabelle.csv als PNG
│   ├── doku_generieren.py        → (intern, gitignored) Word-Doku-Generator
│   ├── powerbi_anleitung.py      → (intern, gitignored) Erzeugt PowerBI-Anleitungs-docx — ⚠️ enthält hartkodierten os.chdir()-Pfad eines anderen Rechners, vor Nutzung prüfen
│   └── word_dokumentation.py     → Erzeugt Dokumentation_Qualitaets_Muster_Finder.docx aus analysetabelle.csv
│
├── 📊 Daten (3) — liegen in Data/, per .gitignore-Ausnahme trotzdem im Repo
│   ├── Data/analysetabelle.csv        → Zentrale Analysetabelle (1.824 Häuser × 15+ Spalten)
│   ├── Data/analysetabelle.xlsx       → Excel-Version
│   └── Data/modell_krankenhaus.pkl    → Trainiertes Decision-Tree-Modell
│
├── 🖼️ grafiken/ — 12 PNG-Grafiken (⚠️ Duplikat: 9 der Dateien liegen zusätzlich unter Notebooks/grafiken/ — Altlast, sollte bereinigt werden)
│   ├── g1_auffaellig_quote.png   → Verteilung auffällig-Quote
│   ├── g2_bettenzahl.png         → Bettenzahl MIT vs. OHNE Probleme
│   ├── g3_traegerschaft.png      → Trägerschaft-Vergleich
│   ├── g4_uni.png                → Uni-Kliniken vs. normale Häuser
│   ├── g5_6_fortbildung_aerzte.png → Fortbildung & Ärzte/Bett
│   ├── g7_bundesland.png         → Anteil je Bundesland
│   ├── g8_korrelation.png        → Korrelationsmatrix
│   ├── g9_scatter_betten_aerzte.png → Scatter Betten vs. Ärzte/Bett
│   ├── g10_stoerfaktor_traeger.png → Störfaktor Träger × Bettengröße
│   ├── confusion_matrix.png      → Confusion Matrix
│   ├── decision_tree.png         → Entscheidungsbaum-Visualisierung
│   └── feature_importance.png    → Feature Importance
│
├── 📄 BI_Analyse/ — BI-Tool-Vergleich
│   ├── BI_Datenanalyse.docx
│   ├── Datei-Übersicht.docx
│   ├── PowerBI_Dashboard_Anleitung.docx
│   └── image (1-5).png
│
├── 📄 Dokumentation
│   ├── README.md                 → Hauptdokumentation mit Startanleitung
│   ├── ProjektDetails.md         → Detaillierte Projektstruktur & Entscheidungen
│   ├── ToDo.md                   → Aufgabenliste + IHK-Abgleich
│   ├── Doku/MD/                  → Markdown-Dokumentation
│   │   ├── Workflow.md           → Workflow-Dokumentation pro Baustein
│   │   ├── Daten_Inhaltsverzeichnis.md → Übersicht aller 86 CSV-Dateien
│   │   ├── Praesentation_Folien_Beschreibung.md
│   │   └── datensatz_bericht.py  → ⚠️ Python-Skript liegt hier statt in scripts/ — undokumentiert, gehört verschoben oder erklärt
│   └── Doku/Word/                → Word-Dokumentation
│       ├── Dokumentation_Qualitaets_Muster_Finder.docx
│       ├── Datensatz_Analyse_Bericht.docx
│       └── Datei_Uebersicht.docx
│
└── ⚙️ Konfiguration
    ├── .gitignore                → Schließt Data/ aus, außer analysetabelle.csv/.xlsx & modell_krankenhaus.pkl (per !-Ausnahme); schließt zusätzlich Aufgabenstellung/ und 4 interne Skripte aus
    └── requirements.txt          → 7 Pakete (streamlit, plotly, pandas, etc.)
```

---

## 📂 Datei-Übersicht

### 📒 Notebooks (3) — im Ordner `Notebooks/`

- `Notebooks/01_Exploration.ipynb` — Datenaufbereitung: 86 CSV-Dateien erkunden, Ziel-Variable bauen, Merkmale zusammenführen → `analysetabelle.csv`
- `Notebooks/02_Analyse.ipynb` — Deskriptive Analyse: 10 Grafiken, T-Test, ANOVA, Konfidenzintervalle, Korrelationen
- `Notebooks/03_Decision_Tree.ipynb` — ML: Decision Tree (max_depth=3), Metriken, R², Feature Importance, joblib

### 🖥️ Dashboard (2) — im Ordner `Dashboard/`

- `Dashboard/streamlit_dashboard.py` — Haupt-App mit 4 Seiten (Übersicht, Vergleiche, Ähnliche Häuser, Risiko-Rechner)
- `Dashboard/dashboard_utils.py` — Hilfsfunktionen: Daten laden, KPIs, Plots, Modell-Vorhersage (Trennung Logik/UI); lädt `Data/analysetabelle.csv` & `Data/modell_krankenhaus.pkl`; importiert `KrankenhausModell` aus `scripts/modell_klasse.py` (Pfad wird zur Laufzeit über `sys.path` ergänzt, da beide Ordner getrennt sind)

### 🐍 Python-Module (7) — im Ordner `scripts/`

- `scripts/modell_klasse.py` — OOP-Wrapper `KrankenhausModell` (prepare, fit, evaluate, save, load); Default-Modellpfad `Data/modell_krankenhaus.pkl`
- `scripts/bi_datenanalyse.py` — Generiert Word-Dokument: BI-Tool-Vergleich mit Kollegen
- `scripts/datei_uebersicht_a4.py` — Generiert Word-Dokument: Datei-Klassifikation (A4-Übersicht)
- `scripts/word_dokumentation.py` — Generiert `Dokumentation_Qualitaets_Muster_Finder.docx` aus `Data/analysetabelle.csv`
- `scripts/grafiken_speichern.py` — *(intern, per `.gitignore` ausgeschlossen)* erzeugt die 10 PNG-Grafiken aus `Data/analysetabelle.csv`
- `scripts/doku_generieren.py` — *(intern, per `.gitignore` ausgeschlossen)* Word-Doku-Generator, liest `Data/analysetabelle.csv`
- `scripts/powerbi_anleitung.py` — *(intern, per `.gitignore` ausgeschlossen)* PowerBI-Anleitungs-docx-Generator — ⚠️ enthält einen hartkodierten `os.chdir()`-Pfad eines fremden Rechners (`c:\Users\Admin\VSCode\...`), vor erneuter Nutzung anpassen

### 📊 Daten (3) — im Ordner `Data/`

- `Data/analysetabelle.csv` — Zentrale Analysetabelle: 1.824 Häuser × 15+ Spalten (Basis für alles)
- `Data/analysetabelle.xlsx` — Excel-Version derselben Tabelle
- `Data/modell_krankenhaus.pkl` — Trainiertes Decision-Tree-Modell (joblib)

> Diese 3 Dateien sind die einzigen Inhalte von `Data/`, die per `.gitignore`-Ausnahme (`!Data/...`) trotzdem versioniert werden — die 86 Rohdaten-CSVs/-Excels in `Data/CSV/` und `Data/Excel/` bleiben ausgeschlossen.

### 📄 Dokumentation (Markdown)

- `README.md` — Hauptdokumentation mit Startanleitung & "Wichtige Entscheidungen"
- `ProjektDetails.md` — Detaillierte Projektstruktur & Entscheidungen
- `ToDo.md` — Aufgabenliste mit Haken + IHK-Abgleich
- `Doku/MD/Workflow.md` — Vollständige Workflow-Dokumentation pro Baustein
- `Doku/MD/Daten_Inhaltsverzeichnis.md` — Übersicht aller 86 CSV-Dateien
- `Doku/MD/Praesentation_Folien_Beschreibung.md` — Präsentationsfolien-Beschreibung

### 📄 Dokumentation (Word)

- `Doku/Word/Dokumentation_Qualitaets_Muster_Finder.docx` — Hauptdokumentation
- `Doku/Word/Datensatz_Analyse_Bericht.docx` — Datensatz-Analyse (86 Dateien)
- `Doku/Word/Datei_Uebersicht.docx` — Datei-Übersicht (generiert)
- `BI_Analyse/` — BI-Analyse-Ordner mit Word-Dokumenten + 5 Bildern

### 🖼️ Grafiken (`grafiken/`)

12 PNG-Dateien:

- `g1_auffaellig_quote.png` — Verteilung der auffällig-Quote
- `g2_bettenzahl.png` — Bettenzahl MIT vs. OHNE Probleme
- `g3_traegerschaft.png` — Trägerschaft-Vergleich
- `g4_uni.png` — Uni-Kliniken vs. normale Häuser
- `g5_6_fortbildung_aerzte.png` — Fortbildungsquote & Ärzte/Bett
- `g7_bundesland.png` — Anteil je Bundesland
- `g8_korrelation.png` — Korrelationsmatrix
- `g9_scatter_betten_aerzte.png` — Scatter Bettenzahl vs. Ärzte/Bett
- `g10_stoerfaktor_traeger.png` — Störfaktor Träger × Bettengröße
- `confusion_matrix.png` — Confusion Matrix Decision Tree
- `decision_tree.png` — Visualisierung Entscheidungsbaum
- `feature_importance.png` — Feature Importance Balkendiagramm

### ⚙️ Konfiguration

- `.gitignore` — Schließt `Data/*` aus (Rohdaten, 86 CSVs/Excels bis 911 MB), außer `Data/analysetabelle.csv`, `Data/analysetabelle.xlsx`, `Data/modell_krankenhaus.pkl` (explizite `!`-Ausnahmen); schließt außerdem `Aufgabenstellung/` und 4 interne Skripte aus
- `requirements.txt` — 7 Pakete: streamlit, plotly, pandas, scikit-learn, joblib, scipy, numpy

---

## 🔗 Datenfluss

```
Rohdaten (Data/CSV, Data/Excel — 86 Dateien, nicht im Repo)
    ↓ Notebooks/01_Exploration.ipynb
Data/analysetabelle.csv (1.824 Häuser × 15+ Spalten)
    ↓                          ↓
Notebooks/02_Analyse.ipynb  Notebooks/03_Decision_Tree.ipynb
(Grafiken → grafiken/)    (modell_krankenhaus.pkl)
    ↓                          ↓
    └──────────┬───────────────┘
               ↓
    Dashboard/streamlit_dashboard.py (Live-Dashboard)
    ├── Dashboard/dashboard_utils.py (Logik)
    └── scripts/modell_klasse.py (Modell-Wrapper, ordnerübergreifend importiert)
```

---

## 🎯 Kern-Ergebnisse

| Kennzahl | Wert |
|----------|------|
| Häuser analysiert | 1.824 |
| Ø Indikatoren pro Haus | 54,7 |
| Median auffällig-Quote | **76,92 %** |
| Träger mit höchstem Anteil | Privat: **56,5 %** |
| Signifikantester Unterschied | Ärzte/Bett (T-Test p < 0,001) |
| Decision Tree Accuracy | **64,9 %** (Basislinie: 50,7 %) |
| R² (lineare Regression) | **0,023** — schwacher Zusammenhang |
| Wichtigster Prädiktor | `aerzte_pro_bett` (Feature Importance 71,3 %) |

> **Fazit:** Keine starken, eindeutigen Zusammenhänge zwischen Strukturmerkmalen und Qualitätsproblemen. Privathäuser und niedrige Ärztedichte zeigen Tendenzen — aber kein klares Muster. **Kein Zusammenhang ist ein valides Ergebnis.**

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
- `scripts/modell_klasse.py` — Decision Tree Klasse (wird von `dashboard_utils.py` ordnerübergreifend importiert)
- `Data/modell_krankenhaus.pkl` — Trainiertes Modell
- `Data/analysetabelle.csv` — Datenbasis (1.824 Häuser)
- `requirements.txt`
- `grafiken/` — PNG-Grafiken (optional)

> ⚠️ Die Rohdaten in `Data/CSV/` und `Data/Excel/` (86 Dateien, bis 911 MB) sind **nicht** im Repository. Für den Dashboard-Betrieb reichen `Data/analysetabelle.csv` und `Data/modell_krankenhaus.pkl` — diese beiden (plus `Data/analysetabelle.xlsx`) sind über eine `.gitignore`-Ausnahme trotzdem versioniert, obwohl sie im sonst ausgeschlossenen `Data/`-Ordner liegen.

---

## ⚠️ Offene Punkte (aus `ToDo.md`)

- **Baustein 5:** Robustheit testen, Code aufräumen, Präsentation vorbereiten
- `pflege_pro_bett` ist im Notebook vorbereitet, aber noch nicht final in der Analysetabelle verankert
- Entscheidungsbegründungen ausformulieren für Präsentation
- Komplett-Durchlauf testen: Rohdaten → `Notebooks/01_Exploration.ipynb` → `Data/analysetabelle.csv` → `Dashboard/streamlit_dashboard.py` *(2026-07-29: Pfad-Inkonsistenz behoben — Code las zuvor aus dem Projekt-Root, Dateien lagen aber in `Data/`; jetzt lesen `dashboard_utils.py`, `modell_klasse.py` & Doku-Generatoren konsistent aus `Data/`. Zusätzlich `streamlit_dashboard.py`/`dashboard_utils.py` von `scripts/` nach `Dashboard/` verschoben — `modell_klasse.py` bleibt in `scripts/`, Import läuft jetzt über `sys.path`-Ergänzung. End-to-End-Lauf noch nicht verifiziert.)*
- **Streamlit-Cloud-Deployment prüfen:** Die Live-App (qualitaets-muster-finder.streamlit.app) hat vermutlich `scripts/streamlit_dashboard.py` als Main-File-Pfad hinterlegt — dieser muss in den App-Settings auf `Dashboard/streamlit_dashboard.py` aktualisiert werden, sonst schlägt das nächste Deployment fehl
- `Notebooks/grafiken/` als Duplikat von `grafiken/` bereinigen (9 der 12 Dateien liegen doppelt)
- `Doku/MD/datensatz_bericht.py` einordnen — Skript liegt im Doku-Ordner, gehört fachlich zu `scripts/`
- `scripts/powerbi_anleitung.py` reparieren — hartkodierter `os.chdir()`-Pfad eines fremden Rechners

---

## 🔑 Wichtige Entscheidungen

| Entscheidung | Begründung |
|--------------|------------|
| **Median als Grenzwert** für Ziel-Variable | Robust gegenüber Ausreißern, teilt Häuser in zwei gleich große Gruppen (49 % vs. 51 %) |
| **`QSErgBewStrukDialog`** als Bewertungsspalte | Offizieller Bewertungscode des Strukturierten Dialogs — einziger objektiver, vergleichbarer Indikator |
| **N99 ausschließen** | `N99 = nicht bewertet` — würde Quote systematisch verfälschen. Nicht bewertet ≠ unauffällig |
| **Deduplizierung über `(SO.QBID, QSQI.Indikator)`** | `QSQI.AEKey` ist Haus-ID, kein Indikator-Schlüssel — Fehler hätte zu 1 Zeile/Haus statt ~55 geführt |
| **`aerzte_pro_bett` als wichtigstes Merkmal** | Vom Decision Tree gelernt: Feature Importance 71,3 %, T-Test bestätigt (p < 0,001) |
| **`max_depth=3` beim Decision Tree** | Bewusst einfach: erklärbarer Baum, verhindert Overfitting |
| **R² so niedrig (0,023)** | Valides Ergebnis — Strukturmerkmale erklären nur 2,3 % der Varianz |
| **NaN bei `aerzte_pro_bett` nicht auffüllen** | 4 von 5 fehlenden Werten sind Tageskliniken mit 0 Betten — NaN ist korrekt ("nicht anwendbar") |

---

*Datenbasis: IQTIG Qualitätsberichte 2023 | Projekt: Qualitäts-Muster-Finder*