# 📁 Projektstruktur — QualitaetsMusterFinderProjekt

> **Projektfrage:** Welche Krankenhausmerkmale hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme aufweist?
>
> **Datenbasis:** IQTIG Qualitätsberichte 2023 — 1.824 deutsche Krankenhäuser

---

## 🏗️ Aufbau nach Bausteinen

Das Projekt folgt einer **5-Baustein-Struktur** plus einem optionalen Erweiterungs-Notebook:

| Baustein | Status | Hauptdatei |
|----------|--------|------------|
| 1 — Daten vorbereiten | ✅ Abgeschlossen | `Notebooks/01_Exploration.ipynb` |
| 2 — Deskriptive Analyse | ✅ Abgeschlossen | `Notebooks/02_Analyse.ipynb` |
| 3 — Streamlit-Dashboard | ✅ Live | `Dashboard/streamlit_dashboard.py` |
| 4 — Entscheidungsbaum (Bonus) | ✅ Abgeschlossen | `Notebooks/03_Decision_Tree.ipynb` |
| 5 — Abschluss & Präsentation | 🟡 Unterlagen fertig, Vortrag noch offen | `Doku/PPT/`, `Doku/Dozent/` |
| Bonus — Potenzielle Erweiterungen | ✅ Analysiert, **nicht ins Hauptmodell übernommen** | `Notebooks/04_Potenzielle_Erweiterungen.ipynb` |

---

## 🏗️ Projektstruktur (aktueller Stand — 2026-08-10)

