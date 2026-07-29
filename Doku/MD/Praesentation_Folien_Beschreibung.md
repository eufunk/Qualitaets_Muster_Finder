---
noteId: "1b8946b08b7211f184a2cf9ec95e8a13"
tags: []

---

# 🎤 Präsentation — Qualitäts-Muster-Finder
## Folienbeschreibung für PowerPoint

> **Gesamtdauer:** ~60 Minuten  
> **Folienanzahl:** 27 Folien  
> **Richtwert:** ~2–3 Minuten pro Folie  
> **Format:** Erzählend — keine Stichpunkt-Listen ablesen, sondern erklären  
> **Farbschema (Empfehlung):** Blau (#1F497D) für Struktur-Themen · Grün (#375E23) für Qualitäts-Themen · Orange (#BF5A00) für Auffälligkeits-Konzepte

---

## BLOCK 1 — Einstieg & Kontext (Folien 1–5) · ca. 10 Min

---

### Folie 1 — Titelfolie
**Inhalt:**
- Projekttitel: **Qualitäts-Muster-Finder**
- Untertitel: *Gibt es Zusammenhänge zwischen der Struktur eines Krankenhauses und seiner Qualität?*
- Datum, Name(n)
- Logo / Kurs-Kontext (falls vorhanden)

**Was gesagt wird:**  
Kurze Begrüßung, Projektname erklären, Erwartungshaltung setzen: Wir haben echte Daten, echte Methoden — und werden ehrliche Ergebnisse präsentieren, auch wenn kein Zusammenhang gefunden wurde.

---

### Folie 2 — Agenda
**Inhalt (Übersicht der Blöcke):**
1. Kontext & Fragestellung
2. Der Datensatz — was steckt drin?
3. Vorgehen & Datenvorbereitung
4. Ergebnisse der Analyse
5. Das Dashboard
6. Gesamteinschätzung & Grenzen

**Was gesagt wird:**  
„Wir laufen heute den kompletten Weg einer Datenanalyse ab — von den Rohdaten bis zum interaktiven Dashboard."

---

### Folie 3 — Die Projektfrage
**Inhalt (zentriert, groß):**
> *„Gibt es Zusammenhänge zwischen den Strukturmerkmalen eines Krankenhauses — Größe, Personal, Träger, Region — und der Häufigkeit seiner auffälligen Qualitätsindikatoren?"*

Darunter klein: *Quelle: Aufgabenstellung / Fragestellung.docx*

**Was gesagt wird:**  
Die Frage ist bewusst offen formuliert. Wir suchen nach Mustern, nicht nach Beweisen. Kein Zusammenhang ist genauso ein valides Ergebnis wie ein starker Zusammenhang — das ist wichtig zu betonen, bevor wir anfangen.

---

### Folie 4 — Warum Krankenhausqualität?
**Inhalt:**
- Jedes deutsche Krankenhaus ist seit 2005 **gesetzlich verpflichtet**, jährlich einen Qualitätsbericht zu veröffentlichen
- Herausgeber: **IQTIG** (Institut für Qualitätssicherung und Transparenz im Gesundheitswesen), im Auftrag des **G-BA** (Gemeinsamer Bundesausschuss)
- Die Daten sind **öffentlich zugänglich** und für alle ~1.900 Krankenhäuser **einheitlich** erhoben
- Berichtsjahr: **2023**

**Visualisierung:** Kleine Infografik — Krankenhaus → Qualitätsbericht → IQTIG → Datensatz

**Was gesagt wird:**  
Das macht diese Daten besonders wertvoll: Alle Häuser werden nach denselben Regeln bewertet. Das ist die Grundvoraussetzung für einen fairen Vergleich.

---

### Folie 5 — Der Datensatz auf einen Blick
**Inhalt (Kennzahlen-Karten):**
- 🏥 **~1.900** Krankenhäuser
- 📁 **86 CSV-Dateien** · ca. 1,2 GB
- 📊 **~150 Qualitätsindikatoren** pro Haus
- 🔑 **1 universeller Schlüssel:** `SO.QBID`
- 📅 Berichtsjahr: 2023

**Was gesagt wird:**  
86 Dateien klingt viel — und ist es auch. Der erste Teil unserer Arbeit war, diesen Datensatz überhaupt zu verstehen. Wie wir das gemacht haben, zeige ich gleich.

---

## BLOCK 2 — Der Datensatz (Folien 6–9) · ca. 12 Min

---

### Folie 6 — Zwei Datenarten: A-Teil und C-Teil
**Inhalt (zwei Spalten, farblich getrennt):**

| **A-Teil — Strukturdaten** 🔵 | **C-Teil — Qualitätsdaten** 🟢 |
|---|---|
| *Wie ist das Haus aufgebaut?* | *Wie gut ist die Versorgung?* |
| Betten, Personal, Träger, Region, Uni | ~150 Qualitätsindikatoren pro Haus |
| → unsere **MERKMALE (X)** | → unsere **ZIEL-VARIABLE (y)** |

**Was gesagt wird:**  
Diese Unterscheidung ist das Herzstück des Projekts. Der A-Teil liefert uns die Eingaben — die Dinge, die wir als Eigenschaften eines Hauses messen können. Der C-Teil liefert das Ergebnis — wie gut das Haus bei der Qualität abschneidet. Wir wollen herausfinden, ob das eine mit dem anderen zusammenhängt.

---

### Folie 7 — Was ist ein Qualitätsindikator?
**Inhalt:**
- Ein QI misst einen **spezifischen Aspekt der Behandlungsqualität**
- Jeder QI hat einen **Referenzbereich** — festgelegt vom G-BA
- Beispiel: *„Die Komplikationsrate bei Hüftprothesen-OPs darf maximal 3% betragen"*
- Liegt ein Haus **außerhalb** → gilt es als **„rechnerisch auffällig" (R\*)**
- Liegt ein Haus **innerhalb** → gilt es als **„nicht auffällig" (N\*)**
- **Nicht bewertet (N99):** zu wenig Fälle, Indikator nicht anwendbar → wird ausgeschlossen

**Visualisierung:** Einfache Skala: grüner Bereich (N\*) | roter Bereich (R\*) · Beispielwert eingezeichnet

**Was gesagt wird:**  
Wichtig: „Auffällig" bedeutet nicht automatisch „schlechte Qualität". Es ist ein statistisches Signal. Ob wirklich ein Problem dahintersteckt, klärt ein nachgelagertes Prüfverfahren — der Strukturierte Dialog. Für unsere Analyse genügt das Signal. Wir fragen: **WER** wird häufiger auffällig — nicht **WARUM**.

---

### Folie 8 — Die 86 Dateien: Wie haben wir uns orientiert?
**Inhalt:**
Dateistruktur-Baum (vereinfacht):
```
Data/
├── SO.*    Stammdaten Krankenhaus      → Merkmale (A-Teil)  ✅
├── QS.*    Qualitätssicherung          → Ziel-Variable (C-Teil)  ✅
├── FA.*    Fachabteilungen + Personal  → Merkmale (A-Teil)  ✅
├── MM.*    Mindestmengen               ⚠️ identifiziert
├── AM.*    Ausstattung                 ⚠️ identifiziert
└── NM.*    Nicht-medizinische Angebote ❌ irrelevant
```

**Was gesagt wird:**  
Wir konnten nicht alle 86 Dateien manuell durchlesen. Stattdessen haben wir systematisch gearbeitet: Dateinamen lesen → Spaltenheader einlesen → Beispielzeilen prüfen → Relevanz bewerten. Der Schlüssel war die Entdeckung: Fast alle Tabellen teilen eine einzige gemeinsame Spalte — `SO.QBID`. Das ist unsere universelle Krankenhaus-ID.

---

### Folie 9 — SO.QBID: Der universelle Schlüssel
**Inhalt:**
Einfaches Datenmodell-Diagramm:
```
SO.csv (Haupttabelle)
  │ SO.QBID
  ├──► QS.Qualitätsindikator.csv  ← ZIEL-VARIABLE
  ├──► QS.Fortbildung.csv         ← Merkmal: Fortbildungsquote
  └──► FA.csv ──► FA.Personalliste.csv  ← Merkmal: Ärzte/Bett
```

**Was gesagt wird:**  
`SO.QBID` erscheint in ~60 der 86 Dateien. Das war unsere erste große Erkenntnis: Wer diesen Schlüssel kennt, kann alles zusammenführen. Das hat uns Stunden manuellem Durchsuchen erspart.

---

## BLOCK 3 — Vorgehen & Datenvorbereitung (Folien 10–14) · ca. 14 Min

---

### Folie 10 — Unser Vorgehen: 6 Schritte
**Inhalt (Timeline / Schritt-für-Schritt):**

| Schritt | Was | Datei |
|---------|-----|-------|
| 1 | Stammdaten laden & Merkmale auswählen | `SO.csv` |
| 2 | Qualitätsindikatoren erkunden | `QS.Qualitätsindikator.csv` (911 MB!) |
| 3 | Ziel-Variable berechnen | → `hat_viele_Probleme` |
| 4 | Fortbildungsquote berechnen | `QS.Fortbildung.csv` |
| 5 | Analysetabelle zusammenführen | → `analysetabelle.csv` |
| 6 | Ärzte pro Bett berechnen | `FA.Personalliste.csv` + `FA.csv` |

**Was gesagt wird:**  
Alle Schritte wurden vollständig reproduzierbar in Python durchgeführt. Kein manuelles Zusammenklicken — wer das Notebook ausführt, bekommt dasselbe Ergebnis.

---

### Folie 11 — Die Ziel-Variable: Wie haben wir sie gebaut?
**Inhalt (Flowchart):**
```
QS.Qualitätsindikator.csv
    ↓ Filter: nur echte QI (ArtDesWertes = "QI")
    ↓ Filter: N99 ausschließen (nicht bewertet ≠ unauffällig!)
    ↓ Deduplizierung: je Haus + Indikator eine Zeile
    ↓ Flag: R* = auffällig (1), N* = nicht auffällig (0)
    ↓ Aggregation: auffällig_quote = auffällig_n / total_qi
    ↓ Schwelle: Median → hat_viele_Probleme = 1 oder 0
```

**Was gesagt wird:**  
Drei Fallstricke, die uns fast eine falsche Zielgröße geliefert hätten: N99 (nicht bewertet ist nicht dasselbe wie gut!), doppelte Einträge (ohne Deduplizierung würde jeder Indikator mehrfach zählen) und falsche Indikator-Typen (EKez, TKez sind Zählkennzahlen, keine echten QI).

---

### Folie 12 — Warum Median als Schwelle?
**Inhalt:**
- Median der `auffaellig_quote`: **76,92 %**
- Das bedeutet: das typische Haus hat **~77 % seiner Indikatoren im auffälligen Bereich**
- Häuser über dem Median → `hat_viele_Probleme = 1` (~49 %)
- Häuser unter dem Median → `hat_viele_Probleme = 0` (~51 %)

**Visualisierung:** Histogramm der `auffaellig_quote` mit Median-Linie eingezeichnet

**Was gesagt wird:**  
76 % klingt erschreckend hoch. Aber das zeigt eher, wie hoch die Anforderungen der Referenzbereiche gesetzt sind — und bestätigt nochmals: „auffällig" ist kein Qualitätsurteil. Der Median teilt die Häuser fair in zwei gleich große Gruppen — besser als ein willkürlicher fester Schwellenwert.

---

### Folie 13 — Die Merkmale (Features X)
**Inhalt (Tabelle):**

| Merkmal | Quelle | Typ |
|---------|--------|-----|
| `SO.Betten` | `SO.csv` | Numerisch |
| `KH.Träger.Art` | `SO.csv` | Kategorial: privat / freigemeinnützig / öffentlich |
| `SO.Bundesland` | `SO.csv` | Kategorial: 16 Bundesländer |
| `SO.Uni` | `SO.csv` | Binär: Uni-Klinik ja/nein |
| `fortbildungsquote` | `QS.Fortbildung.csv` | Numerisch 0–1 |
| `aerzte_pro_bett` | `FA.Personalliste.csv` + `FA.csv` | Numerisch |

**Was gesagt wird:**  
Die meisten Merkmale kamen direkt aus SO.csv. Nur `aerzte_pro_bett` war technisch aufwändiger — weil die Personaldaten über zwei Joins verknüpft werden mussten, und weil die Zahlen als Komma-Dezimal gespeichert waren (z. B. `"13,47"` statt `13.47`).

---

### Folie 14 — Die Analysetabelle: Das zentrale Ergebnis der Vorbereitung
**Inhalt:**
- `analysetabelle.csv` — **eine Zeile = ein Krankenhaus**
- **~1.824 Zeilen · 15 Spalten**
- Fehlende Werte: `KH.Träger.Art` (28 fehlend, <2 %) · `fortbildungsquote` (33 fehlend, <2 %)
- Tageskliniken (0 Betten): `aerzte_pro_bett` = NaN — korrekt, kein stationäres Profil

**Visualisierung:** Screenshot der ersten 5 Zeilen der Analysetabelle (anonymisiert oder mit echten Daten)

**Was gesagt wird:**  
Diese Tabelle ist der Startpunkt für alles Weitere: Analyse, Dashboard, Decision Tree. Das Prinzip: Rohdaten → Analysetabelle → alles andere. Wer die Tabelle hat, braucht die 86 Rohdateien für die Analyse nicht mehr.

---

## BLOCK 4 — Ergebnisse der Analyse (Folien 15–21) · ca. 16 Min

---

### Folie 15 — Befund 1: Verteilung der Auffälligkeit
**Inhalt:**
- Grafik 1 (Histogramm der `auffaellig_quote`)
- Median: 76,92 % · Min: ~20 % · Max: ~100 %
- Verteilung: linkssteil — die meisten Häuser liegen zwischen 60–90 %

**Was gesagt wird:**  
Das Erste, was wir uns angeschaut haben: Wie sieht unsere Ziel-Variable eigentlich aus? Ist sie sinnvoll verteilt? Die Antwort: Ja. Kein extremes Ungleichgewicht, keine Auffälligkeit bei 0 oder 100 % — die Verteilung ist plausibel.

---

### Folie 16 — Befund 2: Bettenzahl
**Inhalt:**
- Grafik 2 (Box-Plot: `SO.Betten` gruppiert nach `hat_viele_Probleme`)
- Median wenige Probleme: **~200 Betten** · Median viele Probleme: **~200 Betten**
- **Kein klarer Größenunterschied**

**Was gesagt wird:**  
Erster Gedanke war: Große Häuser sind vielleicht schlechter, weil sie mehr Fälle haben und mehr Indikatoren ausgewertet werden. Das stimmt aber nicht — die Bettenzahl allein erklärt kaum etwas.

---

### Folie 17 — Befund 3: Trägerschaft
**Inhalt:**
- Grafik 3 (Balkendiagramm: Anteil `hat_viele_Probleme = 1` je Trägerart)
- Privat: **56,5 %** haben viele Probleme
- Freigemeinnützig: **46,4 %**
- Öffentlich: **46,7 %**

**Visualisierung:** Farbige Balken — rot für Anteil mit vielen Problemen, grün für ohne

**Was gesagt wird:**  
Das ist unser klarster inhaltlicher Befund. Private Häuser sind öfter auffällig. Aber — und das ist entscheidend — das müssen wir mit Vorsicht interpretieren. Warum, zeige ich auf der nächsten Folie.

---

### Folie 18 — Störfaktor: Träger & Größe
**Inhalt:**
- Grafik 10 (Box-Plot: `SO.Betten` je Trägerart)
- Private Häuser: Median **~90 Betten** (viel kleiner!)
- Freigemeinnützig: Median **~200 Betten**
- Öffentlich: Median **~260 Betten**

**Was gesagt wird:**  
Private Häuser sind im Median deutlich kleiner. Kleine Häuser haben weniger Fälle pro Indikator — das erhöht die Schwankungsbreite und damit das Risiko, außerhalb des Referenzbereichs zu liegen. Der Trägereffekt könnte also ein Größeneffekt sein. Das zeigt: Korrelation ist nicht Kausalität — und man sollte immer fragen, ob hinter einem gefundenen Zusammenhang noch etwas anderes steckt.

---

### Folie 19 — Befund 4: Bundesland & Uni-Status
**Inhalt (zwei Mini-Grafiken):**
- Grafik 7: Bundesland-Balken — Saarland höchster Anteil (63 %), Berlin niedrigster (33 %)
- Grafik 4: Uni-Kliniken vs. normale Häuser — **kaum Unterschied** (50 % vs. 49 %)

**Was gesagt wird:**  
Regionale Unterschiede sind sichtbar, aber bei kleinen Bundesländern mit wenigen Häusern ist die statistische Aussagekraft begrenzt. Uni-Kliniken zeigen überraschend keinen Vorteil — möglicherweise weil sie komplexere Fälle behandeln und deshalb öfter an die Grenzen der Referenzbereiche stoßen.

---

### Folie 20 — Befund 5: Ärzte pro Bett & Fortbildungsquote
**Inhalt (zwei Box-Plots nebeneinander):**
- `aerzte_pro_bett`: Wenige Probleme: Md = 0,37 · Viele Probleme: Md = 0,33 → **leichter Unterschied**
- `fortbildungsquote`: Wenige Probleme: Md = 0,98 · Viele Probleme: Md = 0,98 → **kein Unterschied**

**Was gesagt wird:**  
Fortbildungsquote zeigt fast keine Korrelation mit der Ziel-Variable — obwohl sie explizit in der Aufgabenstellung genannt wurde. Das ist aber kein Fehler, sondern ein Befund: Die Fortbildungsquote allein erklärt die Auffälligkeitsquote nicht. Ärzte pro Bett zeigt einen kleinen, aber messbaren Unterschied.

---

### Folie 21 — Korrelationsmatrix: Die Gesamtübersicht
**Inhalt:**
- Grafik 8 (Heatmap der Korrelationen)
- Stärkste Korrelationen mit `hat_viele_Probleme`:
  - `total_qi` (Anzahl bewerteter Indikatoren): r = **−0,28**
  - `aerzte_pro_bett`: r = **−0,14**
  - `SO.Betten`: r ≈ **−0,10**
  - `fortbildungsquote`: r ≈ **0,01** (kein Zusammenhang)

**Was gesagt wird:**  
Der stärkste Prädiktor ist `total_qi` — also wie viele Indikatoren ein Haus überhaupt bewertet hat. Häuser mit mehr bewerteten Indikatoren haben tendenziell niedrigere Auffälligkeitsquoten. Das ist kein Qualitätsmerkmal, sondern ein strukturelles Merkmal — vielleicht weil größere Häuser mehr Routine haben. Inhaltlich der überraschendste Befund.

---

## BLOCK 5 — Decision Tree & Dashboard (Folien 22–24) · ca. 10 Min

---

### Folie 22 — Decision Tree: Das Modell
**Inhalt:**
- Algorithmus: `DecisionTreeClassifier`, `max_depth=3`
- Training: 80 % der Daten · Test: 20 %
- Basislinie (Raten): ~50 % Accuracy (ausgewogene Klassen)
- Modell-Accuracy auf Testdaten: **~58–62 %**
- Feature Importance: `aerzte_pro_bett` dominiert mit **71,3 %**

**Visualisierung:** Kleines Baumdiagramm (max_depth=3, lesbar)

**Was gesagt wird:**  
Das Modell ist bewusst einfach gehalten. Es geht nicht darum, das cleverste Modell zu bauen, sondern das erklärbarste. Und der Baum sagt klar: Das einzige Merkmal, das wirklich unterscheidet, ist `aerzte_pro_bett`. Alle anderen Merkmale spielen eine untergeordnete Rolle.

---

### Folie 23 — Dashboard: Live-Demo
**Inhalt:**
- 4 interaktive Seiten:
  - 📊 **Übersicht:** KPI-Karten + Deutschland-Karte
  - 🔍 **Vergleiche:** Dropdown für Merkmalsvergleich mit Befundtext
  - 🏨 **Ähnliche Häuser:** Filter → ähnliche Häuser + Qualitätsvergleich
  - ⚠️ **Risiko-Rechner:** Merkmale eingeben → Decision Tree sagt Risiko voraus
- Live unter: `qualitaets-muster-finder.streamlit.app`

**Was gesagt wird:**  
Jetzt zeige ich das Dashboard live. Die wichtigste Seite für unsere Fragestellung ist Seite 2 — die Vergleichsseite. Dort kann man für jedes Merkmal direkt sehen, ob sich die beiden Gruppen unterscheiden. Und Seite 4 zeigt, wie eine einfache Vorhersage aussieht — inklusive Unsicherheitsangabe.

*→ Hier: Live-Demo durchführen (ca. 3–4 Min)*

---

### Folie 24 — Dashboard: Technische Umsetzung
**Inhalt:**
- **Sprache:** Python 3 · **Framework:** Streamlit
- **Datenbasis:** `analysetabelle.csv` (wird einmal geladen)
- **Modell:** `modell_krankenhaus.pkl` (gespeichert mit `joblib`, wird nicht neu trainiert)
- **Deployment:** Streamlit Community Cloud (kostenlos, öffentlich)
- **Reproduzierbarkeit:** `requirements.txt` → `pip install -r requirements.txt` → `streamlit run Dashboard/streamlit_dashboard.py`

**Was gesagt wird:**  
Das Dashboard läuft nicht lokal, sondern öffentlich im Internet. Wer es öffnen will, braucht nur den Link — kein Python, keine Installation. Die Startanleitung im README.md erklärt, wie man es lokal replizieren kann.

---

## BLOCK 6 — Reflexion & Abschluss (Folien 25–27) · ca. 8 Min

---

### Folie 25 — Gesamteinschätzung: Was haben wir gefunden?
**Inhalt (Ampel-Tabelle):**

| Merkmal | Zusammenhang mit Auffälligkeit? |
|---------|--------------------------------|
| Bettenzahl | 🟡 Sehr schwach |
| Trägerschaft | 🟡 Leicht — aber Störfaktor Größe beachten |
| Bundesland | 🟡 Sichtbar — aber kleine Stichproben |
| Uni-Status | 🔴 Kaum vorhanden |
| Fortbildungsquote | 🔴 Kein Zusammenhang |
| Ärzte pro Bett | 🟢 Schwach, aber stärkster Prädiktor |

**Was gesagt wird:**  
Das Ergebnis: Wir finden keine starken, eindeutigen Zusammenhänge. Das ist — wie wir am Anfang gesagt haben — ein valides Ergebnis. Es bedeutet wahrscheinlich: Die Struktur eines Hauses erklärt allein noch nicht, wie gut es bei Qualitätsindikatoren abschneidet. Andere Faktoren spielen eine größere Rolle.

---

### Folie 26 — Grenzen der Analyse
**Inhalt:**
- **Patientenmix:** Häuser mit schwierigeren Patienten fallen häufiger außerhalb des Referenzbereichs — das liegt nicht an schlechter Qualität
- **Dokumentationsqualität:** Manche Auffälligkeiten sind Dokumentationsfehler, keine echten Qualitätsprobleme
- **Kein Kausalitätsnachweis:** Korrelation ≠ Kausalität — auch bei gefundenen Zusammenhängen
- **Fehlende Merkmale:** Pflegekräfte pro Bett wurde noch nicht eingebunden, Konzernzugehörigkeit fehlt
- **N99-Problematik:** Häuser mit wenig Fällen haben mehr N99 → systematische Verzerrung möglich

**Was gesagt wird:**  
Ein ehrlicher Umgang mit Grenzen gehört zu einer guten Datenanalyse. Wir haben uns bemüht, keine Korrelation „zurechtbiegen" — und wenn die Daten nichts zeigen, sagen wir das klar.

---

### Folie 27 — Fazit & Ausblick
**Inhalt:**
**Was wir gelernt haben:**
- Echte Daten sind unordentlich — Datenvorbereitung ist die eigentliche Arbeit
- „Kein Ergebnis" ist ein ehrlicheres Ergebnis als ein erzwungenes
- Reproduzierbarkeit ist nicht optional — sie ist Qualitätsmerkmal der Analyse

**Was als nächstes kommen könnte:**
- Pflegekräfte pro Bett einbinden
- Patientenmix als Kontrollvariable einführen (z. B. Fallschwere-Index)
- Mehrstufige Analyse: erst nach Träger gruppieren, dann innerhalb vergleichen
- Zeitreihe: Vergleich 2021 → 2022 → 2023

**Abschlusssatz:**  
> *„Wir haben 86 Dateien und 1,2 GB Daten systematisch erkundet, eine saubere Analysetabelle gebaut, ein interaktives Dashboard deployed — und gelernt, dass ein sauber begründetes ‚Wir finden nichts' besser ist als eine Korrelation, die man sich zurechtbiegt."*

---

## 💬 Fragen & Diskussion (offen)

*Keine eigene Folie nötig — Titelfolie wieder einblenden*

---

## 📋 Technische Hinweise für die Präsentation

| Punkt | Empfehlung |
|-------|-----------|
| **Foliendesign** | Klares, schlichtes Layout. Keine Animations-Überblendungen. |
| **Schriftgröße** | Mindestens 20pt für Fließtext, 28pt+ für Überschriften |
| **Grafiken** | Aus `grafiken/`-Ordner direkt einfügen (g1_auffaellig_quote.png, g3_traegerschaft.png, g8_korrelation.png, g10_stoerfaktor_traeger.png sind am stärksten) |
| **Demo-Vorbereitung** | Browser mit Dashboard vorab öffnen, Internetverbindung prüfen; Fallback: Screenshots der 4 Seiten als Folie |
| **Zeitkontrolle** | Block 1–2 (Einstieg + Daten): 22 Min · Block 3 (Vorgehen): 14 Min · Block 4 (Ergebnisse): 16 Min · Block 5 (Dashboard): 10 Min · Block 6 (Reflexion): 8 Min |
| **Generalprobe** | Stoppuhr mitlaufen lassen. Ziel: 55 Min Präsentation + 5 Min Puffer für Fragen |

---

*Erstellt: 2026-07-28 | Projekt: Qualitäts-Muster-Finder | Datenbasis: Qualitätsberichte 2023 (IQTIG)*
