# 📖 IQTIG.md — Erkenntnisse aus dem Bundesqualitätsbericht 2023

> Quelle: `Docs/IQTIG_Bundesqualitaetsbericht-2023_2023-11-08.pdf` (lokal vorhanden, nicht versioniert — 25,5 MB, 4.559 Seiten). Dieses Dokument fasst zusammen, was beim Durchsehen relevant für unser Projekt war. Bei 4.559 Seiten wurde nicht linear gelesen, sondern gezielt: Titel-/Metadatenseiten, das vollständige Inhaltsverzeichnis sowie das erste QS-Verfahren (QS PCI, ~170 Seiten) als repräsentatives Beispiel für die Methodik, die sich über alle Verfahren wiederholt.

---

## 1. Dokumentidentität — direkter Beleg für die IQTIG/G-BA-Herkunft

Auf den ersten beiden Seiten steht es explizit:

> „Bundesqualitätsbericht 2023, 8. November 2023, **erstellt im Auftrag des Gemeinsamen Bundesausschusses**“
> „Auftraggeber: **Gemeinsamer Bundesausschuss (G-BA)**“

Das ist die direkte Antwort auf die frühere Frage „Woher weißt du, dass die Rohdaten von IQTIG stammen?“ — der Bericht selbst weist sich unmissverständlich als IQTIG-Produkt im Auftrag des G-BA aus. Wichtig für die eigene Argumentation bleibt aber die Unterscheidung: Der **Bezugsweg** unserer 86 CSV-Dateien (Download vom Dozenten) sagt nichts über die **Datenherkunft** aus — beides ist unabhängig voneinander.

---

## 2. Aufbau des Berichts

Der PDF ist eine gebündelte Sammlung von **15 einzelnen QS-Verfahren-Berichten**, jeweils mit eigenem Titelblatt, Inhaltsverzeichnis, Tabellen- und Abkürzungsverzeichnis:

1. Perkutane Koronarintervention und Koronarangiographie (QS PCI)
2. Vermeidung nosokomialer Infektionen — postoperative Wundinfektionen (QS WI)
3. Cholezystektomie (QS CHE)
4. Nierenersatztherapie bei chronischem Nierenversagen einschließlich Pankreastransplantationen (QS NET)
5. Transplantationsmedizin (QS TX)
6. Koronarchirurgie und Eingriffe an Herzklappen (QS KCHK)
7. Karotis-Revaskularisation (QS KAROTIS)
8. Ambulant erworbene Pneumonie (QS CAP)
9. Mammachirurgie (QS MC)
10. Gynäkologische Operationen (QS GYN-OP)
11. Dekubitusprophylaxe (QS DEK)
12. Versorgung mit Herzschrittmachern und implantierbaren Defibrillatoren (QS HSMDEF)
13. Perinatalmedizin (QS PM)
14. Hüftgelenkversorgung (QS HGV)
15. Knieendoprothesenversorgung (QS KEP)

Jedes Verfahren ist strukturell identisch aufgebaut: **1 Hintergrund** (medizinischer Kontext, Ziele des Verfahrens) → **2 Einordnung der Ergebnisse** (Datengrundlage, Risikoadjustierung, Datenvalidierung, Indikatorenergebnisse) → detaillierte Tabellen pro Qualitätsindikator. Allein QS PCI umfasst ~170 Seiten — bei 15 Verfahren erklärt das die Gesamtlänge von 4.559 Seiten.

---

## 3. Zentrale Begriffe — und eine wichtige Verwechslungsgefahr

### „Rechnerisch auffällig" — bestätigt unser Grundprinzip

Ein Leistungserbringer gilt für einen Indikator als **rechnerisch auffällig**, wenn sein Ergebnis außerhalb eines **Referenzbereichs** liegt. Referenzbereiche sind entweder:
- **perzentilbasiert** (z. B. „≥ 93,65 %; 5. Perzentil" oder „≤ 1,10; 95. Perzentil"), oder
- **risikoadjustiert** über ein Erwartungswertmodell (O/E-Rate — Verhältnis beobachtete zu erwartete Anzahl, unter Berücksichtigung patientenseitiger Risikofaktoren).

Das bestätigt unabhängig, was in unserem Projekt durchgehend betont wird: **„Rechnerisch auffällig" ist ein statistisches Signal, kein automatisches Qualitätsurteil.** Ob ein echtes Problem vorliegt, klärt danach ein Stellungnahmeverfahren mit dem Leistungserbringer — dasselbe Prinzip wie der „Strukturierte Dialog" in unseren eigenen Rohdaten.

### ⚠️ „Auffälligkeitskriterien" bedeutet hier etwas ANDERES

