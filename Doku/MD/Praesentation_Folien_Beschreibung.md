# Präsentation — Qualitäts-Muster-Finder
## Folienbeschreibung für PowerPoint

> **Gesamtdauer:** 30 Minuten  
> **Folienanzahl:** 15 Folien  
> **Richtwert:** ~2 Minuten pro Folie  
> **Format:** Erzählend 
> **Farbschema:** Blau (#1F497D) für Struktur · Grün (#375E23) für Qualität · Orange (#BF5A00) für Auffälligkeit

---

## Folienübersicht (PPTX)

| Folie | Inhalt |
|---|---|
| 1 | Titelfolie — blauer Hintergrund |
| 2 | Agenda mit farbigen Blöcken |
| 3 | Projektfrage + Datensatz-Kennzahlen nebeneinander |
| 4 | Zwei Datenarten (Struktur vs. Qualität) |
| 5 | Ziel-Variable — 6-Schritt-Flowchart |
| 6 | 8 Merkmale als Tabelle |
| 7–11 | Analyse-Ergebnisse mit den echten Grafiken eingebettet |
| 12 | Decision Tree — Baumdiagramm + Feature Importance |
| 13 | Streamlit-Dashboard — Live-Demo |
| 14 | Gesamteinschätzung — Ampel-Tabelle |
| 15 | Grenzen & Ausblick + Abschlussbalken |

---

## BLOCK 1 — Einstieg & Projektfrage (Folien 1–3) · ca. 4 Min

---

### Folie 1 — Titelfolie
**Inhalt:**
- Projekttitel: **Qualitäts-Muster-Finder**
- Untertitel: *Gibt es Zusammenhänge zwischen der Struktur eines Krankenhauses und seiner Qualität?*
- Datum, Name(n)

**Was gesagt wird:**
Kurze Begrüßung. Wir haben echte Daten, echte Methoden — und werden ehrliche Ergebnisse präsentieren, auch wenn kein Zusammenhang gefunden wurde.

---

### Folie 2 — Agenda
**Inhalt:**
1. Projektfrage & Datensatz
2. Datenvorbereitung
3. Ergebnisse der Analyse
4. Machine Learning & Dashboard
5. Fazit & Grenzen

**Was gesagt wird:**
„Wir laufen heute den kompletten Weg einer Datenanalyse ab — von den Rohdaten bis zum interaktiven Dashboard."

---

### Folie 3 — Projektfrage & Datensatz
**Inhalt (zwei Hälften):**

Links — Projektfrage (groß):
> *„Gibt es Zusammenhänge zwischen den Strukturmerkmalen eines Krankenhauses und der Häufigkeit seiner auffälligen Qualitätsindikatoren?"*

Rechts — Datensatz auf einen Blick:
- 🏥 **1.824** Krankenhäuser mit Bewertung
- 📁 **86 CSV-Dateien** · ca. 1,2 GB
- 📊 **~150 Qualitätsindikatoren** pro Haus
- 📅 Berichtsjahr 2023 · Quelle: IQTIG / G-BA

**Was gesagt wird:**
Jedes deutsche Krankenhaus ist gesetzlich verpflichtet, jährlich einen Qualitätsbericht zu veröffentlichen. Das macht diese Daten besonders wertvoll: Alle Häuser werden nach denselben Regeln bewertet — Grundvoraussetzung für einen fairen Vergleich. Die Frage ist bewusst offen formuliert: Kein Zusammenhang ist genauso ein valides Ergebnis wie ein starker Zusammenhang.

---

## BLOCK 2 — Datenvorbereitung (Folien 4–6) · ca. 6 Min

---

### Folie 4 — Zwei Datenarten: Merkmale & Ziel-Variable
**Inhalt (zwei Spalten):**

| **Strukturdaten (Merkmale X)** 🔵 | **Qualitätsdaten (Ziel y)** 🟢 |
|---|---|
| *Wie ist das Haus aufgebaut?* | *Wie gut ist die Versorgung?* |
| Betten, Personal, Träger, Region | ~150 Qualitätsindikatoren pro Haus |
| SO.csv · FA.csv · Konzern.csv | QS.Qualitätsindikator.csv (911 MB!) |

Darunter: einfaches Datenmodell-Diagramm mit SO.QBID als Verbindungsschlüssel

**Was gesagt wird:**
Diese Unterscheidung ist das Herzstück des Projekts. Der A-Teil liefert die Eingaben, der C-Teil das Ergebnis. Wir wollen herausfinden, ob das eine mit dem anderen zusammenhängt. SO.QBID erscheint in ~60 der 86 Dateien — das ist unser universeller Krankenhaus-Schlüssel, der alles verbindet.

---

### Folie 5 — Wie entsteht die Ziel-Variable?
**Inhalt (Flowchart):**
```
QS.Qualitätsindikator.csv
  ↓  Filter: nur echte QI (nicht Zählkennzahlen)
  ↓  N99 ausschließen (nicht bewertet ≠ unauffällig!)
  ↓  Deduplizierung: je Haus + Indikator eine Zeile
  ↓  R* = auffällig  |  N* = nicht auffällig
  ↓  auffaellig_quote = auffällig_n / total_qi
  ↓  Median (~77 %) → hat_viele_Probleme = 0 oder 1
```

**Was gesagt wird:**
Drei Fallstricke: N99 (nicht bewertet ≠ gut), Duplikate (ohne Deduplizierung werden Indikatoren mehrfach gezählt), falsche Typen (EKez/TKez sind Zählkennzahlen, keine echten QI). Der Median als Schwelle teilt die Häuser fair in zwei gleich große Gruppen. Überraschend: 77 % der Indikatoren liegen typischerweise im roten Bereich — das zeigt, wie hoch die Anforderungen gesetzt sind.

---

### Folie 6 — Die 8 Merkmale der Analysetabelle
**Inhalt (kompakte Tabelle):**

| Merkmal | Quelle | Typ |
|---------|--------|-----|
| Bettenzahl | SO.csv | Numerisch |
| Trägerschaft | SO.csv | privat / freigemeinnützig / öffentlich |
| Bundesland | SO.csv | 16 Bundesländer |
| Uni-Klinik | SO.csv | Ja / Nein |
| Fortbildungsquote | QS.Fortbildung.csv | Numerisch 0–1 |
| Ärzte pro Bett | FA.Personalliste.csv + FA.csv | Numerisch |
| Pflegekräfte pro Bett | SO.Personalliste.csv | Numerisch |
| Konzernhaus | Konzern.csv | Ja / Nein |

Ergebnis: `analysetabelle.csv` — **1.824 Zeilen · 18 Spalten** — eine Zeile pro Krankenhaus.

**Was gesagt wird:**
Diese Tabelle ist der Startpunkt für alles Weitere. Das Prinzip: Rohdaten → Analysetabelle → Analyse, Dashboard, Modell. Technisch aufwändig war aerzte_pro_bett: Personaldaten mussten über zwei Joins verknüpft werden, Zahlen waren als Komma-Dezimal gespeichert.

---

## BLOCK 3 — Ergebnisse der Analyse (Folien 7–11) · ca. 10 Min

---

### Folie 7 — Befund 1: Wie ist die Auffälligkeit verteilt?
**Inhalt:**
- Histogramm der `auffaellig_quote` mit Median-Linie (76,92 %)
- Verteilung: linkssteil — die meisten Häuser zwischen 60–90 %

**Was gesagt wird:**
Zunächst: Wie sieht unsere Ziel-Variable aus? Die Verteilung ist plausibel — kein extremes Ungleichgewicht. Die Häuser sind fair in zwei Gruppen aufgeteilt: ~925 wenige Probleme, ~899 viele Probleme.

---

### Folie 8 — Befund 2: Trägerschaft
**Inhalt:**
- Balkendiagramm: Anteil mit vielen Problemen je Trägerart
  - Privat: **56,5 %** · Freigemeinnützig: **46,4 %** · Öffentlich: **46,7 %**
- Daneben: Box-Plot Bettenzahl je Träger — private Häuser sind kleiner (Md ~90 Betten vs. ~260)
- Statistisch signifikant: ANOVA p < 0,001

**Was gesagt wird:**
Das ist unser klarster inhaltlicher Befund. Aber: Private Häuser sind im Median deutlich kleiner. Kleine Häuser haben weniger Fälle pro Indikator — das erhöht die Schwankungsbreite. Der Trägereffekt könnte ein Größeneffekt sein. Korrelation ist nicht Kausalität.

---

### Folie 9 — Befund 3: Personal ist der stärkste Prädiktor
**Inhalt:**
- Box-Plot: Ärzte pro Bett — Wenige Probleme: Md = 0,468 · Viele Probleme: Md = 0,390
- T-Test: t = 6,002 · **p < 0,001** — statistisch signifikant
- Gleiches Muster bei Pflegekräfte pro Bett (ähnliche Stärke)
- Zum Vergleich: Fortbildungsquote — **kein Unterschied** zwischen den Gruppen

**Was gesagt wird:**
Mehr Personal pro Bett geht mit weniger Qualitätsproblemen einher — das gilt für Ärzte und Pflegekräfte gleichermaßen. Fortbildungsquote zeigt dagegen keinen Zusammenhang, obwohl sie in der Aufgabenstellung explizit genannt wurde. Das ist ein Befund, kein Fehler.

---

### Folie 10 — Befund 4: Bundesland & Uni-Status
**Inhalt (zwei Mini-Grafiken):**
- Bundesland-Balken: Saarland höchster Anteil (63 %, n=19), Berlin niedrigster (33 %, n=54)
- Uni-Kliniken vs. normale Häuser: **kaum Unterschied** (47 % vs. 49 %)

**Was gesagt wird:**
Regionale Unterschiede sind sichtbar, aber bei kleinen Bundesländern begrenzt aussagekräftig. Uni-Kliniken zeigen überraschend keinen Vorteil — wahrscheinlich weil sie komplexere Fälle behandeln. Konzernzugehörigkeit: Chi²-Test zeigt keinen signifikanten Zusammenhang.

---

### Folie 11 — Gesamtübersicht: Korrelationsmatrix
**Inhalt:**
- Heatmap der Korrelationen (Grafik 8)
- Stärkste Korrelationen mit `hat_viele_Probleme`:

| Merkmal | r | Fazit |
|---------|---|-------|
| total_qi (Anzahl Indikatoren) | −0,28 | Moderater Zusammenhang |
| Ärzte pro Bett | −0,14 | Schwach, aber stärkster inhaltlicher Prädiktor |
| Pflegekräfte pro Bett | −0,14 | Ähnlich stark |
| Bettenzahl | −0,08 | Sehr schwach |
| Fortbildungsquote | ~0,01 | Kein Zusammenhang |
| Konzernzugehörigkeit | ~0,00 | Kein Zusammenhang |

**Was gesagt wird:**
Alle Zusammenhänge sind schwach. Das ist das zentrale Ergebnis: Die verfügbaren Strukturmerkmale erklären die Qualitätsunterschiede nur begrenzt. Andere Faktoren — Patientenstruktur, Dokumentationsverhalten, regionale Besonderheiten — spielen wahrscheinlich eine größere Rolle.

---

## BLOCK 4 — Machine Learning & Dashboard (Folien 12–13) · ca. 6 Min

---

### Folie 12 — Decision Tree: Modell & Ergebnis
**Inhalt:**
Links — Baumdiagramm (max_depth=3)  
Rechts — Ergebnisse:
- Accuracy: **63,6 %** (Basislinie: 50,7 %)
- Feature Importance: Ärzte/Bett **53,6 %** · Pflege/Bett 23,8 % · Bettenzahl 22,6 %
- R² = 0,033 — Strukturmerkmale erklären nur **3,3 % der Varianz**

**Was gesagt wird:**
Das Modell ist bewusst einfach und erklärbar. Der Baum sagt klar: Ärzte pro Bett ist das wichtigste Merkmal. Die 63,6 % Accuracy sind besser als reines Raten (50,7 %), aber kein starkes Modell — was zum niedrigen R² passt. Das Modell zeigt, was mit den verfügbaren Daten möglich ist.

---

### Folie 13 — Dashboard: Live-Demo
**Inhalt:**
- 4 Seiten im Dashboard:
  - **Gesamtüberblick:** KPI-Tabelle + Deutschlandkarte + Filter
  - **Einflussfaktoren:** 4 Tabs — Träger, Personal, Streudiagramm, Pivot-Tabelle
  - **Häuser vergleichen:** Ähnliche Häuser finden + Einzelhaus-Steckbrief
  - **Qualitäts-Vorhersage:** Merkmale eingeben → Modell-Einschätzung

*→ Live-Demo: ca. 3 Min*

**Was gesagt wird:**
Jetzt zeige ich das Dashboard live. Wichtigste Seite für unsere Fragestellung: Einflussfaktoren — dort sieht man direkt, ob sich Gruppen unterscheiden. Und die Qualitäts-Vorhersage zeigt, wie das Modell zu einer Entscheidung kommt.

---

## BLOCK 5 — Fazit & Grenzen (Folien 14–15) · ca. 4 Min

---

### Folie 14 — Gesamteinschätzung
**Inhalt (Ampel-Tabelle):**

| Merkmal | Zusammenhang? |
|---------|--------------|
| Ärzte / Pflegekräfte pro Bett | 🟢 Schwach, aber stärkster Prädiktor |
| Trägerschaft | 🟡 Sichtbar — Störfaktor Größe beachten |
| Bundesland | 🟡 Sichtbar — kleine Stichproben vorsichtig interpretieren |
| Bettenzahl | 🟡 Sehr schwach |
| Uni-Status / Konzern | 🔴 Kein Zusammenhang |
| Fortbildungsquote | 🔴 Kein Zusammenhang |

**Was gesagt wird:**
Wir finden keine starken, eindeutigen Zusammenhänge. Die Strukturmerkmale allein reichen nicht aus, um Qualitätsprobleme zu erklären. Das ist ein valides Ergebnis — und der ehrlichste Befund, den wir präsentieren können.

---

### Folie 15 — Grenzen & Ausblick
**Inhalt:**

**Grenzen:**
- Patientenmix: Häuser mit schwierigeren Patienten fallen öfter auffällig — kein Qualitätsproblem
- Dokumentationsqualität: Manche Auffälligkeiten sind Dokumentationsfehler
- Kein Kausalitätsnachweis: Korrelation ≠ Kausalität

**Mögliche nächste Schritte:**
- QS.Leistungsbereich.csv (Dokumentationsrate) als weiteres Merkmal einbinden
- Sentiment-Analyse der Freitext-Kommentare (QSQI.KommentarKrankenhaus)
- Mehrstufige Regression mit Patientenstruktur als Kontrollvariable

**Was gesagt wird:**
Jede Analyse hat Grenzen. Die wichtigste: Wir sehen, was Strukturdaten erklären können — aber nicht, was hinter den Kulissen passiert. Für zukünftige Analysen gibt es konkrete Ansätze. Das Dashboard und alle Notebooks sind reproduzierbar und können direkt erweitert werden.

*→ Fragen? Danke!*

---

## Zeitplan

| Block | Inhalt | Folien | Zeit |
|---|---|---|---|
| 1 | Einstieg & Projektfrage | 1–3 | ~4 Min |
| 2 | Datenvorbereitung | 4–6 | ~6 Min |
| 3 | Ergebnisse | 7–11 | ~10 Min |
| 4 | ML & Dashboard | 12–13 | ~6 Min |
| 5 | Fazit & Grenzen | 14–15 | ~4 Min |
| **Gesamt** | | **15 Folien** | **30 Min** |