```
QualitaetsMusterFinderProjekt/
│
├── 📒 Notebooks/ (4) — Datenanalyse & ML
│   ├── 01_Exploration.ipynb              → Datenaufbereitung (86 CSVs → Data/analysetabelle.csv)
│   ├── 02_Analyse.ipynb                  → Deskriptive Analyse (12 Grafiken, T-Test, Chi²-Test, ANOVA)
│   ├── 03_Decision_Tree.ipynb            → ML: Decision Tree, Feature Importance (importiert KrankenhausModell aus model/)
│   └── 04_Potenzielle_Erweiterungen.ipynb → NEU: prüft 3 bisher ungenutzte CSVs auf zusätzliches Signal (siehe Kern-Ergebnisse)
│
├── 🖥️ Dashboard/ — Streamlit-App (2)
│   ├── streamlit_dashboard.py    → Haupt-App: 4 Seiten (Übersicht, Vergleiche, Ähnliche Häuser, Risiko-Rechner)
│   └── dashboard_utils.py        → Hilfsfunktionen: Daten laden, KPIs, Plots, Modell-Vorhersage (importiert modell_klasse aus model/ via sys.path)
│
├── 🧠 model/ — Modell-Logik (1)
│   └── modell_klasse.py          → OOP-Wrapper KrankenhausModell (prepare, fit, evaluate, save, load)
│
├── 🐍 scripts/ — Python-Module (6, 2026-08-10 auf Kleinschreibung umbenannt & Duplikate bereinigt)
│   ├── projekt_doku.py                 → Generiert Doku/Word/Dokumentation_Qualitaets_Muster_Finder.docx (Hauptdokumentation)
│   ├── grafiken_doku.py                → Generiert Doku/Word/Grafiken_Dokumentation.docx: erklärt alle 12 Grafiken aus 02_Analyse.ipynb
│   ├── datensatz_uebersicht.py         → Generiert Doku/Word/Datensatz_Uebersicht.docx: Datei-Klassifikation aller 86 Rohdaten-CSVs
│   ├── analysetabelle_zusammenfassung.py → Generiert Doku/Word/Analysetabelle_Zusammenfassung.docx: Merkmale, Ziel-Variable, Quelltabellen, Merge-Kriterien, Endgröße (live berechnet)
│   ├── erstelle_dozenten_doku.py       → Generiert Doku/Dozent/Fortschrittsbericht_Qualitaets_Muster_Finder.docx (max. 10 Seiten, Bausteine 1 & 2)
│   └── erstelle_praesentationsskript.py → Generiert Praesentationsskript_Qualitaets_Muster_Finder.docx (30-Min-Sprechertext, 15 Folien)
│
├── 📊 Daten (3) — liegen in Data/, per .gitignore-Ausnahme trotzdem im Repo
│   ├── Data/analysetabelle.csv        → Zentrale Analysetabelle (1.824 Häuser × 18 Spalten)
│   ├── Data/analysetabelle.xlsx       → Excel-Version
│   └── Data/modell_krankenhaus.pkl    → Trainiertes Decision-Tree-Modell
│
├── 🖼️ grafiken/ — 14 PNG-Grafiken + Dashboard-Screenshots
│   ├── g1_auffaellig_quote.png … g12_konzern_vergleich.png, confusion_matrix.png, decision_tree.png, feature_importance.png
│   └── screenshots/ → NEU: 4 Dashboard-Screenshots (einflussfaktoren, gesamtuberblick, haeuser_vergleichen, qualitaets_vorhersage.png) — für Präsentationsunterlagen
│
├── 📄 BI_Analyse/ — Team-Material (Kollegen-Beiträge, Power BI)
│   ├── BI_Datenanalyse.docx, Datei-Übersicht.docx  → ältere, weiterhin versionierte Dokumente
│   ├── QS.Qualitätsindikator.docx  → Word-Fassung von Doku/MD/Qualitätsindikator.md
│   ├── datenfluss_schema.png       → Datenfluss-Diagramm
│   └── image (1–5).png             → Power-BI-Dashboard-Screenshots der Kollegen
│
├── 📄 Dokumentation
│   ├── README.md                 → Hauptdokumentation mit Startanleitung
│   ├── ProjektDetails.md         → Detaillierte Projektstruktur & Entscheidungen (dieses Dokument)
│   ├── ToDo.md                   → Aufgabenliste + IHK-Abgleich
│   ├── Doku/MD/                  → Markdown-Dokumentation (10 Dateien)
│   │   ├── Workflow.md, 01_Exploration.md, 02_Analyse.md, 03_Decision_Tree.md
│   │   ├── 04_Potenzielle_Erweiterungen.md → NEU: Walkthrough zum Bonus-Notebook
│   │   ├── Dashboard.md                    → NEU: Doku zur Dashboard-Bedienung/Layout
│   │   ├── Daten_Inhaltsverzeichnis.md     → Übersicht aller 86 CSV-Dateien
│   │   ├── Qualitätsindikator.md           → NEU: Deep-Dive zur größten Rohdatei (QS.Qualitätsindikator.csv, 911,7 MB)
│   │   ├── Praesentation_Folien_Beschreibung.md      → Folienbeschreibung Einzelvortrag (15 Folien)
│   │   └── Praesentation_Team_Folien_Beschreibung.md → NEU: alternatives Konzept für 3er-Team-Vortrag (Power BI + Streamlit gemischt)
│   ├── Doku/Word/ (7 Dateien)     → Word-Exporte, siehe Datei-Übersicht unten
│   ├── Doku/PPT/                 → NEU: finale Präsentationsunterlagen (2 PPTX + Sprechertext-docx)
│   ├── Doku/PPT.zip              → NEU: Backup-Archiv von Doku/PPT/
│   └── Doku/Dozent/              → NEU: Fortschrittsbericht + Sprechertext für die Dozenten-Zwischenpräsentation
│
└── ⚙️ Konfiguration
    ├── .gitignore                → Schließt Data/ aus, außer analysetabelle.csv/.xlsx & modell_krankenhaus.pkl (per !-Ausnahme); schließt zusätzlich Aufgabenstellung/ aus
    ├── .devcontainer/devcontainer.json → ⚠️ verweist noch auf veralteten Pfad `streamlit_dashboard.py` statt `Dashboard/streamlit_dashboard.py`
    ├── requirements.txt          → 11 Pakete (streamlit, plotly, nbformat, ipykernel, pandas, scikit-learn, joblib, scipy, numpy, matplotlib, seaborn)
    └── .venv/                    → NEU (2026-08-11): projekteigene virtuelle Umgebung + Jupyter-Kernel „Qualitaets-Muster-Finder (.venv)", per .gitignore ausgeschlossen
```

---

## 📂 Datei-Übersicht

### 📒 Notebooks (4) — im Ordner `Notebooks/`

- `Notebooks/01_Exploration.ipynb` — Datenaufbereitung: 86 CSV-Dateien erkunden, Ziel-Variable bauen, Merkmale zusammenführen → `Data/analysetabelle.csv`
- `Notebooks/02_Analyse.ipynb` — Deskriptive Analyse: 12 Grafiken, T-Test, Chi²-Test, ANOVA, Konfidenzintervalle, Korrelationen
- `Notebooks/03_Decision_Tree.ipynb` — ML: Decision Tree (max_depth=3), Metriken, R², Feature Importance, joblib
- `Notebooks/04_Potenzielle_Erweiterungen.ipynb` — **NEU:** Prüft 3 der bisher ungenutzten 79 CSV-Dateien (`QS.Leistungsbereich.csv`, `Notfallversorgung.csv`, `MM.csv`) auf zusätzliches Erklärungssignal für `hat_viele_Probleme`. Ergebnis: zwei empfohlene, aber **noch nicht integrierte** Merkmale (siehe Kern-Ergebnisse)

