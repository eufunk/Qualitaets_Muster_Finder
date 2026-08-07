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
│   ├── 01_Exploration.ipynb      → Datenaufbereitung (86 CSVs → Data/analysetabelle.csv), inkl. pflege_pro_bett & ist_konzern
│   ├── 02_Analyse.ipynb          → Deskriptive Analyse (12 Grafiken, T-Test, Chi²-Test, ANOVA)
│   └── 03_Decision_Tree.ipynb    → ML: Decision Tree, Feature Importance (importiert KrankenhausModell aus model/)
│
├── 🖥️ Dashboard/ — Streamlit-App (2)
│   ├── streamlit_dashboard.py    → Haupt-App: 4 Seiten (Übersicht, Vergleiche, Ähnliche Häuser, Risiko-Rechner)
│   └── dashboard_utils.py        → Hilfsfunktionen: Daten laden, KPIs, Plots, Modell-Vorhersage (importiert modell_klasse aus model/ via sys.path)
│
├── 🧠 model/ — Modell-Logik (1) *(NEU 2026-07-30, vorher in scripts/)*
│   └── modell_klasse.py          → OOP-Wrapper KrankenhausModell (prepare, fit, evaluate, save, load)
│
├── 🐍 scripts/ — Python-Module (7)
│   ├── bi_datenanalyse.py        → Generiert Word-Dokument: BI-Tool-Vergleich
│   ├── datei_uebersicht.py    → Generiert Word-Dokument: Datei-Klassifikation (A4)
│   ├── analysetabelle_zusammenfassung.py → NEU (2026-07-30): Generiert Word-Dokument: Merkmale, Ziel-Variable, Quelltabellen, Merge-Kriterien, Endgröße
│   ├── datensatz_bericht.py      → (intern, gitignored) Generiert Datensatz_Analyse_Bericht.docx — 2026-07-29 aus Doku/MD/ hierher verschoben, hartkodierter os.chdir()-Pfad eines fremden Rechners auf PROJEKT_ROOT-Pattern korrigiert
│   ├── grafiken_speichern.py     → (intern, gitignored) Grafiken aus analysetabelle.csv als PNG
│   ├── powerbi_anleitung.py      → (intern, gitignored) Erzeugt PowerBI-Anleitungs-docx — ⚠️ enthält hartkodierten os.chdir()-Pfad eines anderen Rechners, vor Nutzung prüfen
│   └── word_dokumentation.py     → Erzeugt Dokumentation_Qualitaets_Muster_Finder.docx aus Data/analysetabelle.csv (2026-07-29 auf aktuellen Projektstand gebracht)
│
├── 📊 Daten (3) — liegen in Data/, per .gitignore-Ausnahme trotzdem im Repo
│   ├── Data/analysetabelle.csv        → Zentrale Analysetabelle (1.824 Häuser × 18 Spalten)
│   ├── Data/analysetabelle.xlsx       → Excel-Version
│   └── Data/modell_krankenhaus.pkl    → Trainiertes Decision-Tree-Modell
│
├── 🖼️ grafiken/ — 14 PNG-Grafiken
│   ├── g1_auffaellig_quote.png   → Verteilung auffällig-Quote
│   ├── g2_bettenzahl.png         → Bettenzahl MIT vs. OHNE Probleme
│   ├── g3_traegerschaft.png      → Trägerschaft-Vergleich
│   ├── g4_uni.png                → Uni-Kliniken vs. normale Häuser
│   ├── g5_6_fortbildung_aerzte.png → Fortbildung & Ärzte/Bett
│   ├── g7_bundesland.png         → Anteil je Bundesland
│   ├── g8_korrelation.png        → Korrelationsmatrix (inkl. pflege_pro_bett & ist_konzern)
│   ├── g9_scatter_betten_aerzte.png → Scatter Betten vs. Ärzte/Bett
│   ├── g10_stoerfaktor_traeger.png → Störfaktor Träger × Bettengröße
│   ├── g11_pflege_pro_bett.png   → NEU (2026-07-29): Pflegekräfte pro Bett — Boxplot
│   ├── g12_konzern_vergleich.png → NEU (2026-07-29): Konzernhaus vs. unabhängig
│   ├── confusion_matrix.png      → Confusion Matrix (neu trainiertes Modell)
│   ├── decision_tree.png         → Entscheidungsbaum-Visualisierung (neu trainiertes Modell)
│   └── feature_importance.png    → Feature Importance (neu trainiertes Modell)
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
│   │   ├── 01_Exploration.md     → Schritt-für-Schritt-Erklärung von 01_Exploration.ipynb (was & warum)
│   │   ├── 02_Analyse.md         → NEU (2026-07-30): Schritt-für-Schritt-Erklärung von 02_Analyse.ipynb (was & warum)
│   │   ├── Daten_Inhaltsverzeichnis.md → Übersicht aller 86 CSV-Dateien
│   │   └── Praesentation_Folien_Beschreibung.md
│   └── Doku/Word/                → Word-Dokumentation
│       ├── Dokumentation_Qualitaets_Muster_Finder.docx
│       ├── Datensatz_Analyse_Bericht.docx
│       ├── Datei_Uebersicht.docx
│       └── Analysetabelle_Zusammenfassung.docx → NEU (2026-07-30): Merkmale, Ziel-Variable, Quelltabellen, Merge-Kriterien, Endgröße
│
└── ⚙️ Konfiguration
    ├── .gitignore                → Schließt Data/ aus, außer analysetabelle.csv/.xlsx & modell_krankenhaus.pkl (per !-Ausnahme); schließt zusätzlich Aufgabenstellung/ und 4 interne Skripte aus
    └── requirements.txt          → 7 Pakete (streamlit, plotly, pandas, etc.)