Im Bericht gibt es zusätzlich sogenannte **Auffälligkeitskriterien** — das ist **nicht** dasselbe wie die „rechnerische Auffälligkeit" eines Qualitätsindikators! Auffälligkeitskriterien prüfen stattdessen die **Dokumentationsqualität** der gelieferten Datensätze selbst, in zwei Kategorien:
- **Plausibilität und Vollständigkeit** — z. B. unwahrscheinliche Wertekombinationen innerhalb eines Datensatzes.
- **Vollzähligkeit** — Abgleich der gelieferten Datensätze gegen die „Sollstatistik" (Unter-/Überdokumentation, Minimaldatensätze).

Für unser Projekt relevant, um Begriffe nicht zu verwechseln: Diese „Auffälligkeitskriterien" haben nichts mit unserer Ziel-Variable (`hat_viele_Probleme`, abgeleitet aus `QSErgBewStrukDialog`) zu tun.

### Die Rohdaten-Codes (R10/N/H/U/A/D/S) tauchen in diesem Bericht nicht auf

Wichtige Einschränkung für die Genauigkeit unserer eigenen Dokumentation: Der Bundesqualitätsbericht 2023 beschreibt Ergebnisse **narrativ in Prozentzahlen und Referenzbereichen** ("53 von 1.068 Leistungserbringern, 4,96 %"), nicht als die literalen Rohdaten-Codes (`R10`, `N01`/`N02`/`N99`, `H20`/`H99`, `U30–33`/`U99`, `A40–42`/`A99`, `D50`/`51`/`99`, `S90`/`91`/`99`), die unser Projekt aus `QSErgBewStrukDialog` verwendet. Die Verifikation dieses Code-Schemas (Summenprobe H+U+A+D+S) erfolgte in unserem Projekt gegen einen **anderen** IQTIG-Bericht (`Bericht zum Strukturierten Dialog 2021, Erfassungsjahr 2020`) — dieser Bundesqualitätsbericht 2023 ist nicht identisch mit jener Quelle und sollte nicht damit verwechselt werden.

---

## 4. Methodik-Beispiel anhand QS PCI (stellvertretend für alle 15 Verfahren)

**Datenfluss:** Leistungserbringer → Datenannahmestellen (DAS-LKG für Krankenhäuser, DAS-KV für Vertragsärzt:innen, DAS-SV für Selektivverträge) → IQTIG. Für QS PCI im Erfassungsjahr 2022: 712.459 übermittelte QS-Datensätze, nach Bereinigung (Überlieger-Ein-/Ausschluss) 714.881 Datensätze als Auswertungsgrundlage, verglichen gegen 708.421 „Solldaten" zur Vollzähligkeitsprüfung.

**Auffälligkeits-Beispielzahlen** (Indikator 56000, „Objektive, nicht-invasive Ischämiezeichen als Indikation zur elektiven, isolierten Koronarangiographie"): Bundesergebnis 64,25 %, Referenzbereich ≥ 40,97 % (5. Perzentil) → 53 von 1.068 Leistungserbringern (4,96 %) rechnerisch auffällig.

**Wichtiger methodischer Hinweis aus dem Bericht:** Sektorspezifische Auffälligkeits-Teilsummen (ambulant/stationär) addieren sich **nicht** zur bundesweiten Gesamtzahl, weil ein Leistungserbringer je nach Sektor unterschiedlich eingestuft werden kann, aber im eigentlichen Stellungnahmeverfahren nur eine bundesweite Einstufung zählt. Ein methodisch feines Detail, das zeigt, wie vorsichtig IQTIG selbst mit Summierungen über Teilgruppen umgeht — ein guter Vergleichspunkt für die eigene Sorgfalt bei der Analysetabelle.

---

## 5. Fazit für unser Projekt

- **Bestätigt** (nicht nur behauptet): IQTIG erstellt diese Berichte tatsächlich im Auftrag des G-BA — Beleg direkt im Dokument selbst.
- **Bestätigt unabhängig**: das Grundprinzip „auffällig = statistisches Signal, kein automatisches Qualitätsurteil", das unser Projekt durchgehend betont.
- **Zu beachten**: „Auffälligkeitskriterien" (Dokumentationsqualität) und „rechnerisch auffällig" (Indikatorergebnis) sind im IQTIG-Sprachgebrauch zwei verschiedene Dinge — in eigenen Formulierungen nicht vermischen.
- **Ehrlich bleiben**: Dieser konkrete Bericht ist nicht die Quelle unserer Rohdaten-Codes (R10 etc.) und nicht zeilenscharf mit `Data/CSV/QS.Qualitätsindikator.csv` vergleichbar — er ist ein zusätzlicher, unabhängiger Beleg für die Existenz und Funktionsweise des IQTIG/G-BA-Systems, keine direkte Datenquelle für unsere Analysetabelle.
