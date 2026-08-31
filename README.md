# 🏥 Qualitäts-Muster-Finder

> **Projektfrage:** Welche Krankenhausmerkmale hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme aufweist?

**Live-Dashboard:** [Qualitäts-Muster-Finder Dashboard](https://appdashboardpy-dkgplgkkzczyvnwpfjjcsp.streamlit.app/)  
**Datenbasis:** Qualitätsberichte 2023 — 1.821 deutsche Krankenhäuser mit auswertbarer Qualitätsbewertung (IQTIG)

---

## 📊 Das Dashboard

4 interaktive Seiten:

| Seite | Inhalt |
|-------|--------|
| **Übersicht** | KPI-Karten, Deutschland-Karte, Verteilung der Auffälligkeitsquote |
| **Vergleiche** | Träger, Ärzte/Bett, Streudiagramm, Pivot-Tabelle |
| **Ähnliche Häuser** | Filtersuche + Einzelhaus-Steckbrief |
| **Risiko-Rechner** | Decision Tree Vorhersage mit Unsicherheitsangabe |

---

## 🚀 Lokal starten

### Voraussetzungen
- Python 3.10+
- Pakete aus `requirements.txt`

### Installation
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

> Eigene, projekteigene `.venv` verwenden — nicht die venv eines anderen Projekts als Kernel/Interpreter auswählen. `requirements.txt` enthält u. a. `nbformat` und `ipykernel`, die für interaktive Grafiken (Plotly) und die Notebooks benötigt werden.

### Notebooks in VS Code / Jupyter nutzen
```bash
.venv\Scripts\python -m ipykernel install --user --name qualitaets-muster-finder --display-name "Qualitaets-Muster-Finder (.venv)"
```
Danach in VS Code beim Öffnen eines Notebooks (`Notebooks/*.ipynb`) oben rechts den Kernel **„Qualitaets-Muster-Finder (.venv)"** auswählen.

### Starten
```bash
streamlit run Dashboard/streamlit_dashboard.py
```

→ Dashboard öffnet sich automatisch unter `http://localhost:8501`

### Benötigte Dateien
```
📁 Projektordner/
├── Notebooks/
│   ├── 01_Exploration.ipynb     # Datenaufbereitung (86 CSVs → Data/analysetabelle.csv)
│   ├── 02_Analyse.ipynb         # Deskriptive Analyse (12 Grafiken, T-Test, Chi²-Test, ANOVA)
│   └── 03_Decision_Tree.ipynb   # ML: Decision Tree, Feature Importance
├── Dashboard/
│   ├── streamlit_dashboard.py   # Haupt-App
│   └── dashboard_utils.py       # Funktionen & Plots
├── model/
│   └── modell_klasse.py         # Decision Tree Klasse
├── Data/
│   ├── modell_krankenhaus.pkl   # Trainiertes Modell
│   └── analysetabelle.csv       # Datenbasis (1.821 Häuser)
├── requirements.txt
└── grafiken/                    # PNG-Grafiken (optional)
```

> ⚠️ Die Rohdaten in `Data/CSV/` und `Data/Excel/` (86 Dateien, bis 911 MB) sind **nicht** im Repository. Für den Dashboard-Betrieb werden nur `Data/analysetabelle.csv` und `Data/modell_krankenhaus.pkl` benötigt — diese beiden liegen zwar im sonst per `.gitignore` ausgeschlossenen `Data/`-Ordner, sind aber per expliziter `!`-Ausnahme trotzdem versioniert.
>
> Die Python-Skripte, die die Word-Dokumentation in `Docs/Word/` erzeugen, liegen lokal in `scripts/` — dieser Ordner ist per `.gitignore` bewusst nicht versioniert (siehe `ProjektDetails.md`).

---

## 🗂️ Projektstruktur

| Datei / Ordner | Beschreibung |
|----------------|-------------|
| `Notebooks/01_Exploration.ipynb` | Datenaufbereitung: Ziel-Variable, Merkmale, Analysetabelle |
| `Notebooks/02_Analyse.ipynb` | Deskriptive Analyse: 12 Grafiken, T-Test, Chi²-Test, ANOVA, Konfidenzintervalle |
| `Notebooks/03_Decision_Tree.ipynb` | Decision Tree, Metriken, R², Feature Importance |
| `Dashboard/streamlit_dashboard.py` | Haupt-App: 4 Seiten (Gesamtüberblick, Einflussfaktoren, Häuser vergleichen, Qualitäts-Vorhersage) |
| `Dashboard/dashboard_utils.py` | Hilfsfunktionen: Daten laden, KPIs, Plots, Modell-Vorhersage |
| `model/modell_klasse.py` | OOP-Wrapper `KrankenhausModell` (prepare, fit, evaluate, save, load) |
| `Data/analysetabelle.csv` | Fertige Analysetabelle (Ergebnis aus Baustein 1) |
| `Data/modell_krankenhaus.pkl` | Trainiertes Decision-Tree-Modell |
| `Docs/MD/Workflow.md` | Vollständige Dokumentation aller Entscheidungen |
| `ToDo.md` | Aufgabenliste nach Baustein-Struktur |
| `ProjektDetails.md` | Vollständige, versionierte Dateiübersicht |

---

## 🔑 Wichtige Entscheidungen — Warum haben wir das so gemacht?

### Warum Median als Grenzwert für die Ziel-Variable?
Die auffällig-Quote variiert zwischen 0 % und 100 %. Der Median (5,88 %) teilt die Häuser in genau zwei etwa gleich große Gruppen — das ergibt eine **ausgewogene Klassenverteilung** (49,7 % vs. 50,3 %), was für Machine Learning optimal ist. Ein fixer Schwellenwert (z. B. 80 %) wäre willkürlich.

### Warum `QSErgBewStrukDialog` als Bewertungsspalte?
Diese Spalte enthält den offiziellen Bewertungscode des Strukturierten Dialogs — das standardisierte Verfahren der deutschen Qualitätsberichterstattung. Laut IQTIG-Bericht bedeutet `R10` „im Referenzbereich" (also **nicht** auffällig); jeder andere, bewertbare Code gilt als auffällig — der einzige objektive, vergleichbare Indikator über alle Häuser hinweg.

### Warum alle N*-Codes ausgeschlossen?
`N01`, `N02` und `N99` bedeuten „nicht bewertet" — diese Indikatoren haben **keinen Referenzwert** und können weder als auffällig noch als unauffällig gelten. Sie würden die Quote systematisch verfälschen. Nicht bewertet ≠ unauffällig.

### Warum Deduplizierung über `(SO.QBID, QSQI.Indikator)` statt `QSQI.AEKey`?
`QSQI.AEKey` ist eine **Haus-ID**, kein Indikator-Schlüssel. Ein Fehler hier hätte dazu geführt, dass pro Haus nur 1 Zeile übrig bleibt statt ~55. Die Deduplizierung über `(SO.QBID, QSQI.Indikator)` stellt sicher, dass jeder Indikator pro Haus genau einmal gezählt wird.

### Warum `aerzte_pro_bett` als wichtigstes Merkmal?
Nicht wir haben das entschieden — der Decision Tree hat es aus den Daten gelernt: Feature Importance 72,8 %. Der T-Test bestätigt den Unterschied (p < 0,0001). Häuser mit mehr Ärzten pro Bett haben signifikant höhere Auffälligkeitsquoten.

### Warum `max_depth=3` beim Decision Tree?
Bewusst einfach gehalten: Ein Baum mit max. 3 Entscheidungsebenen ist **erklärbar** — man kann ihn in eigenen Worten vorlesen. Tiefere Bäume würden Overfitting riskieren und die Interpretierbarkeit verlieren. Ziel war ein verständliches Modell, nicht die höchste Accuracy.

### Warum R² negativ (−0,007)?
Das ist ein **valides Ergebnis**, kein Fehler. Strukturmerkmale (Betten, Träger, Ärzte, Pflegepersonal, Konzernzugehörigkeit) erklären die stetige Auffälligkeitsquote linear nicht besser als der reine Durchschnittswert. Das bedeutet: Andere Faktoren (Patientenmix, Spezialisierung, Dokumentationsqualität) spielen eine viel größere Rolle — die aber nicht im Datensatz enthalten sind.

### Warum NaN bei `aerzte_pro_bett` nicht auffüllen?
4 von 5 fehlenden Werten sind Tageskliniken mit `SO.Betten = 0`. Ärzte/Bett ist für diese Häuser **nicht definiert** — 0 Betten ergibt kein sinnvolles Verhältnis. NaN ist hier die korrekte Aussage: „nicht anwendbar".

### Warum `ist_konzern` trotz fehlendem Signal im Modell?
Der Chi²-Test zeigt keinen Zusammenhang zwischen Konzernzugehörigkeit und Qualitätsproblemen (p=0,2585), und der Decision Tree bestätigt das mit 0 % Feature Importance. Wir haben das Merkmal trotzdem aufgenommen, statt es vorab auszuschließen — das Modell soll selbst entscheiden, was relevant ist. „Kein Zusammenhang" ist auch hier ein valider, dokumentierter Befund.

---

## 📈 Ergebnisse auf einen Blick

| Kennzahl | Wert |
|----------|------|
| Häuser analysiert | 1.821 |
| Ø Indikatoren pro Haus | 42,6 |
| Median auffällig-Quote | **5,88 %** |
| Träger mit höchstem Anteil | Öffentlich: **53,5 %** — laut ANOVA aber NICHT signifikant (p = 0,969) |
| Signifikantester Unterschied | Ärzte/Bett (T-Test p < 0,0001) |
| Konzernhäuser | 358 von 1.821 (19,7 %) — kein signifikanter Zusammenhang (Chi² p=0,2585) |
| Decision Tree Accuracy | **57,0 %** (Basislinie: 50,4 %) |
| R² (lineare Regression) | **−0,007** — kein linear nutzbarer Zusammenhang |

> **Fazit:** Keine starken, eindeutigen Zusammenhänge zwischen Strukturmerkmalen und Qualitätsproblemen. Mehr Personal pro Bett hängt mit mehr, nicht weniger, Qualitätsproblemen zusammen — die Trägerschaft zeigt trotz optisch sichtbarem Unterschied laut ANOVA keinen statistisch abgesicherten Zusammenhang. **Kein Zusammenhang ist ein valides Ergebnis.**

---

*Datenbasis: IQTIG Qualitätsberichte 2023 | Projekt: Qualitäts-Muster-Finder*