# 🖥️ Dashboard — Was zeigen wir, und wie?

> **Ziel des Dashboards:** Die Ergebnisse aus `01_Exploration.ipynb` und `02_Analyse.ipynb` interaktiv erlebbar machen — für jemanden, der die Notebooks nie gesehen hat. Das Dashboard ist die Antwort auf die Projektfrage in klickbarer Form.

**Technologie:** Streamlit (`Dashboard/streamlit_dashboard.py`) + Plotly für alle Grafiken  
**Datengrundlage:** `Data/analysetabelle.csv` (1.824 Krankenhäuser, Qualitätsberichte 2023, IQTIG)  
**Modell:** `Data/modell_krankenhaus.pkl` (Decision Tree, `max_depth=3`)

---

## Globale Sidebar

**Was wir zeigen wollen:** Einheitliche Filterung, die auf alle vier Seiten gleichzeitig wirkt.

**Wie wir es zeigen:** Drei `st.selectbox`-Widgets in der linken Sidebar:
- **Bundesland** — alle 16 + „Alle"
- **Trägerschaft** — freigemeinnützig / öffentlich / privat + „Alle"
- **Klinik-Typ** — Alle / Normale Klinik / Uni-Klinik

Ein Live-Zähler zeigt jederzeit an, wie viele Häuser nach dem Filter übrig bleiben (`Häuser im Filter: X von 1.824`). Alle Grafiken und Kennzahlen reagieren sofort auf den Filter — keine separaten Filter-Buttons nötig.

---

## Seite 1 — „📊 Übersicht"

### Was wir zeigen wollen
Den schnellen Gesamtüberblick: Wie viele Häuser haben Qualitätsprobleme, wo liegen sie, und wie ist die Verteilung der Auffälligkeit?

### Wie wir es zeigen

**KPI-Karten (4 Spalten)**

| Karte | Inhalt | Warum diese Zahl? |
|---|---|---|
| 🏥 Krankenhäuser | Absolute Anzahl nach Filter | Zeigt sofort, wie groß die betrachtete Gruppe ist |
| ⚠️ Anteil „Viele Probleme" | Prozent + Delta zu 50 % | 50 % ist die erwartete Baseline (Median-Split) |
| 📈 Ø auffällig-Quote | Mittlere Auffälligkeitsquote | Feingranularer als das 0/1-Label |
| 👨‍⚕️ Ø Ärzte pro Bett | Mittlere Personalstärke | Das wichtigste Feature aus dem Modell |

**Deutschland-Karte (2/3 Breite)**  
- Plotly `scatter_mapbox` auf Basis `carto-positron`
- Jeder Punkt = ein Krankenhaus, **Farbe** = wenige (grün) vs. viele Probleme (rot), **Punktgröße** = Bettenzahl
- Hover zeigt: Name, Betten, Bundesland, Träger, auffällig-Quote
- Zentriert auf Deutschland (lat=51,2 / lon=10,4), Zoom-Level 5

**Histogramm auffällig-Quote (1/3 Breite, neben der Karte)**  
- 30 gleich breite Balken, eingefärbt nach Problemkategorie
- Gestrichelte vertikale Linie bei Median (76,92 %) — erklärt, wo die Grenze zwischen „wenige" und „viele" liegt

**Bundesland-Balkendiagramm (volle Breite)**  
- Ein Balken pro Bundesland, Höhe = Anteil „Viele Probleme" in %
- Einfärben nach Wert (rot je höher), sortiert absteigend
- Zeigt regionale Unterschiede auf einen Blick

---

## Seite 2 — „🔍 Vergleiche"

### Was wir zeigen wollen
Welche Merkmale unterscheiden Häuser mit vielen vs. wenigen Problemen — und wie stark ist der Unterschied?

### Wie wir es zeigen

Vier **Tabs** nebeneinander — jeder Tab beantwortet eine eigene Teilfrage:

**Tab 1 — Trägerschaft**  
- Grouped Bar Chart: pro Trägerart zwei Balken (grün/rot, Anteile summieren sich auf 100 %)
- Textblock darunter mit konkreten Prozentzahlen und statistischem Befund (ANOVA p<0,001)
- Hinweis auf den Störfaktor: Private Häuser sind im Median kleiner → Befund nicht überinterpretieren

**Tab 2 — Ärzte pro Bett**  
- Zwei Boxplots nebeneinander (grün = wenige, rot = viele Probleme), Ausreißer ausgeblendet
- Gestrichelte Linie bei Decision-Tree-Split (0,271 Ärzte/Bett)
- Zwei Metriken darunter: Median Ärzte/Bett für jede Gruppe
- Textblock: T-Test-Ergebnis (t=6,002, p<0,001), Interpretation des Splits

**Tab 3 — Streudiagramm**  
- `st.selectbox` für die X-Achse: aerzte_pro_bett / SO.Betten / fortbildungsquote / total_qi
- Scatter-Plot mit OLS-Regressionslinie (Plotly `trendline="ols"`)
- Caption erklärt r² als Maß für Zusammenhangsstärke
- Zeigt Fälle ohne sichtbaren Zusammenhang (Fortbildungsquote) genauso wie Fälle mit (Ärzte/Bett)

