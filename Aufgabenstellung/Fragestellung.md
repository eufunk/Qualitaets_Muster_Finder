# Projekt: Qualitäts-Muster-Finder

> Übertragen aus `Aufgabenstellung/Fragestellung.docx` (Original-Aufgabenstellung, unverändert im Inhalt). Die Checkboxen markieren den aktuellen Umsetzungsstand (Stand: 2026-08-09) — Details und Begründungen dazu in `ToDo.md` sowie `Doku/MD/01_Exploration.md` und `Doku/MD/02_Analyse.md`.

---

## Die Fragestellung

> Welche Krankenhausmerkmale hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme hat?

## Hintergrund

Jedes deutsche Krankenhaus berichtet jährlich über ~150 Qualitätsindikatoren — z. B. der Anteil der Patientinnen, bei denen während einer gynäkologischen Bauchspiegelung ein umliegendes Organ verletzt wurde, die Rate der Patientinnen und Patienten ohne Komplikationen nach einem Herzkathetereingriff (PCI), oder der Anteil der Patientinnen und Patienten, bei denen im Krankenhaus ein Druckgeschwür (Dekubitus) entstand. *(Leistungsbereiche GYN-OP, PCI, DEK — direkt aus `QS.Qualitätsindikator.csv`)*

Bei manchen Indikatoren werden Häuser als „auffällig" bewertet. Welche strukturellen Merkmale (Größe, Personal, Ausstattung) unterscheiden Häuser mit vielen vs. wenigen Problemen?

---

## Die Aufgabe

### 1. Daten vorbereiten

- [x] **Ziel-Variable erstellen:**
  - [x] Für jedes Krankenhaus: Anteil auffälliger Qualitätsindikatoren berechnen — *erledigt in `Notebooks/01_Exploration.ipynb`, Kapitel 3 (`QS.Qualitätsindikator.csv` → `auffaellig_quote`); erklärt in `Doku/MD/01_Exploration.md` Kap. 3*
  - [x] Target: „Hat überdurchschnittlich viele Probleme" = liegt über Median — *Spalte `hat_viele_Probleme` in `Data/analysetabelle.csv`, ebenfalls `01_Exploration.ipynb` Kap. 3, Schritt 7*
- [x] **5–8 interessante Merkmale auswählen, z. B.:**
  - [x] Bettenzahl — *`SO.csv` → `SO.Betten`, `01_Exploration.ipynb` Kapitel 2*
  - [x] Ärzte pro Bett — *`FA.Personalliste.csv` × `FA.csv` → `aerzte_pro_bett`, `01_Exploration.ipynb` Kapitel 6*
  - [x] Pflegekräfte pro Bett — *`SO.Personalliste.csv` → `pflege_pro_bett`, `01_Exploration.ipynb` Kapitel 7 (ergänzt 2026-07-29)*
  - [x] Trägerschaft (öffentlich/privat/kirchlich) — *`SO.csv` → `KH.Träger.Art`, `01_Exploration.ipynb` Kapitel 2*
  - [x] Region (Stadt/Land oder Bundesland) — *`SO.csv` → `SO.Bundesland`, `01_Exploration.ipynb` Kapitel 2*
  - [x] Uni-Klinik (ja/nein) — *`SO.csv` → `SO.Uni`, `01_Exploration.ipynb` Kapitel 2*
  - [x] Fortbildungsquote — *`QS.Fortbildung.csv` → `fortbildungsquote`, `01_Exploration.ipynb` Kapitel 4*

### 2. Deskriptive Analyse

- [x] Vergleiche: Wie unterscheiden sich Häuser MIT überdurchschnittlich vielen vs. wenigen Problemen? — *`Notebooks/02_Analyse.ipynb` Kapitel 2 (Grafiken 1–7, 11–12); erklärt in `Doku/MD/02_Analyse.md`*
- [x] Korrelationen berechnen: Welche Merkmale hängen zusammen? — *`02_Analyse.ipynb` Kapitel 3, Grafik 8 (Korrelationsmatrix)*
- [x] Gruppenvergleiche: Uni-Kliniken vs. normale Häuser, große vs. kleine, öffentlich vs. privat — *`02_Analyse.ipynb` Grafiken 2 (Betten), 3 (Träger), 4 (Uni)*
- [x] Visualisierungen: Box-Plots, Scatter-Plots, Balkendiagramme — *alle 12 Grafiken über `scripts/grafiken_speichern.py` erzeugt, liegen in `grafiken/`*

