# 01_Exploration_Ref — Referenzbereich-Nachrechnung

> Dieses Dokument erklärt Schritt für Schritt, was im Notebook `Notebooks/01_Exploration_Ref.ipynb` passiert — ein Exkurs zur Hauptanalyse, kein Ersatz dafür. Es ändert nichts an `Data/analysetabelle.csv` oder der im Projekt verwendeten Ziel-Variable.

**Ausgangsfrage:** `QSErgBewStrukDialog` liefert IQTIGs bereits fertige Bewertung, ob ein Indikator auffällig ist. `QS.Qualitätsindikator.csv` enthält aber zusätzlich die Rohgrößen, aus denen diese Bewertung eigentlich hervorgeht — `QSQI.Ergebnis` (gemessener Wert), `QSQI.Referenzwert` (Schwellenwert) und `QSQI.Operator` (Vergleichsrichtung). Was passiert, wenn wir die Auffälligkeit selbst aus diesen drei Spalten nachrechnen, statt `QSErgBewStrukDialog` einfach zu übernehmen — kommt dasselbe Ergebnis heraus?

**Kurzfassung:** Nein, nicht ganz — mit 96,0 % Übereinstimmung auf Zeilenebene kommt man ziemlich nah heran, aber nicht exakt. Der Grund für die Abweichung ist selbst ein interessanter Befund: Eine einfache Punktwert-Regel ignoriert, dass IQTIG die statistische Unsicherheit jedes Messwerts (Konfidenzintervall) explizit mitberücksichtigt.

---

## 1 — Nur echte Qualitätsindikatoren betrachten

Wie im Hauptnotebook: Zählkennzahlen (`EKez`/`TKez`/`KKez`) sind keine echten Bewertungen und werden ausgeschlossen (`QSQI.ArtDesWertes == 'QI'`).

**Ergebnis (tatsächlicher Notebook-Output):** 417.799 Rohzeilen → 308.726 nach dem QI-Filter.

---

## 2 — Die drei Rohspalten im Detail

### `QSQI.Operator`

Bei rund einem Drittel der Zeilen fehlt er komplett — dort gibt es gar keinen Schwellenwert-Vergleich (meist bei N*-codierten Zeilen, aber nicht nur dort, siehe Abschnitt 5). Zwei Werte kommen vor:

| Wert | Bedeutung | Anzahl Zeilen |
|---|---|---|
| `<=` | Ergebnis soll unter dem Referenzwert bleiben | 174.872 |
| `>=` | Ergebnis soll über dem Referenzwert liegen | 32.972 |
| *(leer)* | Kein Vergleich verfügbar | 100.882 |

Anteil mit Operator vorhanden: **67,3 %**.

### `QSQI.Ergebnis` — die kleine-Zahlen-Maskierung

Der gemessene Wert ist meist eine normale Zahl (Dezimalpunkt, kein Komma). Bei kleinen Fallzahlen maskiert IQTIG den echten Wert aber aus Datenschutzgründen mit dem Text `<=3` — der exakte Wert bleibt damit unbekannt, bekannt ist nur „höchstens 3". Betrifft **70.915 Zeilen (23,0 %)** der QI-Zeilen.

### `QSQI.Referenzwert` — Komma-Dezimalformat

Der Schwellenwert selbst steht im deutschen Komma-Format (z. B. `4,18`) und muss vor der Umrechnung erst in einen Dezimalpunkt konvertiert werden — derselbe Formatfehler-Fallstrick wie bei `FA.Personal.Anzahl` im Hauptnotebook (`str.replace(',', '.')` + `pd.to_numeric`).

---

## 3 — Wie viele Zeilen sind überhaupt selbst berechenbar?

Damit sich eine Auffälligkeit selbst berechnen lässt, müssen gleichzeitig vorliegen: ein echter Zahlenwert bei `QSQI.Ergebnis` (nicht maskiert), ein `QSQI.Referenzwert` und ein `QSQI.Operator`. Die Bereinigung der Rohdaten auf die selbst berechenbare Teilmenge läuft in zwei Schritten:

**Ergebnis (tatsächlicher Notebook-Output):**

| Schritt | Zeilen danach | Entfernt |
|---|---:|---:|
| Ausgangsdatensatz (nach QI-Filter) | 308.726 | — |
| 1. `QSQI.Operator` vorhanden | 207.844 | 100.882 |
| 2. `QSQI.Ergebnis` ist echte Zahl (nicht maskiert) | 111.061 | 96.783 |

`QSQI.Referenzwert` ist bei der nach Schritt 2 verbleibenden Menge in jedem Fall bereits vorhanden (0 weitere Verluste) — die drei Spalten werden von IQTIG offenbar immer gemeinsam befüllt oder gemeinsam leer gelassen. Nur **111.061 von 308.726 Zeilen (36,0 %)** erfüllen damit alle drei Bedingungen gleichzeitig.

---

## 4 — Eigene Bewertung berechnen und mit `QSErgBewStrukDialog` vergleichen

**Regel:** Bei Operator `<=` ist ein Haus unauffällig, wenn `Ergebnis <= Referenzwert`; bei `>=` unauffällig, wenn `Ergebnis >= Referenzwert`. Verglichen wird nur mit Zeilen, die auch offiziell bewertet sind (kein N*-Code) — 110.975 Zeilen.

**Kreuztabelle (tatsächlicher Notebook-Output):**

| eigene Bewertung ↓ / offizielle Bewertung → | nicht auffällig (0) | auffällig (1) |
|---|---:|---:|
| **nicht auffällig (0)** | 100.597 | 8 |
| **auffällig (1)** | 4.416 | 5.954 |