### 🖥️ Dashboard (2) — im Ordner `Dashboard/`

- `Dashboard/streamlit_dashboard.py` — Haupt-App mit 4 Seiten (Übersicht, Vergleiche, Ähnliche Häuser, Risiko-Rechner)
- `Dashboard/dashboard_utils.py` — Hilfsfunktionen: Daten laden, KPIs, Plots, Modell-Vorhersage (Trennung Logik/UI); lädt `Data/analysetabelle.csv` & `Data/modell_krankenhaus.pkl`; importiert `KrankenhausModell` aus `model/modell_klasse.py` (Pfad wird zur Laufzeit über `sys.path` ergänzt, da beide Ordner getrennt sind)

### 🧠 Modell-Logik (1) — im Ordner `model/`

- `model/modell_klasse.py` — OOP-Wrapper `KrankenhausModell` (prepare, fit, evaluate, save, load); Default-Modellpfad `Data/modell_krankenhaus.pkl`. Einzige Quelle der Wahrheit für Features & Modell-Logik — wird von `Dashboard/dashboard_utils.py` und `Notebooks/03_Decision_Tree.ipynb` ordnerübergreifend importiert (`sys.path`-Ergänzung, kein echtes Python-Package)

### 🐍 Python-Module (6) — im Ordner `scripts/`

> **2026-08-10:** Alle Dateien in diesem Ordner wurden auf durchgängige Kleinschreibung umbenannt. Zwei Duplikate wurden identifiziert und entfernt: `grafiken_dokumentation.py` (byteidentisch mit `grafiken_doku.py`) und `doku_generieren.py` (veraltete Vorversion von `projekt_doku.py`, schrieb an falschen Pfad). Zusätzlich wurde der `OUT_PATH` in `analysetabelle_zusammenfassung.py` von Projekt-Root auf `Doku/Word/` korrigiert (Pfad-Drift zum tatsächlichen Ablageort der Datei behoben).

- `scripts/projekt_doku.py` — Generiert `Doku/Word/Dokumentation_Qualitaets_Muster_Finder.docx` aus `Data/analysetabelle.csv` (Hauptdokumentation, korrekter Zielpfad)
- `scripts/grafiken_doku.py` — Generiert `Doku/Word/Grafiken_Dokumentation.docx`: erklärt alle 12 Grafiken aus `02_Analyse.ipynb`, Zahlen live berechnet
- `scripts/datensatz_uebersicht.py` — Generiert `Doku/Word/Datensatz_Uebersicht.docx`: kompakte Klassifikation, welche der 86 Rohdaten-Dateien verwendet wurden, welche nicht, welche „vielleicht"
- `scripts/analysetabelle_zusammenfassung.py` — Generiert `Doku/Word/Analysetabelle_Zusammenfassung.docx`: welche Merkmale/Ziel-Variable(n) aus welchen Quelltabellen, Merge-Kriterien (Left Join, Schlüssel je Tabelle), Endgröße — live berechnet, keine hartkodierten Zahlen
- `scripts/erstelle_dozenten_doku.py` — Generiert `Doku/Dozent/Fortschrittsbericht_Qualitaets_Muster_Finder.docx` (max. 10 Seiten, Bausteine 1 & 2, für Zwischenpräsentation bei den Dozent:innen). Am 2026-08-11 an manuelle Word-Anpassungen angeglichen (Abschnitte „1.3 Verwendete Python-Bibliotheken" und „4 Projektstruktur & Reproduzierbarkeit" entfernt, ein Satz unter 1.1 gestrichen) — Skript und Datei sind wieder deckungsgleich, verifiziert per automatisiertem Absatz-für-Absatz-Vergleich (0 Unterschiede)
- `scripts/erstelle_praesentationsskript.py` — Generiert das vollständige Sprechertext-Dokument (30 Min, 15 Folien, erzählend mit Übergängen)

