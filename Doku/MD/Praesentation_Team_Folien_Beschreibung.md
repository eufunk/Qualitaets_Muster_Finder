
# Präsentation — Qualitäts-Muster-Finder
## Variante 2: Drei Präsentatoren — 30 Minuten

> **Gesamtdauer:** 30 Minuten  
> **Präsentatoren:** Kollege E · Kollege A · Kollege M  
> **Redezeit pro Person:** je ~10 Minuten  
> **Prinzip:** Jeder präsentiert den Teil, den er selbst erarbeitet hat

---

## Aufgabenteilung auf einen Blick

| Wer | Werkzeug | Inhalt |
|---|---|---|
| **Kollege E** | Jupyter Notebook + Streamlit | Datenvorbereitung · Analyse · Machine Learning |
| **Kollege A** | Power BI | Dashboard-Demo Teil 1 · Visualisierungen Trägerschaft & Personal |
| **Kollege M** | Power BI | Dashboard-Demo Teil 2 · Visualisierungen Bundesland & Korrelation · Fazit |

---

## KOLLEGE E — Technische Grundlagen & Analyse  ·  Folien 1–6 + 12  ·  ~10 Min

> *Kollege E hat den Datensatz aufbereitet, die Ziel-Variable konstruiert, alle Python-Analysen durchgeführt und das Machine-Learning-Modell trainiert.*

---

### Folie 1 — Titelfolie
**Inhalt:**
- Projekttitel: **Qualitäts-Muster-Finder**
- Untertitel: *Gibt es Zusammenhänge zwischen der Struktur eines Krankenhauses und seiner Qualität?*
- Datum, alle drei Namen

**Was gesagt wird (E):**
Kurze Begrüßung, Vorstellung aller drei Präsentatoren und ihrer Rollen. „Ich zeige euch heute, wie wir aus 86 rohen CSV-Dateien eine analysierbare Datenbasis gemacht haben — und was die Python-Analyse ergeben hat."

---

### Folie 2 — Agenda
**Inhalt:**
1. **E:** Projektfrage · Datensatz · Datenvorbereitung · Analyse · ML
2. **A:** Power BI — Dashboard Teil 1
3. **M:** Power BI — Dashboard Teil 2 · Fazit

**Was gesagt wird (E):**
„Jeder von uns präsentiert den Teil, den er selbst erarbeitet hat."

---

### Folie 3 — Projektfrage & Datensatz
**Inhalt:** Projektfrage links · Datensatz-Kennzahlen rechts (1.824 Häuser, 86 CSV, IQTIG 2023)

**Was gesagt wird (E):**
Die Frage ist bewusst offen: Kein Zusammenhang ist genauso ein valides Ergebnis wie ein starker. Der Datensatz ist öffentlich zugänglich — alle Häuser werden nach denselben gesetzlichen Regeln bewertet.

---

### Folie 4 — Zwei Datenarten
**Inhalt:** Strukturdaten (Merkmale X) vs. Qualitätsdaten (Ziel y), verbunden über SO.QBID

**Was gesagt wird (E):**
A-Teil liefert die Eingaben, C-Teil das Ergebnis. SO.QBID ist der universelle Schlüssel, der alle 86 Dateien verbindet.

---

### Folie 5 — Ziel-Variable
**Inhalt:** 6-Schritt-Flowchart von QS.Qualitätsindikator.csv zu hat_viele_Probleme

**Was gesagt wird (E):**
Drei Fallstricke: N99 (nicht bewertet ≠ gut), Duplikate, falsche Typen. Median ~77 % als Schwelle — überraschend hoch, aber plausibel.

---

### Folie 6 — 8 Merkmale
**Inhalt:** Tabelle der 8 Merkmale mit Quelle und Typ

**Was gesagt wird (E):**
Das Ergebnis der Vorbereitung: analysetabelle.csv — 1.824 Zeilen, eine Zeile pro Krankenhaus, bereit für Analyse und Dashboard.

---

### Folie 12 — Decision Tree
**Inhalt:** Baumdiagramm + Feature Importance + Accuracy 63,6 %

**Was gesagt wird (E):**
Das Modell ist bewusst einfach und erklärbar. Ärzte pro Bett dominiert mit 53,6 %. R² = 3,3 % — Strukturmerkmale allein erklären wenig. Das ist ein ehrliches Ergebnis, kein Versagen.

*→ Übergabe an Kollege A*

---
---

## KOLLEGE A — Power BI · Dashboard Teil 1 + Befunde 1–3  ·  Folien 7–9 + PBI-Demo  ·  ~10 Min

> *Kollege A hat das Power-BI-Datenmodell aufgebaut und Visualisierungen zu Trägerschaft und Personal erstellt.*

---

### Folie 7 — Befund 1: Verteilung der Auffälligkeit
**Inhalt:** Histogramm der auffaellig_quote · Median 76,92 % · Verteilung linkssteil

**Was gesagt wird (A):**
Das ist das Ergebnis, das Kollege E vorbereitet hat — ich erkläre, was wir damit im Dashboard visualisiert haben. Die Verteilung zeigt: die meisten Häuser liegen zwischen 60–90 %.

---

### Folie 8 — Befund 2: Trägerschaft
**Inhalt:** Balkendiagramm + Boxplot Bettengröße je Träger · Privat 56,5 %

