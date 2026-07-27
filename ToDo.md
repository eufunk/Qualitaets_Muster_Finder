# ✅ ToDo — Qualitäts-Muster-Finder

> **Projektfrage:** Welche Krankenhausmerkmale hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme hat?
>
> Quelle: `Aufgabenstellung/Fragestellung.docx` & `Aufgabenstellung/Text_Presentation.docx`

---

## 📦 Baustein 1 — Daten vorbereiten *(Woche 1)*

### Setup
- [x] Fachlichen Kontext klären (Qualitätsindikatoren, Qualitätsberichte verstehen)
- [x] Gemeinsames Git-Repository aufsetzen *(entfällt — Projekt wird lokal geteilt, kein GitHub)*
- [x] Rohdaten **nicht** ins Repository — nur per `.gitignore` ausschließen *(Quelle: `Aufgabenstellung/Text_Presentation.docx`, Folie 14: „Die Rohdaten gehören da nicht rein. Die sind zu groß und haben da nichts verloren.")*

### Datensatz erkunden
- [x] Alle CSV-Dateien sichten und ein eigenes „Inhaltsverzeichnis" der Daten erstellen
- [x] Relevante Tabellen identifizieren:
  - Qualitätsindikatoren (C-1.2): Bewertungen für ~1.900 Krankenhäuser
  - Strukturdaten (A-Teil): Betten, Personal, Träger, Standort

### Ziel-Variable erstellen
- [x] Für jedes Krankenhaus: Anteil auffälliger Qualitätsindikatoren berechnen
- [x] Target-Variable definieren: `"Hat überdurchschnittlich viele Probleme"` = liegt über dem Median
- [x] Fallstricke prüfen:
  - [x] Doppelte Einträge entfernen
  - [x] Nur tatsächlich bewertete Indikatoren einbeziehen (nicht bewertet ≠ unauffällig)
- [ ] Zielgröße zuerst **jeder für sich** berechnen → Ergebnisse vergleichen → gemeinsame Version festlegen

### Merkmale auswählen & zusammenführen
- [x] 5–8 aussagekräftige Merkmale auswählen, z. B.:
  - [x] Bettenzahl
  - [x] Ärzte pro Bett
  - [ ] Pflegekräfte pro Bett *(noch offen — aus `FA.Personalliste.csv`, Bereich=Pflege)*
  - [x] Trägerschaft (öffentlich / privat / kirchlich)
  - [x] Region (Stadt/Land oder Bundesland)
  - [x] Uni-Klinik (ja/nein)
  - [x] Fortbildungsquote
- [x] Alle Merkmale + Zielgröße in **eine Analysetabelle** zusammenführen (1 Zeile = 1 Krankenhaus)
- [x] Zusammenführung **per Skript** reproduzierbar machen (kein manuelles Zusammenklicken)

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
- [ ] Randfälle testen: leere Eingaben, fehlende Werte
- [ ] Code aufräumen
- [ ] Komplett-Durchlauf testen: Rohdaten → fertige App ohne Fehler

### Dokumentation
- [x] Startanleitung schreiben → README.md erstellt
- [x] Entscheidungen festhalten → README.md Abschnitt "Wichtige Entscheidungen"

### Präsentation
- [ ] Fragestellung vorstellen
- [ ] Hürden & Erkenntnisse aus der Datenaufbereitung
- [ ] Befunde der deskriptiven Analyse
- [ ] Live-Demo des Dashboards
- [ ] Grenzen der Analyse ehrlich benennen
- [ ] Erzählen statt Stichpunkte ablesen
- [ ] Generalprobe mit Stoppuhr (jeder spricht einen Teil)

### Abschlusspräsentation
- [ ] Abschlusspräsentation halten
- [ ] Gemeinsame Retrospektive: Was lief gut, was mitnehmen?

---

## 🗂️ Teamorganisation

- [ ] Schwerpunkte verteilen: Datenpipeline | Analyse & Modell | Dashboard
- [ ] Wissen teilen: Wer etwas fertig hat, erklärt es den anderen (~10 min)
- [ ] Wochenrhythmus einhalten:
  - [ ] Morgens kurzes Daily
  - [ ] Mittwochs gemeinsamer Zwischenstand
  - [ ] Freitags Demo

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