> **Hinweis (2026-08-10):** Im Zuge dieser Analyse wurden außerdem `Doku/MD/datensatz_bericht.py` (Alt-Leiche im Doku-Ordner), `scripts/word_dokumentation.py`, `scripts/insert_folie_datensatz.py`, `scripts/insert_folie_quelldateien.py`, `scripts/update_folie13.py`, `scripts/powerbi_anleitung.py`, `scripts/grafiken_speichern.py` und `scripts/datensatz_bericht.py` sowie `Dashboard/folie13_praesentation.py` gelöscht (nicht mehr im Arbeitsverzeichnis vorhanden) — offenbar ein manuelles Aufräumen abgeschlossener Einmal-Skripte (Folien-Editoren, PNG-Export-Skript) parallel zu dieser Analyse.

### 📊 Daten (3) — im Ordner `Data/`

- `Data/analysetabelle.csv` — Zentrale Analysetabelle: 1.824 Häuser × 18 Spalten (Basis für alles), unverändert seit 2026-07-29
- `Data/analysetabelle.xlsx` — Excel-Version derselben Tabelle
- `Data/modell_krankenhaus.pkl` — Trainiertes Decision-Tree-Modell (joblib)

> Diese 3 Dateien sind die einzigen Inhalte von `Data/`, die per `.gitignore`-Ausnahme (`!Data/...`) trotzdem versioniert werden — die Rohdaten-CSVs/-Excels in `Data/CSV/` und `Data/Excel/` bleiben ausgeschlossen.

### 📄 Dokumentation (Markdown)

- `README.md` — Hauptdokumentation mit Startanleitung & "Wichtige Entscheidungen"
- `ProjektDetails.md` — Detaillierte Projektstruktur & Entscheidungen (dieses Dokument)
- `ToDo.md` — Aufgabenliste mit Haken + IHK-Abgleich
- `Doku/MD/Workflow.md` — Vollständige Workflow-Dokumentation pro Baustein
- `Doku/MD/01_Exploration.md` — Schritt-für-Schritt-Erklärung von `01_Exploration.ipynb`
- `Doku/MD/02_Analyse.md` — Schritt-für-Schritt-Erklärung von `02_Analyse.ipynb`
- `Doku/MD/03_Decision_Tree.md` — Schritt-für-Schritt-Erklärung von `03_Decision_Tree.ipynb` (2026-08-10 erweitert)
- `Doku/MD/04_Potenzielle_Erweiterungen.md` — **NEU:** Walkthrough zu `04_Potenzielle_Erweiterungen.ipynb` inkl. Hypothesen, Ergebnissen und Empfehlungen je geprüfter Datei
- `Doku/MD/Dashboard.md` — **NEU:** Doku zu Aufbau, Navigation und Seiten des Streamlit-Dashboards
- `Doku/MD/Daten_Inhaltsverzeichnis.md` — Übersicht aller 86 CSV-Dateien
- `Doku/MD/Qualitätsindikator.md` — **NEU:** Deep-Dive zu `QS.Qualitätsindikator.csv` (911,7 MB, größte Rohdatei, 29 Spalten)
- `Doku/MD/Praesentation_Folien_Beschreibung.md` — Folienbeschreibung für den Einzelvortrag (15 Folien, 30 Min), 2026-08-10 überarbeitet
- `Doku/MD/Praesentation_Team_Folien_Beschreibung.md` — **NEU:** Alternatives Präsentationskonzept zu dritt (Kollege E: Python/Streamlit, Kollege A & M: Power BI), ebenfalls 15 Folien/30 Min

### 📄 Dokumentation (Word)

- `Doku/Word/Dokumentation_Qualitaets_Muster_Finder.docx` — Hauptdokumentation (generiert von `projekt_doku.py`)
- `Doku/Word/Datensatz_Uebersicht.docx` — Datei-Klassifikation aller 86 Rohdaten (generiert von `datensatz_uebersicht.py`)
- `Doku/Word/Grafiken_Dokumentation.docx` — Erklärung aller 12 Analyse-Grafiken (generiert von `grafiken_doku.py`)
- `Doku/Word/Analysetabelle_Zusammenfassung.docx` — Merkmale, Ziel-Variable, Quelltabellen, Merge-Kriterien, Endgröße (generiert)
- `Doku/Word/Dashboard_Uebersicht.docx` — **NEU:** Word-Fassung von `Doku/MD/Dashboard.md`
- `Doku/Word/ML_Doku.docx` — **NEU:** Word-Fassung des Decision-Tree-Walkthroughs
- `Doku/Word/Praesentation_Folienvorschlag.docx` — **NEU:** Foliengliederungs-Vorschlag (30 Min, 15 Folien)