### 3. Dashboard bauen

Streamlit-App mit 4 Seiten *(`Dashboard/streamlit_dashboard.py`)*:

**Seite 1: „Gesamtüberblick"**
- [x] Kennzahlen: Wie viele Häuser haben überdurchschnittlich viele Probleme? Wo?
- [x] Deutschland-Karte: Regionale Verteilung
- [x] Verteilung der auffällig-Quote (Histogramm)
- [x] Filter: Bundesland · Träger · Klinik-Typ

**Seite 2: „Einflussfaktoren"**
- [x] 4 Tabs — Trägervergleich, Personal/Bett Boxplot, Streudiagramm, Pivot-Tabelle
- [x] Z. B. „Ärzte pro Bett: Median MIT vielen Problemen: 0,390 | wenigen Problemen: 0,468"

**Seite 3: „Häuser vergleichen"**
- [x] Eingabe: Betten, Region, Träger → ähnliche Häuser finden
- [x] Ergebnistabelle mit auffällig-Quote je Haus
- [x] Einzelhaus-Steckbrief: Haus vs. Ø ähnlicher Häuser

**Seite 4: „Qualitäts-Vorhersage"** *(Bonus)*
- [x] Merkmal-Eingaben → Decision Tree sagt Risiko voraus
- [x] Entscheidungsbaum-Visualisierung (`grafiken/decision_tree.png`)
- [x] Feature Importance angezeigt

### Zusätzlich: Einfacher Entscheidungsbaum

- [x] Decision Tree trainieren (max. Tiefe 3) — *`Notebooks/03_Decision_Tree.ipynb`, Klasse `KrankenhausModell` in `model/modell_klasse.py`*
- [x] Vorhersage: „Hat überdurchschnittlich viele Probleme" basierend auf Strukturmerkmalen — *`03_Decision_Tree.ipynb`; Modell gespeichert als `Data/modell_krankenhaus.pkl`*
- [x] Accuracy: 63,6 % (Basislinie 50,7 %) · R² = 0,033 · Feature Importance: `aerzte_pro_bett` 53,6 %, `pflege_pro_bett` 23,8 %, `SO.Betten` 22,6 %
- [x] **Dashboard-Seite 4 „Qualitäts-Vorhersage":** Eingabe Merkmale → Modell-Einschätzung + Baumvisualisierung

### Präsentation *(2026-08-09)*

- [x] **Folie 13 im PPTX aktualisiert** — Power BI → Streamlit-Dashboard (Titel, Screenshot, Inhaltszeilen); `scripts/update_folie13.py`
- [x] **Streamlit-Präsentationsfolie** — `Dashboard/folie13_praesentation.py` (slide-artig, 2×2 Karten + Screenshots, für Einzelpräsentation)
- [x] **Sprechertext-Dokument** — `Doku/Praesentationsskript_Qualitaets_Muster_Finder.docx` (30 Min, 15 Folien, erzählend mit Übergängen); `scripts/erstelle_praesentationsskript.py`
- [x] **`Praesentation_Folien_Beschreibung.md`** — alle 15 Folien mit PPTX abgeglichen, Zeile 13 korrigiert

---

## Die Daten (liegen vor)

- Qualitätsindikatoren (C-1.2): Bewertungen für ~1.900 Krankenhäuser *(tatsächlich nachgezählt: 1.824 Häuser mit Bewertungen — siehe Herkunfts-Erklärung in `Doku/MD/01_Exploration.md`, Kapitel 3)*
- Strukturdaten (A-Teil): Betten, Personal, Träger, Standort

## Hinweis

> Dieses Projekt arbeitet mit echten Daten aus dem Gesundheitswesen. Es kann durchaus sein, dass die Analyse keine klaren Zusammenhänge zeigt – das ist ein valides Ergebnis!
