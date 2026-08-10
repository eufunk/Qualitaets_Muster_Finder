# ✅ ToDo — Qualitäts-Muster-Finder

> **Projektfrage:** Welche Krankenhausmerkmale hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme hat?
>
> Quelle: `Aufgabenstellung/Fragestellung.docx` & `Aufgabenstellung/Text_Presentation.docx`

---

## 📦 Baustein 1 — Daten vorbereiten *(Woche 1)*

### Setup
- [x] Fachlichen Kontext klären (Qualitätsindikatoren, Qualitätsberichte verstehen)
- [x] Git-Repository aufsetzen + Code auf GitHub *(Dashboard läuft live auf Streamlit Cloud → GitHub aktiv)*
- [x] Rohdaten **nicht** ins Repository — per `.gitignore` ausgeschlossen *(Folie 14: „Die Rohdaten gehören da nicht rein. Die sind zu groß.")*

### Datensatz erkunden
- [x] Alle CSV-Dateien sichten und ein eigenes „Inhaltsverzeichnis" der Daten erstellen
- [x] Relevante Tabellen identifizieren:
  - Qualitätsindikatoren (C-1.2): Bewertungen für ~1.900 Krankenhäuser *(Schätzung aus Fragestellung.docx — tatsächlich nachgezählt: 1.824)*
  - Strukturdaten (A-Teil): Betten, Personal, Träger, Standort

### Ziel-Variable erstellen
- [x] Für jedes Krankenhaus: Anteil auffälliger Qualitätsindikatoren berechnen
- [x] Target-Variable definieren: `"Hat überdurchschnittlich viele Probleme"` = liegt über dem Median
- [x] Fallstricke prüfen:
  - [x] Doppelte Einträge entfernen (Deduplizierung über `SO.QBID + QSQI.Indikator`)
  - [x] Nur tatsächlich bewertete Indikatoren einbeziehen (N99 ausgeschlossen — nicht bewertet ≠ unauffällig)
  - [x] Nur echte QI-Zeilen (`QSQI.ArtDesWertes == 'QI'` — keine Zählkennzahlen EKez/TKez)

### Merkmale auswählen & zusammenführen
- [x] 5–8 aussagekräftige Merkmale auswählen, z. B.:
  - [x] Bettenzahl
  - [x] Ärzte pro Bett
  - [x] **Pflegekräfte pro Bett** *(2026-07-29 erledigt — `pflege_pro_bett` aus `SO.Personalliste.csv`, Filter `SO.Personal.Bereich == 'Pflege'`; direkter Join über `SO.QBID`, kein Umweg über `FA.csv` nötig)*
  - [x] Trägerschaft (öffentlich / privat / kirchlich)
  - [x] Region (Stadt/Land oder Bundesland)
  - [x] Uni-Klinik (ja/nein)
  - [x] Fortbildungsquote
  - [x] **Konzernzugehörigkeit** *(2026-07-29 ergänzt — `ist_konzern` aus `Konzern.csv`, BI-Kollegen-Empfehlung; Join-Bug behoben, siehe unten)*
- [x] Alle Merkmale + Zielgröße in **eine Analysetabelle** zusammenführen (1 Zeile = 1 Krankenhaus)
- [x] Zusammenführung **per Skript** reproduzierbar machen (kein manuelles Zusammenklicken)
- [x] **Analysetabelle aktualisieren** — `pflege_pro_bett` und `ist_konzern` sind jetzt Spalten 17+18 in `Data/analysetabelle.csv`
- [x] **Bug behoben (2026-07-29):** `01_Exploration.ipynb` verglich beim Konzern-Join `Konzern.csv`s `SO.Standortnummer` fälschlich gegen `SO.QBID` statt gegen `SO.csv`s eigene `SO.Standortnummer`-Spalte → `ist_konzern` war für alle 1.824 Häuser 0. Nach Fix: 358 Konzernhäuser (19,6 %). Chi²-Test zeigt aber: kein signifikanter Zusammenhang mit `hat_viele_Probleme` (p=0,90) — Decision Tree bestätigt das mit 0 % Feature Importance für `ist_konzern`.

---

## 📊 Baustein 2 — Deskriptive Analyse *(Woche 2)*

- [x] Jedes Merkmal **einzeln** untersuchen: Verteilung, typische Werte, Ausreißer, Lücken
- [x] Auffällige vs. unauffällige Häuser **pro Merkmal vergleichen** (Grafik + schriftliche Aussage)
- [x] Zusammenhänge prüfen:
  - [x] Merkmal ↔ Zielgröße (Korrelationen berechnen)
  - [x] Merkmale **untereinander** (z. B. Größe ↔ Personal)
- [x] Störfaktoren aufspüren: „Steckt da vielleicht in Wahrheit etwas anderes dahinter?“
- [x] Gruppenvergleiche:
  - [x] Uni-Kliniken vs. normale Häuser
  - [x] Große vs. kleine Häuser
  - [x] Öffentlich vs. privat
- [x] Visualisierungen erstellen (~10 aussagekräftige Grafiken):
  - [x] Box-Plots
  - [x] Scatter-Plots
  - [x] Balkendiagramme
- [x] Zu **jeder** Grafik einen erklärenden Satz schreiben (auch „kein Unterschied“ ist ein Befund)
- [x] **Grafiken nachgebessert (2026-08-03):** Grafik 1 bekam eine Linie über den Balkenspitzen (bessere Ablesbarkeit der Anzahl) und 10 %-Schritte auf der Prozent-Achse; Grafik 3 die Legende verschoben (überdeckte zuvor den Balken für „öffentlich"); Grafik 4 eine fehlende Farb-Legende ergänzt (inkl. Gruppengrößen n=1.731/93). Alle Änderungen in `scripts/grafiken_speichern.py` **und** synchron im Notebook `02_Analyse.ipynb` vorgenommen.

---

## 🖥️ Baustein 3 — Dashboard bauen *(Woche 3 & 4)*
**Status: ✅ Erster Entwurf abgeschlossen — live auf Streamlit Community Cloud**

### Grundstruktur
- [x] Streamlit kennenlernen und Grundstruktur anlegen (Navigation zwischen Seiten)

### Seite 1 — „Übersicht" *(Pflicht)*
- [x] Kennzahlen: Wie viele Häuser haben überdurchschnittlich viele Probleme? Wo?
- [x] Deutschland-Karte: Regionale Verteilung auffälliger Häuser
- [x] Verteilung: Wie viele auffällige QI haben Häuser im Durchschnitt?

### Seite 2 — „Vergleiche" *(Pflicht)*
- [x] Dropdown: „Wähle ein Merkmal"
- [x] Verteilung bei Häusern mit vielen vs. wenigen Problemen anzeigen
- [x] Beispiel: „Ärzte pro Bett: Ø MIT vielen Problemen: 0.52 | wenigen Problemen: 0.68"
- [x] Ergebnis auch in Worten erklären, nicht nur als Diagramm

### Seite 3 — „Finde ähnliche Krankenhäuser" *(Pflicht)*
- [x] Eingabe: Betten, Region, Träger
- [x] Daten filtern → ähnliche Häuser und deren Qualität anzeigen
- [x] Vergleich: „Dein Haus vs. Durchschnitt ähnlicher Häuser"

### Seite 4 — „Risiko-Rechner" *(Bonus / Kür)*
- [x] Merkmal-Eingaben → Modell sagt Risiko voraus
- [x] Unsicherheit der Vorhersage anzeigen (keine falsche Sicherheit suggerieren)
- [x] Visualisierung des Entscheidungsbaums

### Abschluss Dashboard
- [x] Einheitliches Layout über alle Seiten
- [x] Modell einmal abspeichern (z. B. mit `joblib`), nicht bei jedem Start neu berechnen

---

## 🤖 Baustein 4 — Entscheidungsbaum *(Woche 4, Bonus)*

- [x] Daten in Trainings- und Testdaten aufteilen (`train_test_split`)
- [x] Vergleichs-Basislinie festlegen (wie gut wäre bloßes Raten?)
- [x] Decision Tree trainieren (`max_depth=3`)
- [x] Modell bewerten: Genauigkeit auf **neuen** (Test-)Daten prüfen
- [x] **Cross-Validation** (5-Fold CV) — 59,7 % ± 4,2 % Accuracy, bestätigt kein Overfitting
- [x] Baum in eigenen Worten vorlesen können (Verständnistest)
- [x] Vorhersage: `"Hat überdurchschnittlich viele Probleme"` basierend auf Strukturmerkmalen
- [x] **Metriken:** Accuracy, Precision, Recall, F1-Score, Confusion Matrix
- [x] **R²-Metrik** erklärt und berechnet (R²=0,033 → bestätigt schwachen Zusammenhang)
- [x] **Feature Importance** visualisiert (`aerzte_pro_bett` dominiert mit 53,6 %)
- [x] **OOP** — Modell-Wrapper-Klasse `KrankenhausModell` implementiert *(2026-07-29: Notebook importiert die Klasse jetzt aus `modell_klasse.py` statt sie inline zu duplizieren — behebt zugleich einen `__main__`-Pickle-Bug, der das Dashboard zuvor beim Laden des Modells crashen ließ; 2026-07-30: Datei von `scripts/` nach `model/` verschoben)*
- [x] **`joblib`** — Modell gespeichert als `Data/modell_krankenhaus.pkl`
- [x] **Modell neu trainiert (2026-07-29)** mit `pflege_pro_bett` und `ist_konzern` als zusätzlichen Features. Accuracy 63,6 % (Basislinie 50,7 %). Feature Importance: `aerzte_pro_bett` 53,6 %, `pflege_pro_bett` 23,8 %, `SO.Betten` 22,6 %, alle anderen (inkl. `ist_konzern`) 0 %

---

## 🏁 Baustein 5 — Abschluss & Präsentation *(Woche 5)*

### Robustheit & Code-Qualität
- [ ] Randfälle testen: leere Eingaben, fehlende Werte im Dashboard
- [x] **Code aufräumen** — Duplikat `scripts/doku_generieren.py` gelöscht (identisch mit `word_dokumentation.py`), `datei_uebersicht_a4.py` → `datei_uebersicht.py` umbenannt, `modell_klasse.py` von `scripts/` nach eigenen Ordner `model/` verschoben, python-docx-Metadaten-Bug (falsches Erstelldatum/Autor „2013-12-23"/„python-docx") in allen 5 Word-Generator-Skripten behoben
- [x] Komplett-Durchlauf getestet: Rohdaten → `01_Exploration.ipynb` → `Data/analysetabelle.csv` → `03_Decision_Tree.ipynb` → `Data/modell_krankenhaus.pkl` → `Dashboard/streamlit_dashboard.py` — alles ohne Fehler *(2026-07-29: alle drei Notebooks + Dashboard erfolgreich end-to-end durchlaufen lassen und lokal im Browser via `streamlit run` geprüft)*
- [ ] Streamlit-Cloud-Deployment: Main-File-Pfad in den App-Settings von `scripts/streamlit_dashboard.py` auf `Dashboard/streamlit_dashboard.py` umstellen
- [ ] `requirements.txt` verifizieren — alle verwendeten Pakete enthalten und Versionen aktuell?

### Dokumentation
- [x] Startanleitung schreiben → `README.md` erstellt
- [x] Entscheidungen festhalten → `README.md` Abschnitt "Wichtige Entscheidungen"
- [x] **Entscheidungsbegründungen ausformulieren** *(Folie 13: „festhalten, welche Entscheidungen ihr getroffen habt und warum")* — erledigt:
  - [x] Warum Median als Schwelle (nicht Mittelwert oder fester Wert)? → `Doku/MD/01_Exploration.md` Kap. 3, Schritt 7
  - [x] Warum N99 ausgeschlossen? → `Doku/MD/01_Exploration.md` Kap. 3, Schritt 2
  - [x] Warum diese Merkmale (und nicht andere)? → je ein „Warum"-Abschnitt pro Merkmal in `Doku/MD/01_Exploration.md`, konsolidiert in `Doku/Word/Analysetabelle_Zusammenfassung.docx`
  - [x] Warum `aerzte_pro_bett` über FA.csv statt SO.Personalliste? → `Doku/MD/01_Exploration.md` Kap. 6
- [x] **Notebook-Walkthroughs erstellt:** `Doku/MD/01_Exploration.md`, `Doku/MD/02_Analyse.md` und `Doku/MD/03_Decision_Tree.md` — erklären jeden Schritt der beiden Notebooks inkl. Begründung, mit allen Grafiken eingebettet, Konzept-Boxen (IQTIG, G-BA, p-Wert, Boxplot-Aufbau, „Diagramm lesen" je Grafik) und Klarstellung der „~1.900"-Zahl sowie des kleine-Zahlen-Effekts hinter der 100 %-Spitze in `auffaellig_quote`
- [x] Kollegen-Zusammenfassung erstellt: `Doku/Word/Analysetabelle_Zusammenfassung.docx` (gewählte Merkmale, Ziel-Variablen, Quelltabellen, Merge-Kriterien, Endgröße der Analysetabelle)

### Präsentation *(Folie 13)*

#### Folien & Unterlagen *(2026-08-09 abgeschlossen)*
- [x] **Folie 13 im PPTX aktualisiert** — Power BI → Streamlit-Dashboard (Titel, Screenshot, 5 Inhaltszeilen); Backup unter `Doku/Qualitaets_Muster_Finder_backup_folie13.pptx`; Skript: `scripts/update_folie13.py`
- [x] **`Doku/MD/Praesentation_Folien_Beschreibung.md` korrigiert** — Übersichtstabelle Zeile 13 von „Dashboard in Power BI Präsentieren" auf „Streamlit-Dashboard — Live-Demo" aktualisiert; alle 15 Folien stimmen mit PPTX überein
- [x] **Streamlit-Präsentationsfolie erstellt** — `Dashboard/folie13_praesentation.py`: slide-artige Einzelseite mit 2×2 Karten + Dashboard-Screenshots für die Einzelpräsentation; Start: `streamlit run Dashboard/folie13_praesentation.py`
- [x] **Vollständiges Sprechertext-Dokument erstellt** — `Doku/Praesentationsskript_Qualitaets_Muster_Finder.docx` (30 Min, 15 Folien, erzählend mit fließenden Übergängen, Zeitangaben je Folie); Skript: `scripts/erstelle_praesentationsskript.py`
- [x] **Erzählen statt Stichpunkte ablesen** — Sprechertext je Folie im Word-Skript vollständig ausformuliert, Übergänge hervorgehoben

#### Noch offen
- [ ] Fragestellung vorstellen
- [ ] Hürden & Erkenntnisse aus der Datenaufbereitung (Fallstricke, Designentscheidungen)
- [ ] Befunde der deskriptiven Analyse — auch „kein Zusammenhang" klar und begründet benennen
- [ ] Live-Demo des Dashboards (alle 4 Seiten zeigen)
- [ ] Grenzen der Analyse ehrlich benennen: was können wir **nicht** aussagen?
- [ ] Generalprobe mit Stoppuhr

### Abschlusspräsentation
- [ ] Abschlusspräsentation halten
- [ ] Gemeinsame Retrospektive: Was lief gut, was mitnehmen?

---

## 🗂️ Teamorganisation *(Soloprojekt — angepasst)*

- [x] Schwerpunkte definiert: Datenpipeline → Analyse → Dashboard → Modell → Doku
- [ ] Regelmäßiger Zwischenstand mit Trainer/in
- [ ] Freitags Demo-fähiger Stand

---

> ⚠️ **Hinweis:** Kein Zusammenhang ist ein **valides Ergebnis**. Ehrlichkeit schlägt Effekthascherei.

---

## 🎓 IHK-Abgleich — Was haben wir abgedeckt?

> Abgleich mit `Aufgabenstellung/VorbereitungIHK.md` — welche Themen wurden durch das Projekt praktisch angewendet, welche fehlen noch?

### ✅ Durch das Projekt bereits abgedeckt

| IHK-Thema | Wo im Projekt |
|-----------|---------------|
| **Dateien lesen & schreiben** (`read_csv`, `to_csv`, `pathlib`) | Baustein 1 — alle CSV-Dateien geladen, `analysetabelle.csv` gespeichert |
| **Fehlende Werte** (`isnull()`, NaN-Behandlung) | Baustein 1 — NaN bei `aerzte_pro_bett` (Tageskliniken) bewusst belassen |
| **Duplikate** (`drop_duplicates()`) | Baustein 1 — `(SO.QBID, QSQI.Indikator)` dedupliziert |
| **Datentypen umwandeln** (`str.replace`, `pd.to_numeric`) | Baustein 1 — Komma-Dezimal in Float konvertiert |
| **String-Operationen** (`str.startswith`, `str.replace`) | Baustein 1 — `QSErgBewStrukDialog.str.startswith('R')` |
| **`groupby()` & Aggregationsfunktionen** | Baustein 1 — Ärzte summiert, Quote berechnet |
| **`merge()`** | Baustein 1 — 4 Tabellen zur Analysetabelle zusammengeführt |
| **Boolesche Filter** | Baustein 1 & 2 — `df[df['hat_viele_Probleme']==1]` |
| **f-Strings & Formatierung** | Baustein 1 & 2 — in allen Print-/Plot-Ausgaben |
| **Lagemaße** (Median, Mittelwert) | Baustein 2 — Median-Quote 76,92 %, Vergleiche |
| **Streuungsmaße** (IQR, std) | Baustein 2 — `describe()` in Analyse |
| **Korrelationskoeffizient** (Pearson) | Baustein 2 — Heatmap mit `.corr()` |
| **Scatterplot, Barplot, Histogram, Boxplot, Heatmap** | Baustein 2 — alle 10 Grafiken |
| **T-Test** (Aerzte/Bett) | t=6,002, **p<0,001 signifikant** | Baustein 2 — `02_Analyse.ipynb` |
| **ANOVA** (Träger) | F=11,323, **p<0,001 signifikant** | Baustein 2 — `02_Analyse.ipynb` |
| **Konfidenzintervalle** (95 %) | Wenige=[0,468–0,497], Viele=[0,402–0,433] | Baustein 2 — `02_Analyse.ipynb` |
| **`pivot_table()`** | Träger × Uni-Status | Baustein 2 — `02_Analyse.ipynb` |
| **Feature Matrix X & Zielvariable y** | `analysetabelle.csv` | Baustein 1 |
| **`train_test_split`** | 80/20, stratifiziert | Baustein 4 — `03_Decision_Tree.ipynb` |

---

### ⚠️ Noch nicht abgedeckt — aber als erledigt markiert oder vergessen

> Diese Themen wurden im Rahmen von Baustein 1 & 2 **nicht** angewendet, obwohl sie laut IHK-Liste relevant sind. Bei der Präsentation könnten Fragen dazu kommen!

| IHK-Thema | Warum nicht abgedeckt | Wo nachholen |
|-----------|----------------------|--------------|
| **Inferenzstatistik** — T-Test, ANOVA | **✅ Ergänzt!** Beide signifikant (p<0,001) | Erledigt |
| **Konfidenzintervalle** | **✅ Ergänzt!** | Erledigt |
| **Decision Tree — Gini/Entropy, Visualisierung** | **✅ Abgeschlossen!** | Baustein 4 |
| **Metriken: Accuracy, Precision, Recall, F1, Confusion Matrix** | **✅ Abgeschlossen!** | Baustein 4 |
| **R²-Metrik** *(kritisch — war in Präsentation ein Thema!)* | **✅ Berechnet!** R²=0,033 — erklärt und interpretiert | Baustein 4 |
| **Streamlit** (Widgets, Session State, Formulare) | ✅ Implementiert — 4 Seiten live | Baustein 3 |
| **`pivot_table()`** | **✅ Ergänzt!** | Baustein 2 |
| **OOP / Klassen** | **✅ Implementiert!** Klasse `KrankenhausModell` | Baustein 4 |
| **`joblib` / `pickle`** | **✅ Erledigt!** `modell_krankenhaus.pkl` gespeichert | Baustein 4 |