> ⚠️ Für `Dashboard_Uebersicht.docx`, `ML_Doku.docx` und `Praesentation_Folienvorschlag.docx` existiert **kein** Generator-Skript mehr im aktuellen `scripts/`-Ordner (Metadaten bestätigen `python-docx`-Erzeugung). Vermutlich wurden die erzeugenden Skripte im Rahmen einer früheren Aufräumaktion gelöscht, ohne die Ausgabedateien zu entfernen — die drei Dateien sind inhaltlich weiterhin aktuell, aber nicht mehr reproduzierbar.

### 📄 Doku/PPT/, Doku/PPT.zip, Doku/Dozent/ — Präsentationsunterlagen (NEU)

- `Doku/PPT/Qualitaets_Muster_Finder.pptx` — Finale PPTX für den Einzelvortrag (15 Folien, Folie 13 am 2026-08-09 von Power BI auf Streamlit-Dashboard umgestellt)
- `Doku/PPT/Qualitaets_Muster_Finder_Teamvortrag.pptx` — Alternative PPTX für den 3er-Team-Vortrag
- `Doku/PPT/Praesentationsskript_Qualitaets_Muster_Finder.docx` — Vollständiger Sprechertext (generiert von `erstelle_praesentationsskript.py`)
- `Doku/PPT.zip` — Backup-Archiv der beiden PPTX-Dateien
- `Doku/Dozent/Fortschrittsbericht_Qualitaets_Muster_Finder.docx` — Zwischenbericht für die Dozent:innen (max. 10 Seiten, generiert von `erstelle_dozenten_doku.py`). Am 2026-08-11 manuell in Word angepasst (zwei Abschnitte gekürzt); das Skript wurde daraufhin synchronisiert und erzeugt wieder exakt diesen Stand — ein erneuter Lauf ist damit wieder gefahrlos möglich
- `Doku/Dozent/Sprechertext_Dozentenpraesentation.txt` — Sprechertext für die Dozenten-Zwischenpräsentation (Anfang Woche 3)

> Es existieren also **zwei parallele Präsentationskonzepte**: ein Einzelvortrag (Python/Streamlit-fokussiert, `Praesentation_Folien_Beschreibung.md`) und ein Team-Vortrag zu dritt, bei dem zwei Kollegen den Power-BI-Teil beisteuern (`Praesentation_Team_Folien_Beschreibung.md`, Material dazu in `BI_Analyse/`). `ToDo.md` bezeichnet das Projekt weiterhin als „Soloprojekt — angepasst"; welches der beiden Konzepte final verwendet wird, ist in den Dokumenten nicht explizit festgelegt.

### 🖼️ Grafiken (`grafiken/`)

14 PNG-Dateien wie zuvor (siehe Kern-Ergebnisse unten für Details) plus:

- `grafiken/screenshots/` — **NEU:** 4 Dashboard-Screenshots (`einflussfaktoren.png`, `gesamtuberblick.png`, `haeuser_vergleichen.png`, `qualitaets_vorhersage.png`) für die Präsentationsunterlagen

### 📄 BI_Analyse/ — Team-Material

Enthält heute anderen Inhalt als in einer früheren Version dieses Dokuments beschrieben (die ursprünglich hier verorteten Generator-Skripte `bi_datenanalyse.py` und `datei_uebersicht.py` wurden per Commit entfernt). Aktueller Inhalt: `BI_Datenanalyse.docx`, `Datei-Übersicht.docx`, `QS.Qualitätsindikator.docx` (Word-Fassung von `Doku/MD/Qualitätsindikator.md`), `datenfluss_schema.png` sowie 5 Power-BI-Dashboard-Screenshots der Kollegen (`image (1–5).png`).

### ⚙️ Konfiguration

