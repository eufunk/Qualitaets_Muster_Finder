# 🏥 Qualitäts-Muster-Finder

> **Projektfrage:** Welche Krankenhausmerkmale hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme aufweist?

**Live-Dashboard:** [qualitaets-muster-finder.streamlit.app](https://qualitaets-muster-finder.streamlit.app)  
**Datenbasis:** Qualitätsberichte 2023 — 1.824 deutsche Krankenhäuser (IQTIG)

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
pip install -r requirements.txt
```

### Starten
```bash
streamlit run streamlit_dashboard.py
```

→ Dashboard öffnet sich automatisch unter `http://localhost:8501`

### Benötigte Dateien
```
📁 Projektordner/
├── streamlit_dashboard.py   # Haupt-App
├── dashboard_utils.py       # Funktionen & Plots
├── modell_klasse.py         # Decision Tree Klasse
├── modell_krankenhaus.pkl   # Trainiertes Modell
├── analysetabelle.csv       # Datenbasis (1.824 Häuser)
├── requirements.txt
└── grafiken/                # PNG-Grafiken (optional)
```

> ⚠️ Der `Data/`-Ordner mit den Rohdaten (86 CSV-Dateien, bis 911 MB) ist **nicht** im Repository. Er wird für den Dashboard-Betrieb **nicht benötigt** — nur `analysetabelle.csv` reicht.

---

## 🗂️ Projektstruktur

| Datei / Ordner | Beschreibung |
|----------------|-------------|
| `01_Exploration.ipynb` | Datenaufbereitung: Ziel-Variable, Merkmale, Analysetabelle |
| `02_Analyse.ipynb` | Deskriptive Analyse: 10 Grafiken, T-Test, ANOVA, Konfidenzintervalle |
| `03_Decision_Tree.ipynb` | Decision Tree, Metriken, R², Feature Importance |
| `analysetabelle.csv` | Fertige Analysetabelle (Ergebnis aus Baustein 1) |
| `modell_krankenhaus.pkl` | Trainiertes Decision-Tree-Modell |
| `Workflow.md` | Vollständige Dokumentation aller Entscheidungen |
| `ToDo.md` | Aufgabenliste nach Baustein-Struktur |

---

## 🔑 Wichtige Entscheidungen — Warum haben wir das so gemacht?

### Warum Median als Grenzwert für die Ziel-Variable?
Die auffällig-Quote variiert zwischen 0 % und 100 %. Der Median (76,92 %) teilt die Häuser in genau zwei gleich große Gruppen — das ergibt eine **ausgewogene Klassenverteilung** (49 % vs. 51 %), was für Machine Learning optimal ist. Ein fixer Schwellenwert (z.B. 80 %) wäre willkürlich.

### Warum `QSErgBewStrukDialog` als Bewertungsspalte?
Diese Spalte enthält den offiziellen Bewertungscode des Strukturierten Dialogs — das standardisierte Verfahren der deutschen Qualitätsberichterstattung. `R*` (rechnerisch auffällig) ist der einzige objektive, vergleichbare Indikator über alle Häuser hinweg.

### Warum N99 ausgeschlossen?
`N99 = nicht bewertet` — diese Indikatoren haben **keinen Referenzwert** und können weder als auffällig noch als unauffällig gelten. Sie würden die Quote systematisch verfälschen. Nicht bewertet ≠ unauffällig.

### Warum Deduplizierung über `(SO.QBID, QSQI.Indikator)` statt `QSQI.AEKey`?
`QSQI.AEKey` ist eine **Haus-ID**, kein Indikator-Schlüssel. Ein Fehler hier hätte dazu geführt, dass pro Haus nur 1 Zeile übrig bleibt statt ~55. Die Deduplizierung über `(SO.QBID, QSQI.Indikator)` stellt sicher, dass jeder Indikator pro Haus genau einmal gezählt wird.

### Warum `aerzte_pro_bett` als wichtigstes Merkmal?
Nicht wir haben das entschieden — der Decision Tree hat es aus den Daten gelernt: Feature Importance 71,3 %. Der T-Test bestätigt den Unterschied (p < 0,001). Häuser mit ≤ 0,271 Ärzten/Bett haben signifikant höhere Auffälligkeitsquoten.

### Warum `max_depth=3` beim Decision Tree?
Bewusst einfach gehalten: Ein Baum mit max. 3 Entscheidungsebenen ist **erklärbar** — man kann ihn in eigenen Worten vorlesen. Tiefere Bäume würden Overfitting riskieren und die Interpretierbarkeit verlieren. Ziel war ein verständliches Modell, nicht die höchste Accuracy.

### Warum R² so niedrig (0,023)?
Das ist ein **valides Ergebnis**, kein Fehler. Strukturmerkmale (Betten, Träger, Ärzte) erklären nur 2,3 % der Varianz in der Auffälligkeitsquote. Das bedeutet: Andere Faktoren (Patientenmix, Spezialisierung, Dokumentationsqualität) spielen eine viel größere Rolle — die aber nicht im Datensatz enthalten sind.

### Warum NaN bei `aerzte_pro_bett` nicht auffüllen?
4 von 5 fehlenden Werten sind Tageskliniken mit `SO.Betten = 0`. Ärzte/Bett ist für diese Häuser **nicht definiert** — 0 Betten ergibt kein sinnvolles Verhältnis. NaN ist hier die korrekte Aussage: „nicht anwendbar".

---

## 📈 Ergebnisse auf einen Blick

| Kennzahl | Wert |
|----------|------|
| Häuser analysiert | 1.824 |
| Ø Indikatoren pro Haus | 54,7 |
| Median auffällig-Quote | **76,92 %** |
| Träger mit höchstem Anteil | Privat: **56,5 %** |
| Signifikantester Unterschied | Ärzte/Bett (T-Test p < 0,001) |
| Decision Tree Accuracy | **64,9 %** (Basislinie: 50,7 %) |
| R² (lineare Regression) | **0,023** — schwacher Zusammenhang |

> **Fazit:** Keine starken, eindeutigen Zusammenhänge zwischen Strukturmerkmalen und Qualitätsproblemen. Privathäuser und niedrige Ärztedichte zeigen Tendenzen — aber kein klares Muster. **Kein Zusammenhang ist ein valides Ergebnis.**

---

*Datenbasis: IQTIG Qualitätsberichte 2023 | Projekt: Qualitäts-Muster-Finder*