**Was gesagt wird (A):**
Unser klarster Befund. Aber der Störfaktor ist wichtig: Private Häuser sind kleiner — der Effekt könnte ein Größeneffekt sein. Im Power-BI-Dashboard haben wir genau diesen Vergleich interaktiv aufgebaut.

---

### Folie 9 — Befund 3: Personal
**Inhalt:** Boxplots Ärzte/Bett und Pflege/Bett · T-Test p < 0,001

**Was gesagt wird (A):**
Personal ist der stärkste inhaltliche Prädiktor. Mehr Ärzte und Pflegekräfte pro Bett → weniger Qualitätsprobleme. Fortbildungsquote dagegen zeigt keinen Zusammenhang.

---

### Folie 13 — Power BI Dashboard Teil 1
**Inhalt:** Power-BI-Demo live

**Was gesagt wird (A):**
Jetzt zeige ich, wie wir diese Befunde in Power BI visualisiert haben. Ich gehe durch: Überblick-Seite, Trägerschafts-Vergleich und Personal-Analyse. *(Live-Demo ca. 3 Min)*

*→ Übergabe an Kollege M*

---
---

## KOLLEGE M — Power BI · Dashboard Teil 2 + Befunde 4–5 + Fazit  ·  Folien 10–11 + 14–15  ·  ~10 Min

> *Kollege M hat weitere Power-BI-Visualisierungen (Bundesland, Korrelation) erstellt und fasst das Gesamtergebnis zusammen.*

---

### Folie 10 — Befund 4: Bundesland & Uni-Status
**Inhalt:** Bundesland-Balkendiagramm · Uni-Kliniken vs. normale Häuser · Konzern

**Was gesagt wird (M):**
Regionale Unterschiede sind sichtbar — Saarland 63 %, Berlin 33 %. Aber: Kleine Bundesländer haben wenige Häuser, die Zahlen sind mit Vorsicht zu interpretieren. Uni-Kliniken und Konzernhäuser zeigen überraschend keinen Vorteil.

---

### Folie 11 — Korrelationsmatrix
**Inhalt:** Heatmap · alle r-Werte · alle Zusammenhänge schwach

**Was gesagt wird (M):**
Das Gesamtbild: Alle Zusammenhänge sind schwach. Strukturmerkmale erklären die Qualitätsunterschiede nur begrenzt. Im Power-BI-Dashboard kann man jeden dieser Zusammenhänge interaktiv erkunden.

---

### Folie 13 — Power BI Dashboard Teil 2 *(Fortsetzung)*
**Inhalt:** Power-BI-Demo live — Bundesland-Seite und Korrelations-Visualisierung

**Was gesagt wird (M):**
Ich zeige die restlichen Dashboard-Seiten: Bundesland-Vergleich und die interaktive Tabelle. *(Live-Demo ca. 2 Min)*

---

### Folie 14 — Gesamteinschätzung
**Inhalt:** Ampel-Tabelle aller Merkmale

**Was gesagt wird (M):**
Wir finden keine starken, eindeutigen Zusammenhänge. Das ist ein valides Ergebnis. Personal ist der stärkste Prädiktor — aber auch dieser Effekt ist schwach.

---

### Folie 15 — Grenzen & Ausblick
**Inhalt:** Grenzen (Patientenmix, Dokumentation, Kausalität) · Ausblick (weitere Datenquellen, NLP, Regression)

**Was gesagt wird (M):**
Jede Analyse hat Grenzen. Die wichtigste: Strukturdaten erklären nicht alles. Als nächste Schritte wären Patientenstruktur-Daten und eine Sentiment-Analyse der Krankenhaus-Kommentare interessant. Alle Notebooks und das Dashboard sind reproduzierbar. → Fragen?

---
---

## Zeitplan

| Wer | Folien | Inhalt | Zeit |
|---|---|---|---|
| **Kollege E** | 1, 2, 3, 4, 5, 6, 12 | Einstieg · Datenvorbereitung · ML | ~10 Min |
| **Kollege A** | 7, 8, 9, 13 (Teil 1) | Befunde 1–3 · Power BI Demo Teil 1 | ~10 Min |
| **Kollege M** | 10, 11, 13 (Teil 2), 14, 15 | Befunde 4–5 · Power BI Demo Teil 2 · Fazit | ~10 Min |
| **Gesamt** | **15 Folien** | | **30 Min** |

---

## Absprache-Empfehlungen

- **Übergabe E → A:** Nach Folie 6 kurze Übergabe: „Jetzt zeigt euch Kollege A, was diese Daten im Power-BI-Dashboard bedeuten — und welche Befunde sich dabei ergeben haben."
- **Übergabe A → M:** Nach der ersten Dashboard-Demo: „Kollege M führt durch die restlichen Befunde und das Fazit."
- **Folie 13 teilen:** A zeigt Träger/Personal-Seiten im PBI-Dashboard, M zeigt Bundesland/Korrelation-Seiten — beide kommen kurz zu Folie 13 zurück.
- **Gemeinsame Vorbereitung:** Folie 2 (Agenda) sollte alle drei Namen und Rollen zeigen, damit das Publikum weiß, wer wann spricht.