- `.gitignore` — Schließt `Data/*` aus (Rohdaten, 86 CSVs/Excels), außer den 3 `!`-Ausnahmen; schließt zusätzlich `Aufgabenstellung/` aus
- `.devcontainer/devcontainer.json` — Codespaces-Konfiguration; ⚠️ `postAttachCommand` startet noch `streamlit run streamlit_dashboard.py` (alter Root-Pfad) statt `Dashboard/streamlit_dashboard.py`
- `requirements.txt` — 11 Pakete: streamlit, plotly, nbformat, ipykernel, pandas, scikit-learn, joblib, scipy, numpy, matplotlib, seaborn. `nbformat`/`ipykernel` seit 2026-08-11 ergänzt (interaktive Plotly-Grafik + eigener Jupyter-Kernel), `matplotlib`/`seaborn` ebenfalls seit 2026-08-11 ergänzt — fehlten trotz direkter Nutzung in allen Notebooks (siehe „Wichtige Entscheidungen")
- `.venv/` — **NEU (2026-08-11):** projekteigene virtuelle Umgebung, per `.gitignore` ausgeschlossen. Als Jupyter-Kernel „Qualitaets-Muster-Finder (.venv)" registriert (`python -m ipykernel install --user --name qualitaets-muster-finder ...`) — siehe README „Notebooks in VS Code / Jupyter nutzen"

---

## 🔗 Datenfluss

```
Rohdaten (Data/CSV, Data/Excel — 86 Dateien, nicht im Repo)
    ↓ Notebooks/01_Exploration.ipynb
Data/analysetabelle.csv (1.824 Häuser × 18 Spalten)
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
| Häuser analysiert | 1.824 |
| Ø Indikatoren pro Haus | 54,7 |
| Median auffällig-Quote | **76,92 %** |
| Träger mit höchstem Anteil | Privat: **56,5 %** |
| Signifikantester Unterschied (Baustein 2) | Ärzte/Bett (T-Test p < 0,001) |
| Konzernhäuser | 358 von 1.824 (19,6 %) — kein signifikanter Zusammenhang mit Qualitätsproblemen (Chi² p = 0,90) |
| Decision Tree Accuracy | **63,6 %** (Basislinie: 50,7 %) |
| R² (lineare Regression) | **0,033** — schwacher Zusammenhang |
| Wichtigster Prädiktor im aktuellen Modell | `aerzte_pro_bett` (Feature Importance 53,6 %), gefolgt von `pflege_pro_bett` (23,8 %) und `SO.Betten` (22,6 %) |

> **Fazit Baustein 1–4:** Keine starken, eindeutigen Zusammenhänge zwischen Strukturmerkmalen und Qualitätsproblemen. Privathäuser und niedrige Ärztedichte zeigen Tendenzen — aber kein klares Muster. **Kein Zusammenhang ist ein valides Ergebnis.**

### Zusatzbefunde aus `04_Potenzielle_Erweiterungen.ipynb` (noch nicht integriert)

| Geprüfte Datei | Neues Merkmal | Korrelation mit `hat_viele_Probleme` | Empfehlung |
|---|---|---|---|
| `QS.Leistungsbereich.csv` | `mittl_doku_rate` (Dokumentationsrate) | **r = −0,237**, p < 0,001 — stärker als `aerzte_pro_bett` (r = −0,14) | ✅ Einbinden — stärkster gefundener Zusammenhang, möglicher Confounder für den Trägerschaftseffekt |
| `Notfallversorgung.csv` | `notfall_stufe` (0–3) | **r = −0,179**, p < 0,001 | ✅ Einbinden — erklärt, warum Häuser ohne Notfallversorgung (Stufe 0) paradoxerweise die höchste Auffälligkeitsquote haben (kleine-Zahlen-Effekt) |
| `MM.csv` (Mindestmengen) | `mm_compliance_rate` | r = +0,071, p = 0,025 — Median 100 % in beiden Gruppen | ❌ Nicht einbinden — zu geringe Varianz, nur 1.018/1.824 Häuser abgedeckt |

> Würden `mittl_doku_rate` und `notfall_stufe` in `analysetabelle.csv` aufgenommen, würde laut Notebook 04 voraussichtlich `mittl_doku_rate` als wichtigstes Merkmal `aerzte_pro_bett` ablösen und die Decision-Tree-Accuracy über die aktuellen 63,6 % steigen. Dieser Schritt ist bewusst (noch) nicht umgesetzt.

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
- `Data/analysetabelle.csv` — Datenbasis (1.824 Häuser)
- `requirements.txt`
- `grafiken/` — PNG-Grafiken (optional)

> ⚠️ Die Rohdaten in `Data/CSV/` und `Data/Excel/` sind **nicht** im Repository. Für den Dashboard-Betrieb reichen `Data/analysetabelle.csv` und `Data/modell_krankenhaus.pkl` — diese beiden (plus `Data/analysetabelle.xlsx`) sind über eine `.gitignore`-Ausnahme trotzdem versioniert, obwohl sie im sonst ausgeschlossenen `Data/`-Ordner liegen.

> Live-Dashboard: [Qualitäts-Muster-Finder Dashboard](https://appdashboardpy-dkgplgkkzczyvnwpfjjcsp.streamlit.app/)

---

## ⚠️ Offene Punkte

**Präsentation (aus `ToDo.md`, Stand 2026-08-10):**
- [ ] Fragestellung vorstellen, Hürden & Erkenntnisse, Befunde der deskriptiven Analyse benennen
- [ ] Live-Demo des Dashboards (alle 4 Seiten)
- [ ] Grenzen der Analyse ehrlich benennen
- [ ] Generalprobe mit Stoppuhr
- [ ] Abschlusspräsentation halten + gemeinsame Retrospektive
- [ ] Klären, welches der zwei Präsentationskonzepte (Einzel- vs. Team-Vortrag) final gehalten wird

**Code-/Doku-Aufräumen (Stand 2026-08-10):**
- [ ] Generator-Skripte für `Dashboard_Uebersicht.docx`, `ML_Doku.docx` und `Praesentation_Folienvorschlag.docx` fehlen — entweder Skripte wiederherstellen oder Dateien als „manuell gepflegt" kennzeichnen
- [ ] `.devcontainer/devcontainer.json` auf `Dashboard/streamlit_dashboard.py` aktualisieren (verweist noch auf alten Root-Pfad)
- [ ] Entscheiden, ob `mittl_doku_rate` und `notfall_stufe` aus `04_Potenzielle_Erweiterungen.ipynb` in `analysetabelle.csv` und das Modell übernommen werden

**Erledigt seit letztem Stand (2026-07-29 bis 2026-08-10, Auswahl):**
- ✅ Folie 13 im PPTX von Power BI auf Streamlit-Dashboard umgestellt, Live-Dashboard-URL in `README.md` korrigiert
- ✅ Fortschrittsbericht & Sprechertext für Dozenten-Zwischenpräsentation erstellt (`Doku/Dozent/`)
- ✅ Vollständiges Präsentationsskript sowie finale PPTX-Unterlagen erstellt (`Doku/PPT/`)
- ✅ Bonus-Notebook `04_Potenzielle_Erweiterungen.ipynb` inkl. Walkthrough-Doku erstellt
- ✅ Diverse Einmal-Skripte (Folien-Editoren, PNG-Export, alte Word-Generatoren) nach Gebrauch entfernt
- ✅ Alle Dateien in `scripts/` auf Kleinschreibung umbenannt
- ✅ `scripts/grafiken_dokumentation.py` (byteidentisches Duplikat von `grafiken_doku.py`) und `scripts/doku_generieren.py` (veraltete Vorversion von `projekt_doku.py`) gelöscht; `OUT_PATH` in `analysetabelle_zusammenfassung.py` auf `Doku/Word/` korrigiert
- ✅ Grafik 1 in `02_Analyse.ipynb` auf Plotly umgestellt (Hover-Tooltips zeigen Bereich + Hausanzahl je Balken)
- ✅ Projekteigene `.venv` angelegt und als Jupyter-Kernel registriert (`qualitaets-muster-finder`) — löst Kernel-Verwechslung mit einem fremden Projekt (`smart-job-analyzer`), die zu `nbformat`-Fehlern führte
- ✅ `requirements.txt` um `nbformat`, `ipykernel`, `matplotlib`, `seaborn` ergänzt — letztere zwei fehlten trotz direkter Nutzung in allen drei Notebooks komplett
- ✅ Echten End-to-End-Lauf von `02_Analyse.ipynb` über den neuen Kernel durchgeführt und dabei zwei matplotlib-3.11-Breaking-Changes gefunden und behoben: `boxplot(labels=...)` wurde entfernt (jetzt `tick_labels=...`) in den Grafik-2- und Grafik-5+6-Zellen
- ✅ Grafiken 2–5(+6), 7, 9–12 in `02_Analyse.ipynb` ebenfalls auf Plotly mit Hover-Tooltips umgestellt (alle 12 Grafiken bis auf Grafik 8 jetzt interaktiv); mehrere Notebook-Markdown-Zellen um Begriffserklärungen ergänzt (univariat, Inferenzstatistik, T-Test, 50 %-Referenzlinie bei Grafik 7)
- ✅ `scripts/erstelle_dozenten_doku.py` an manuelle Word-Anpassungen in `Fortschrittsbericht_Qualitaets_Muster_Finder.docx` angeglichen (siehe Datei-Übersicht oben) — per Absatz-für-Absatz-Vergleich auf 0 Unterschiede verifiziert

---

## 🔑 Wichtige Entscheidungen

| Entscheidung | Begründung |
|--------------|------------|
| **Median als Grenzwert** für Ziel-Variable | Robust gegenüber Ausreißern, teilt Häuser in zwei gleich große Gruppen (49 % vs. 51 %) |
| **`QSErgBewStrukDialog`** als Bewertungsspalte | Offizieller Bewertungscode des Strukturierten Dialogs — einziger objektiver, vergleichbarer Indikator |
| **N99 ausschließen** | `N99 = nicht bewertet` — würde Quote systematisch verfälschen. Nicht bewertet ≠ unauffällig |
| **Deduplizierung über `(SO.QBID, QSQI.Indikator)`** | `QSQI.AEKey` ist Haus-ID, kein Indikator-Schlüssel — Fehler hätte zu 1 Zeile/Haus statt ~55 geführt |
| **`aerzte_pro_bett` als wichtigstes Merkmal** | Vom Decision Tree gelernt: Feature Importance 53,6 %, T-Test bestätigt (p < 0,001) |
| **`max_depth=3` beim Decision Tree** | Bewusst einfach: erklärbarer Baum, verhindert Overfitting |
| **R² so niedrig (0,033)** | Valides Ergebnis — Strukturmerkmale erklären nur 3,3 % der Varianz |
| **NaN bei `aerzte_pro_bett` nicht auffüllen** | 4 von 5 fehlenden Werten sind Tageskliniken mit 0 Betten — NaN ist korrekt ("nicht anwendbar") |
| **`SO.Standortnummer` statt `SO.QBID` für Konzern-Join** | `Konzern.csv` nutzt `SO.Standortnummer` als Schlüssel — ursprünglicher Code verglich versehentlich gegen `SO.QBID` (0 Treffer), 2026-07-29 korrigiert |
| **`ist_konzern` trotz fehlendem Signal ins Modell aufgenommen** | Chi²-Test zeigt keinen Zusammenhang (p=0,90), Decision Tree bestätigt mit 0 % Feature Importance. Bewusst drin gelassen: „Kein Zusammenhang" ist selbst ein dokumentiertes, vom Modell empirisch bestätigtes Ergebnis |
| **`pflege_pro_bett` über `SO.Personalliste.csv` statt `AQ.Pflege.csv`** | `AQ.Pflege.csv` enthält nur Qualifikationsnachweise, keine Personal-Anzahlen. `SO.Personalliste.csv` hat direkt `SO.QBID` + `SO.Personal.Anzahl` mit Bereich `'Pflege'` |
| **Erweiterungs-Merkmale aus Notebook 04 (noch) nicht ins Hauptmodell übernommen** | Trotz stärkerem Signal (`mittl_doku_rate` r=−0,237 > `aerzte_pro_bett` r=−0,14) bewusst als separate Explorationsanalyse dokumentiert statt spontan ins laufende Modell gemergt — Übernahme würde `01_Exploration.ipynb`, `analysetabelle.csv` und das trainierte Modell neu durchlaufen lassen und ist als expliziter Folgeschritt vorgesehen, nicht Teil des ursprünglichen Aufgabenumfangs |
| **Grafik 1 als Plotly statt matplotlib** | Einzige Grafik mit Hover-Tooltips (Bereich + Hausanzahl je Balken) — bewusst nicht auf alle 12 Grafiken übertragen, um Umfang der Änderung begrenzt zu halten; erfordert `nbformat` zur Laufzeit für `fig.show()` in Jupyter |
| **Projekteigene `.venv` statt geteilter/globaler Python-Umgebung** | Ein in VS Code versehentlich ausgewählter Kernel eines anderen, unabhängigen Projekts (`smart-job-analyzer`) führte zu schwer diagnostizierbaren `nbformat`-Fehlern beim Anzeigen der Plotly-Grafik. Eine dedizierte, per `requirements.txt` reproduzierbare `.venv` + eigener Jupyter-Kernel verhindert künftige Versions-/Abhängigkeitskonflikte zwischen Projekten |

---

*Datenbasis: IQTIG Qualitätsberichte 2023 | Projekt: Qualitäts-Muster-Finder | Diese Übersicht aktualisiert: 2026-08-10*