**Übereinstimmung: 96,01 %.** Schon mit der simplen Punktwert-Regel kommt man ziemlich nah an IQTIGs Bewertung heran — aber eben nicht exakt. 4.416 Zeilen stuft die eigene Regel als auffällig ein, wo IQTIG „nicht auffällig" (R10) sagt; nur 8 Zeilen andersherum. Die Asymmetrie (fast alle Abweichungen in dieselbe Richtung) ist der erste Hinweis, dass hier kein zufälliges Rauschen vorliegt, sondern ein systematischer Grund.

---

## 5 — Der Grund für die Abweichung: Konfidenzintervalle

`QS.Qualitätsindikator.csv` enthält eine weitere Spalte, die die einfache Regel ignoriert hat: `QSQI.KHVertrauensbereich` — das **Konfidenzintervall** des Hauses um seinen eigenen Messwert. IQTIGs tatsächliche Regel ist offenbar kein reiner Punktvergleich, sondern ein statistischer Test: Ein Haus gilt nur dann als auffällig, wenn der Referenzwert **außerhalb** seines Konfidenzintervalls liegt. Liegt der Referenzwert innerhalb (die Abweichung könnte also statistisches Rauschen sein), bleibt das Haus unauffällig — selbst wenn der reine Punktwert über dem Referenzwert liegt.

**Beispiel aus den Daten:** Ergebnis 1,21, Referenzwert 1,10 (Operator `<=`) → nach der naiven Regel „auffällig", weil 1,21 > 1,10. Tatsächliches Konfidenzintervall des Hauses: 0,66–2,04 — der Referenzwert 1,10 liegt mittendrin. IQTIGs offizielle Bewertung: R10 (nicht auffällig), zu Recht.

**Ergebnis (tatsächlicher Notebook-Output):** Bei **99,46 % der 4.416 Abweichungen** liegt der Referenzwert im Konfidenzintervall des Hauses — das erklärt praktisch die gesamte Diskrepanz.

---

## 6 — Hochrechnung auf Hausebene: Würde sich die Ziel-Variable ändern?

Dieselbe Frage jetzt für die eigentliche Ziel-Variable: Wenn `auffaellig_quote` und `hat_viele_Probleme` mit der eigenen (naiven) Bewertung statt mit `QSErgBewStrukDialog` berechnet würden — käme dieselbe Analysetabelle heraus?

Dafür wurden die 111.061 selbst berechenbaren Zeilen genauso dedupliziert wie im Hauptnotebook (`SO.QBID` + `QSQI.Indikator`, 45.308 Zeilen verbleiben) und pro Haus zusammengefasst.

| Kennzahl | Eigene Berechnung | Offiziell (`analysetabelle.csv`) |
|---|---:|---:|
| Häuser abgedeckt | 1.710 | 1.821 |
| Ø Indikatoren pro Haus | 26,5 | 42,6 |
| Median auffaellig_quote | 5,00 % | 5,88 % |

**Direkter Vergleich bei den 1.710 gemeinsamen Häusern (93,9 % der 1.821):**

- Korrelation eigene vs. offizielle Haus-Quote: **r = 0,742**
- Übereinstimmung der Gruppenzuordnung (eigener Median-Split vs. offizielles `hat_viele_Probleme`): **75,9 %**

Eine Korrelation von 0,74 ist nicht schwach — aber auf Ebene der binären Gruppenzuordnung, mit der im Projekt tatsächlich gearbeitet wird, würde jedes vierte Haus (24,1 %) in die jeweils andere Gruppe fallen als mit der offiziellen Bewertung.

---

## 7 — Fazit

Zwei unabhängige Gründe, warum eine Eigenberechnung schlechter wäre als die Übernahme von `QSErgBewStrukDialog`:

1. **Geringere Datenbasis.** Nur 36 % der Zeilen sind überhaupt selbst berechenbar (fehlender Referenzwert/Operator bei rund einem Drittel der Zeilen, dazu die aus Datenschutzgründen maskierten Kleinzahl-Ergebnisse). 111 Häuser (6,1 % von 1.821) hätten gar keine einzige selbst berechenbare Zeile mehr — deutlich mehr als die 3 Häuser, die bei der offiziellen Methode verloren gehen (siehe Abschnitt 1.4/2.2 der Hauptdokumentation). Bei den verbleibenden 1.710 Häusern stehen im Schnitt 26,5 statt 42,6 Indikatoren zur Verfügung — 38 % weniger Datenbasis pro Haus.
2. **Fehlende Konfidenzintervall-Korrektur.** Eine naive Punktwert-vs-Referenzwert-Regel ignoriert, dass IQTIG die statistische Unsicherheit des Messwerts explizit berücksichtigt. Genau das erklärt praktisch alle Abweichungen auf Zeilenebene (99,5 %).

**Schlussfolgerung:** Die im Hauptprojekt getroffene Entscheidung, `QSErgBewStrukDialog` direkt zu übernehmen statt die Auffälligkeit selbst aus Ergebnis, Referenzwert und Operator nachzurechnen, war richtig. IQTIGs fertige Bewertung ist vollständiger (mehr Häuser, mehr Indikatoren pro Haus) und methodisch genauer (berücksichtigt Konfidenzintervalle), als es eine einfache Eigenberechnung leisten könnte — ein zusätzlicher, unabhängiger Beleg dafür, dass die im Hauptprojekt gewählte Methode (Übernahme der offiziellen Bewertung statt Nachrechnen) die richtige war.