**Tab 4 — Pivot-Tabelle**  
- `pivot_table()`: Zeilen = Trägerart, Spalten = Uni-Status, Zellen = Ø auffällig-Quote
- Heatmap-Formatierung (grün–gelb–rot via `background_gradient(cmap="RdYlGn_r")`)
- Beantwortet: Interagieren Trägerschaft und Uni-Status miteinander?

---

## Seite 3 — „🏨 Ähnliche Häuser"

### Was wir zeigen wollen
Praxisnähe: Jemand mit einem konkreten Krankenhaus im Kopf kann eingeben, was es grob auszeichnet, und sieht ähnliche Häuser mit deren Qualitätsprofil — plus einen Steckbrief für jedes einzelne Haus.

### Wie wir es zeigen

**Filter-Panel (1/3 Breite, linke Spalte)**
- `st.number_input` für Bettenzahl (Toleranz: ±50 % beim Filtern)
- `st.selectbox` für Bundesland und Trägerschaft
- `st.slider` für maximale Anzahl Ergebnisse (5–30)
- Suche startet erst beim Klick auf „🔍 Suchen" (kein Autorefresh bei Eingabe)

**Ergebnistabelle (2/3 Breite, rechte Spalte)**
- `st.dataframe` mit bedingter Formatierung: Zeilen mit „Viele Probleme" leicht rot hinterlegt
- Spalten: Name, Betten, Träger, Bundesland, auffällig-Quote, Ärzte/Bett, Fortbildungsquote, Kategorie
- Zwei Metriken unter der Tabelle: Ø auffällig-Quote und Ø Ärzte/Bett der gefundenen Gruppe, jeweils mit Delta zum Gesamtmedian

**Einzelhaus-Steckbrief (volle Breite, unter dem Filter-Bereich)**
- `st.selectbox` mit allen 1.824 Häusern (Dropdown-Suche nach Name möglich)
- 8 Metriken in zwei Reihen à 4 Spalten: Betten, Träger, Bundesland, Uni-Status + Quote, Kategorie, Ärzte/Bett, Fortbildungsquote
- Quote-Metrik mit Delta zum Gesamtmedian (zeigt auf einen Blick: besser oder schlechter als Durchschnitt?)

---

## Seite 4 — „⚠️ Risiko-Rechner" *(Bonus / Kür)*

### Was wir zeigen wollen
Das trainierte Modell in Aktion: Nutzer gibt Merkmale ein und sieht sofort, ob der Baum ein Haus als Risikohaus einstuft — inkl. ehrlicher Kommunikation der Modellgrenzen.

### Wie wir es zeigen

**Warnhinweis oben** (immer sichtbar, nicht wegklickbar)  
`st.warning`: Modell-Accuracy 63,6 %, R² = 3,3 % — Vorhersagen sind Hinweise, keine Diagnosen. Ehrlichkeit über die Schwäche des Modells ist explizit Teil des Designs.

**Eingabe-Formular (zwei Spalten)**

| Linke Spalte | Rechte Spalte |
|---|---|
| Bettenzahl (`number_input`, 0–2000) | Ärzte pro Bett (`number_input`, 0–5, Schritt 0,05) |
| Uni-Klinik? (`selectbox`: Ja/Nein) | Pflegekräfte pro Bett (`number_input`) |
| Fortbildungsquote (`slider`, 0–100 %) | Trägerschaft (`selectbox`) |
| Konzernhaus? (`selectbox`) | — |

**Ergebnis-Block** (erscheint nach Klick auf „🔮 Risiko berechnen")  
- Farbiger Kasten (grün/rot je nach Vorhersage) mit: Vorhersage-Text, kurze Erklärung, Unsicherheitseinschätzung
- Zwei Metriken: P(Wenige Probleme) und P(Viele Probleme) als Prozentwerte aus `predict_proba`
- **Entscheidungsgrundlage:** Erklärt in Klartext, welcher Wert für Ärzte/Bett den Split auslöst (≤ 0,271 → Risiko hoch), und zeigt ob der eingegebene Wert darüber oder darunter liegt

**Feature-Importance-Diagramm** (immer sichtbar, unabhängig von der Eingabe)  
- Horizontales Balkendiagramm mit den 7 Features und ihren Importance-Werten
- Farblich abgestuft: die 3 genutzten Features (blau) vs. die 4 ungenutzten (grau, Importance = 0)
- Erklärt visuell, warum Ärzte/Bett so viel mehr Gewicht hat als z. B. Fortbildungsquote

---

## Technische Entscheidungen

| Entscheidung | Begründung |
|---|---|
| `@st.cache_data` für CSV-Laden | Daten werden nur einmal geladen, auch bei Seitenwechsel oder Filterwechsel |
| `@st.cache_resource` für Modell | Modell-Objekt bleibt im RAM, kein erneutes Deserialisieren |
| Plotly statt Matplotlib | Interaktive Hover-Infos, zoom- und exportierbar ohne Extra-Code |
| Logik in `dashboard_utils.py` | Trennung UI ↔ Datenlogik: Tests und Wartung ohne Streamlit-Kontext möglich |
| Globale Filter in Sidebar | Eine Änderung filtert alle 4 Seiten gleichzeitig — kein Inkonsistenz-Risiko |
| Komma→Punkt-Fix beim Laden | Koordinaten in `SO.csv` nutzen deutsches Dezimalformat; Fix einmalig beim `lade_daten()`-Aufruf |