```

---

## 📂 Datei-Übersicht

### 📒 Notebooks (3) — im Ordner `Notebooks/`

- `Notebooks/01_Exploration.ipynb` — Datenaufbereitung: 86 CSV-Dateien erkunden, Ziel-Variable bauen, Merkmale zusammenführen → `Data/analysetabelle.csv`
- `Notebooks/02_Analyse.ipynb` — Deskriptive Analyse: 12 Grafiken, T-Test, Chi²-Test, ANOVA, Konfidenzintervalle, Korrelationen
- `Notebooks/03_Decision_Tree.ipynb` — ML: Decision Tree (max_depth=3), Metriken, R², Feature Importance, joblib

### 🖥️ Dashboard (2) — im Ordner `Dashboard/`

- `Dashboard/streamlit_dashboard.py` — Haupt-App mit 4 Seiten (Übersicht, Vergleiche, Ähnliche Häuser, Risiko-Rechner)
- `Dashboard/dashboard_utils.py` — Hilfsfunktionen: Daten laden, KPIs, Plots, Modell-Vorhersage (Trennung Logik/UI); lädt `Data/analysetabelle.csv` & `Data/modell_krankenhaus.pkl`; importiert `KrankenhausModell` aus `model/modell_klasse.py` (Pfad wird zur Laufzeit über `sys.path` ergänzt, da beide Ordner getrennt sind)

### 🧠 Modell-Logik (1) — im Ordner `model/` *(NEU 2026-07-30, vorher in `scripts/`)*

- `model/modell_klasse.py` — OOP-Wrapper `KrankenhausModell` (prepare, fit, evaluate, save, load); Default-Modellpfad `Data/modell_krankenhaus.pkl`. Einzige Quelle der Wahrheit für Features & Modell-Logik — wird von `Dashboard/dashboard_utils.py` und `Notebooks/03_Decision_Tree.ipynb` ordnerübergreifend importiert (`sys.path`-Ergänzung, kein echtes Python-Package)

### 🐍 Python-Module (7) — im Ordner `scripts/`

- `scripts/bi_datenanalyse.py` — Generiert Word-Dokument: BI-Tool-Vergleich mit Kollegen
- `scripts/datei_uebersicht.py` — Generiert Word-Dokument: Datei-Klassifikation (A4-Übersicht)
- `scripts/analysetabelle_zusammenfassung.py` — **NEU (2026-07-30)** Generiert `Analysetabelle_Zusammenfassung.docx` aus `Data/analysetabelle.csv`: welche Merkmale/Ziel-Variable(n) aus welchen Quelltabellen, Merge-Kriterien (Left Join, Schlüssel je Tabelle), Endgröße — live berechnet, keine hartkodierten Zahlen
- `scripts/datensatz_bericht.py` — *(intern, per `.gitignore` ausgeschlossen)* Generiert `Datensatz_Analyse_Bericht.docx` — **2026-07-29** von `Doku/MD/` hierher verschoben (lag dort fachlich falsch); der hartkodierte `os.chdir()`-Pfad eines fremden Rechners wurde dabei auf das gleiche `PROJEKT_ROOT`-Pattern wie die anderen Skripte umgestellt
- `scripts/word_dokumentation.py` — Generiert `Dokumentation_Qualitaets_Muster_Finder.docx` aus `Data/analysetabelle.csv` — **2026-07-29** auf aktuellen Projektstand gebracht (Baustein-Status, pflege_pro_bett/ist_konzern, 12 Grafiken, offene Punkte)
- `scripts/grafiken_speichern.py` — *(intern, per `.gitignore` ausgeschlossen)* erzeugt die 12 PNG-Grafiken aus `Data/analysetabelle.csv`
- `scripts/powerbi_anleitung.py` — *(intern, per `.gitignore` ausgeschlossen)* PowerBI-Anleitungs-docx-Generator — ⚠️ enthält einen hartkodierten `os.chdir()`-Pfad eines fremden Rechners (`c:\Users\Admin\VSCode\...`), vor erneuter Nutzung anpassen

> **2026-07-29:** `doku_generieren.py` wurde entfernt — es erzeugte exakt dieselbe Datei (`Dokumentation_Qualitaets_Muster_Finder.docx`) wie `word_dokumentation.py`, offenbar ein liegen gebliebener Entwurf aus der Zeit vor dessen Refactoring. Zwei Generatoren für dieselbe Ausgabedatei zu pflegen war redundant und fehleranfällig.

### 📊 Daten (3) — im Ordner `Data/`

- `Data/analysetabelle.csv` — Zentrale Analysetabelle: 1.824 Häuser × 18 Spalten (Basis für alles)
- `Data/analysetabelle.xlsx` — Excel-Version derselben Tabelle
- `Data/modell_krankenhaus.pkl` — Trainiertes Decision-Tree-Modell (joblib)

> Diese 3 Dateien sind die einzigen Inhalte von `Data/`, die per `.gitignore`-Ausnahme (`!Data/...`) trotzdem versioniert werden — die 86 Rohdaten-CSVs/-Excels in `Data/CSV/` und `Data/Excel/` bleiben ausgeschlossen.

### 📄 Dokumentation (Markdown)

- `README.md` — Hauptdokumentation mit Startanleitung & "Wichtige Entscheidungen"
- `ProjektDetails.md` — Detaillierte Projektstruktur & Entscheidungen
- `ToDo.md` — Aufgabenliste mit Haken + IHK-Abgleich
- `Doku/MD/Workflow.md` — Vollständige Workflow-Dokumentation pro Baustein
- `Doku/MD/01_Exploration.md` — Schritt-für-Schritt-Erklärung von `01_Exploration.ipynb`: was gemacht wurde und warum
- `Doku/MD/02_Analyse.md` — **NEU (2026-07-30)** Schritt-für-Schritt-Erklärung von `02_Analyse.ipynb`: was gemacht wurde und warum
- `Doku/MD/Daten_Inhaltsverzeichnis.md` — Übersicht aller 86 CSV-Dateien
- `Doku/MD/Praesentation_Folien_Beschreibung.md` — Präsentationsfolien-Beschreibung

### 📄 Dokumentation (Word)

- `Doku/Word/Dokumentation_Qualitaets_Muster_Finder.docx` — Hauptdokumentation
- `Doku/Word/Datensatz_Analyse_Bericht.docx` — Datensatz-Analyse (86 Dateien)
- `Doku/Word/Datei_Uebersicht.docx` — Datei-Übersicht (generiert)
- `Doku/Word/Analysetabelle_Zusammenfassung.docx` — **NEU (2026-07-30)**: Merkmale, Ziel-Variable, Quelltabellen, Merge-Kriterien, Endgröße (generiert)
- `BI_Analyse/` — BI-Analyse-Ordner mit Word-Dokumenten + 5 Bildern

### 🖼️ Grafiken (`grafiken/`)

14 PNG-Dateien:

- `g1_auffaellig_quote.png` — Verteilung der auffällig-Quote
- `g2_bettenzahl.png` — Bettenzahl MIT vs. OHNE Probleme
- `g3_traegerschaft.png` — Trägerschaft-Vergleich
- `g4_uni.png` — Uni-Kliniken vs. normale Häuser
- `g5_6_fortbildung_aerzte.png` — Fortbildungsquote & Ärzte/Bett
- `g7_bundesland.png` — Anteil je Bundesland
- `g8_korrelation.png` — Korrelationsmatrix (inkl. pflege_pro_bett & ist_konzern)
- `g9_scatter_betten_aerzte.png` — Scatter Bettenzahl vs. Ärzte/Bett
- `g10_stoerfaktor_traeger.png` — Störfaktor Träger × Bettengröße
- `g11_pflege_pro_bett.png` — Pflegekräfte pro Bett MIT vs. OHNE viele Probleme
- `g12_konzern_vergleich.png` — Konzernhaus vs. unabhängiges Haus
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
Data/analysetabelle.csv (1.824 Häuser × 18 Spalten)
    ↓                          ↓
Notebooks/02_Analyse.ipynb  Notebooks/03_Decision_Tree.ipynb
(Grafiken → grafiken/)    (modell_krankenhaus.pkl)
    ↓                          ↓
    └──────────┬───────────────┘
               ↓
    Dashboard/streamlit_dashboard.py (Live-Dashboard)
    ├── Dashboard/dashboard_utils.py (Logik)
    └── model/modell_klasse.py (Modell-Wrapper, ordnerübergreifend importiert)
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
| Konzernhäuser | 358 von 1.824 (19,6 %) — kein signifikanter Zusammenhang mit Qualitätsproblemen (Chi² p = 0,90) |
| Decision Tree Accuracy | **63,6 %** (Basislinie: 50,7 %) |
| R² (lineare Regression) | **0,033** — schwacher Zusammenhang |
| Wichtigster Prädiktor | `aerzte_pro_bett` (Feature Importance 53,6 %), gefolgt von `pflege_pro_bett` (23,8 %) und `SO.Betten` (22,6 %) |

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
- `model/modell_klasse.py` — Decision Tree Klasse (wird von `dashboard_utils.py` ordnerübergreifend importiert)
- `Data/modell_krankenhaus.pkl` — Trainiertes Modell
- `Data/analysetabelle.csv` — Datenbasis (1.824 Häuser)
- `requirements.txt`
- `grafiken/` — PNG-Grafiken (optional)

> ⚠️ Die Rohdaten in `Data/CSV/` und `Data/Excel/` (86 Dateien, bis 911 MB) sind **nicht** im Repository. Für den Dashboard-Betrieb reichen `Data/analysetabelle.csv` und `Data/modell_krankenhaus.pkl` — diese beiden (plus `Data/analysetabelle.xlsx`) sind über eine `.gitignore`-Ausnahme trotzdem versioniert, obwohl sie im sonst ausgeschlossenen `Data/`-Ordner liegen.

---

## ⚠️ Offene Punkte (aus `ToDo.md`)

- **Baustein 5:** Robustheit testen, Code aufräumen, Präsentation vorbereiten
- Entscheidungsbegründungen ausformulieren für Präsentation (inkl. neuer Punkte: Konzern-Join-Fix, Aufnahme von `ist_konzern` trotz fehlendem Signal)
- **Streamlit-Cloud-Deployment prüfen:** Die Live-App (qualitaets-muster-finder.streamlit.app) hat vermutlich `scripts/streamlit_dashboard.py` als Main-File-Pfad hinterlegt — dieser muss in den App-Settings auf `Dashboard/streamlit_dashboard.py` aktualisiert werden, sonst schlägt das nächste Deployment fehl
- `scripts/powerbi_anleitung.py` reparieren — hartkodierter `os.chdir()`-Pfad eines fremden Rechners

**Erledigt (2026-07-29):**
- ✅ `datensatz_bericht.py` von `Doku/MD/` nach `scripts/` verschoben, hartkodierter `os.chdir()`-Pfad auf `PROJEKT_ROOT`-Pattern korrigiert
- ✅ `pflege_pro_bett` und `ist_konzern` final in `Data/analysetabelle.csv` verankert (18 Spalten)
- ✅ Komplett-Durchlauf getestet: Rohdaten → alle 3 Notebooks → Dashboard, fehlerfrei
- ✅ `Notebooks/grafiken/`-Duplikat entfernt (war 1:1 Kopie von `grafiken/`)
- ✅ Konzern-Join-Bug behoben (verglich fälschlich gegen `SO.QBID` statt `SO.Standortnummer`)
- ✅ Modell neu trainiert mit `pflege_pro_bett` & `ist_konzern`, Dashboard-Risiko-Rechner um beide Eingaben erweitert

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
| **`SO.Standortnummer` statt `SO.QBID` für Konzern-Join** | Bug (2026-07-29): `Konzern.csv` nutzt `SO.Standortnummer` als Schlüssel — der ursprüngliche Code verglich ihn versehentlich gegen `SO.QBID` (0 Treffer). `SO.csv` hat aber selbst eine `SO.Standortnummer`-Spalte, die zuvor nicht mit ausgewählt wurde |
| **`ist_konzern` trotz fehlendem Signal ins Modell aufgenommen** | Chi²-Test zeigt keinen Zusammenhang (p=0,90), Decision Tree bestätigt mit 0 % Feature Importance. Bewusst drin gelassen: „Kein Zusammenhang" ist selbst ein dokumentiertes, vom Modell empirisch bestätigtes Ergebnis, kein Grund zum Ausschluss |
| **`pflege_pro_bett` über `SO.Personalliste.csv` statt `AQ.Pflege.csv`** | `AQ.Pflege.csv` enthält nur Qualifikationsnachweise, keine Personal-Anzahlen. `SO.Personalliste.csv` hat direkt `SO.QBID` + `SO.Personal.Anzahl` mit Bereich `'Pflege'` — kein Umweg über `FA.csv` nötig |

---

*Datenbasis: IQTIG Qualitätsberichte 2023 | Projekt: Qualitäts-Muster-Finder*