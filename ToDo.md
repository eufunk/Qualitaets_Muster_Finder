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
  - Qualitätsindikatoren (C-1.2): Bewertungen für ~1.900 Krankenhäuser
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
  - [ ] **Pflegekräfte pro Bett** *(noch offen — explizit in `Fragestellung.docx` gefordert! Aus `FA.Personalliste.csv`, Filter: `FA.Personal.Bereich == 'Pflege'` — analog zu Ärzte-Berechnung)*
  - [x] Trägerschaft (öffentlich / privat / kirchlich)
  - [x] Region (Stadt/Land oder Bundesland)
  - [x] Uni-Klinik (ja/nein)
  - [x] Fortbildungsquote
- [x] Alle Merkmale + Zielgröße in **eine Analysetabelle** zusammenführen (1 Zeile = 1 Krankenhaus)
- [x] Zusammenführung **per Skript** reproduzierbar machen (kein manuelles Zusammenklicken)
- [ ] **Analysetabelle aktualisieren** sobald Pflegekräfte pro Bett berechnet ist (Spalte ergänzen)

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
- [x] Baum in eigenen Worten vorlesen können (Verständnistest)
- [x] Vorhersage: `"Hat überdurchschnittlich viele Probleme"` basierend auf Strukturmerkmalen
- [x] **Metriken:** Accuracy, Precision, Recall, F1-Score, Confusion Matrix
- [x] **R²-Metrik** erklärt und berechnet (R²=0,023 → bestätigt schwachen Zusammenhang)
- [x] **Feature Importance** visualisiert (`aerzte_pro_bett` dominiert)
- [x] **OOP** — Modell-Wrapper-Klasse `KrankenhausModell` implementiert
- [x] **`joblib`** — Modell gespeichert als `modell_krankenhaus.pkl`

---

## 🏁 Baustein 5 — Abschluss & Präsentation *(Woche 5)*

### Robustheit & Code-Qualität
- [ ] Randfälle testen: leere Eingaben, fehlende Werte im Dashboard
- [ ] Code aufräumen (ungenutzte Variablen, überflüssige Kommentare)
- [ ] Komplett-Durchlauf testen: Rohdaten → `01_Exploration.ipynb` → `Data/analysetabelle.csv` → `Dashboard/streamlit_dashboard.py` — alles ohne Fehler *(Folie 13: „Geht das von den Rohdaten bis zur fertigen App durch, ohne dass es irgendwo hakt?")* *(2026-07-29: Code las zuvor aus dem Projekt-Root statt aus `Data/`, wo die Dateien tatsächlich lagen — jetzt behoben. Zusätzlich `streamlit_dashboard.py`/`dashboard_utils.py` nach `Dashboard/` verschoben. End-to-End-Lauf noch nicht verifiziert.)*
- [ ] Streamlit-Cloud-Deployment: Main-File-Pfad in den App-Settings von `scripts/streamlit_dashboard.py` auf `Dashboard/streamlit_dashboard.py` umstellen
- [ ] `requirements.txt` verifizieren — alle verwendeten Pakete enthalten und Versionen aktuell?

### Dokumentation
- [x] Startanleitung schreiben → `README.md` erstellt
- [x] Entscheidungen festhalten → `README.md` Abschnitt "Wichtige Entscheidungen"
- [ ] **Entscheidungsbegründungen** ausformulieren *(Folie 13: „festhalten, welche Entscheidungen ihr getroffen habt und warum"):*
  - [ ] Warum Median als Schwelle (nicht Mittelwert oder fester Wert)?
  - [ ] Warum N99 ausgeschlossen?
  - [ ] Warum diese Merkmale (und nicht andere)?
  - [ ] Warum `aerzte_pro_bett` über FA.csv statt SO.Personalliste?

### Präsentation *(Folie 13)*
- [ ] Fragestellung vorstellen
- [ ] Hürden & Erkenntnisse aus der Datenaufbereitung (Fallstricke, Designentscheidungen)
- [ ] Befunde der deskriptiven Analyse — auch „kein Zusammenhang" klar und begründet benennen
- [ ] Live-Demo des Dashboards (alle 4 Seiten zeigen)
- [ ] Grenzen der Analyse ehrlich benennen: was können wir **nicht** aussagen?
- [ ] **Erzählen statt Stichpunkte ablesen** *(Folie 13: „Niemand will Stichpunkte vorgelesen bekommen")*
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
| **Inferenzstatistik** — T-Test, ANOVA | ~~Noch nicht gemacht~~ — **✅ Ergänzt!** Beide signifikant (p<0,001) | ~~Baustein 2 ergänzen~~ Erledigt |
| **Konfidenzintervalle** | ~~Nicht berechnet~~ — **✅ Ergänzt!** | Erledigt |
| **Decision Tree — Gini/Entropy, Visualisierung** | **✅ Abgeschlossen!** | Baustein 4 |
| **Metriken: Accuracy, Precision, Recall, F1, Confusion Matrix** | **✅ Abgeschlossen!** | Baustein 4 |
| **R²-Metrik** *(kritisch — war in Präsentation ein Thema!)* | **✅ Berechnet!** R²=0,023 — erklärt und interpretiert | Baustein 4 |
| **Streamlit** (Widgets, Session State, Formulare) | ✅ Implementiert — 4 Seiten live | Baustein 3 |
| **`pivot_table()`** | **✅ Ergänzt!** | Baustein 2 |
| **OOP / Klassen** | **✅ Implementiert!** Klasse `KrankenhausModell` | Baustein 4 |
| **`joblib` / `pickle`** | **✅ Erledigt!** `modell_krankenhaus.pkl` gespeichert | Baustein 4 |
