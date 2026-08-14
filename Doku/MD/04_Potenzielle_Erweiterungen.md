
# 🔍 04_Potenzielle_Erweiterungen.ipynb — Was wurde gemacht und warum?

> Dieses Dokument erklärt Schritt für Schritt, was im Notebook `Notebooks/04_Potenzielle_Erweiterungen.ipynb` passiert — und warum jeweils so entschieden wurde.  
> **Ergebnis:** Zwei neue Merkmale identifiziert, die die Modellgüte verbessern könnten. Ein drittes wurde getestet und verworfen.

> **⚠️ Korrektur (2026-08-14):** Die Ziel-Variable `hat_viele_Probleme` wurde in `01_Exploration.ipynb` korrigiert (`QSErgBewStrukDialog` war zuvor falsch interpretiert). Dieses Notebook wurde mit der korrigierten `Data/analysetabelle.csv` neu ausgeführt — **alle Korrelationen in diesem Dokument sind neu** und haben sich im Vorzeichen gedreht, konsistent mit der Umkehrung bei allen anderen Merkmalen in `02_Analyse.md`. Die Empfehlungen (Doku-Rate und Notfallstufe einbinden, Mindestmengen nicht) bleiben inhaltlich gleich, aber die Begründungen ändern sich teils deutlich.

**Projektfrage (übergeordnet):** Welche Krankenhausmerkmale hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme aufweist?

---

## Einordnung: Warum dieses Notebook?

`01_Exploration.ipynb` bis `03_Decision_Tree.ipynb` haben mit **7 von 86 CSV-Dateien** gearbeitet. Von den verbleibenden 79 Dateien wurden 33 als „möglicherweise relevant" eingestuft, aber bewusst nicht in die Analysetabelle aufgenommen — aus Zeitgründen und weil die Kernergebnisse auch ohne sie aussagekräftig sind.

Dieses Notebook beantwortet die Folgefrage: **Hätten einzelne dieser Dateien das Modell oder die Analyse nennenswert verbessert?**

**Warum das wichtig ist:**  
Das aktuelle Modell erklärt die Auffälligkeitsquote linear **gar nicht** (R² = −0,007, siehe `03_Decision_Tree.md`) — ein ehrliches, aber ernüchterndes Ergebnis. Wenn unter den nicht eingebundenen Dateien Merkmale stecken, die einen wesentlich stärkeren Zusammenhang zeigen, sollte das für eine Erweiterung bekannt sein. Außerdem gibt es zwei bekannte **Confounders** (störende Drittvariablen), die die bisherigen Ergebnisse verzerren könnten:

1. **Dokumentationsqualität** — Häuser mit lückenhafter Dokumentation fallen häufiger „rechnerisch auffällig", nicht wegen schlechterer Versorgung, sondern wegen fehlender Datensätze.
2. **Fallschwere (Patientenmix)** — Häuser, die die schwersten Fälle behandeln (hohe Notfallstufe), werden an denselben Indikatoren gemessen wie Normalhäuser — ein systematischer Nachteil.

Beide Confounders tauchen im bisherigen Modell nicht auf, weil die nötigen Daten in den bisher nicht eingebundenen Dateien liegen.

---

## 1. Setup & Daten laden

**Was:** `analysetabelle.csv` geladen (1.821 Häuser), Pfade zu `Data/CSV/` gesetzt.

**Warum:** Alle neuen Merkmale werden über `SO.QBID` an die bestehende Analysetabelle gejoint — so bleibt die Analyse konsistent mit `02_Analyse.ipynb` und `03_Decision_Tree.ipynb`.

---

## 2. QS.Leistungsbereich.csv — Dokumentationsrate

### Was ist diese Datei?

`QS.Leistungsbereich.csv` (12 MB) enthält für jedes Krankenhaus und jeden Leistungsbereich (z. B. Geburtshilfe, Mammachirurgie) die **Dokumentationsrate** — also der Anteil der tatsächlich dokumentierten Fälle an der erwarteten Anzahl, ausgedrückt in Prozent.

Eine Dokumentationsrate von 100 % bedeutet: das Haus hat alle Fälle vollständig gemeldet. Eine Rate von 0 % bedeutet: es wurden keine Daten übermittelt — entweder weil keine Fälle stattfanden, oder weil die Dokumentation fehlt.

### Hypothese

Häuser mit **schlechter Dokumentationsrate** fallen häufiger rechnerisch auffällig, weil fehlende oder unvollständige Dokumentation die Bewertungslogik des IQTIG verfälscht. Der Zusammenhang mit `hat_viele_Probleme` wäre dann kein Qualitätssignal, sondern ein **Artefakt der Dokumentationsqualität**.

### Was wurde gemacht?

1. `QSLB.Dokumentationsrate` von Komma-Dezimal auf Punkt umgestellt (deutsches Format `100,0` → `100.0`), dann in Float konvertiert.
2. Mittlere Dokumentationsrate je Krankenhaus berechnet (`groupby('SO.QBID').mean()`).
3. Per Left Join an `analysetabelle.csv` angehängt.
4. Pearson-Korrelation mit `hat_viele_Probleme` berechnet.
5. Boxplot (Doku-Rate nach Problemgruppe) und Histogramm der Verteilung erstellt.

### Ergebnis

```
Match: 1.815 von 1.821 Häusern (99,7 % Match-Rate)
Korrelation mit hat_viele_Probleme: r = +0,208  (p < 0,0001)
```

**Interpretation (korrigiert):** r = +0,208 ist inzwischen **etwas schwächer als `aerzte_pro_bett` (r = +0,210)** aus `02_Analyse.ipynb` — beide liegen praktisch gleichauf. Das Vorzeichen hat sich gedreht: Je höher die Dokumentationsrate, desto **häufiger**, nicht seltener, gehört ein Haus jetzt zur Gruppe „viele Probleme".

Die ursprüngliche Hypothese (lückenhafte Dokumentation täuscht Auffälligkeit vor) hat sich damit **nicht bestätigt**. Der tatsächliche Mechanismus läuft stattdessen über dieselbe Logik wie bei `total_qi` in `02_Analyse.ipynb` (dort die stärkste Korrelation, r = +0,241): Eine höhere Dokumentationsrate bedeutet, dass mehr Indikatoren überhaupt bewertet werden können — und mehr bewertete Indikatoren bedeuten mehr Gelegenheiten, dass einer davon als auffällig eingestuft wird (unter der korrigierten Regel zählt alles außer `R10` als auffällig). Die Dokumentationsrate bleibt trotzdem ein **wichtiger Confounder**, nur mit umgekehrter Wirkrichtung als ursprünglich angenommen.

### Mehrwert

- Vergleichbar starkes Merkmal wie `aerzte_pro_bett`, das aktuell stärkste Merkmal im Decision Tree
- Erklärt sich über denselben Mechanismus wie `total_qi` (Anzahl bewertbarer Indikatoren), nicht über einen Dokumentations-Artefakt wie ursprünglich angenommen
- Empfehlung: **In `analysetabelle.csv` aufnehmen** und `03_Decision_Tree.ipynb` neu trainieren

---

## 3. Notfallversorgung.csv — Notfallversorgungsstufe

### Was ist diese Datei?

`Notfallversorgung.csv` (363 KB) enthält für jedes Krankenhaus, ob und auf welcher Stufe es an der Notfallversorgung teilnimmt:

| Stufe | Bedeutung |
|---|---|
| 0 | Keine Teilnahme an der Notfallversorgung |
| 1 | Basisnotfallversorgung |
| 2 | Erweiterte Notfallversorgung |
| 3 | Umfassende Notfallversorgung (Maximalversorger) |

### Hypothese

Häuser der **höchsten Notfallstufe (3)** behandeln die komplexesten Fälle — Polytrauma, Herzinfarkt, Schlaganfall. Die Qualitätsindikatoren des IQTIG sind aber an typischen Standardfällen kalibriert. Häuser mit Stufe 3 sollten daher häufiger auffällig sein, **nicht weil ihre Qualität schlechter ist, sondern weil ihre Fälle schwieriger sind** (Confounding durch Patientenmix).

### Was wurde gemacht?

1. Die Notfallstufe steckt nicht im Freitext von `TeilnahmeNotfallstufe`, sondern in den Spalten `Stufe1/2/3UmstandZuordnungNotfallstufe` — eine Spalte ist befüllt (NaN = nicht zugeordnet, Wert = zugeordnet). Daraus wurde die Stufe 0–3 extrahiert.
2. Je Haus das Maximum der Stufe gebildet (ein Haus kann in mehreren Leistungsbereichen gelistet sein).
3. Per Left Join an `analysetabelle.csv` angehängt.
4. Anteil `hat_viele_Probleme` je Notfallstufe berechnet.
5. Pearson-Korrelation berechnet.

### Ergebnis

```
Verteilung: Stufe 0 = 957, Stufe 1 = 544, Stufe 2 = 210, Stufe 3 = 116
Match: 1.419 von 1.821 Häusern (77,9 % Match-Rate)

Anteil viele Probleme je Stufe:
  Stufe 0 (keine NV):  34,5 %  (n = 566)
  Stufe 1 (Basis):     62,0 %  (n = 537)
  Stufe 2 (Erweitert): 56,6 %  (n = 205)
  Stufe 3 (Umfassend): 57,7 %  (n = 111)

Korrelation mit hat_viele_Probleme: r = +0,181  (p < 0,0001)
```

**Interpretation (korrigiert):** Das Ergebnis passt jetzt genau zur ursprünglichen Hypothese, ganz ohne Paradox: Stufe 0 (keine Notfallversorgung) hat mit 34,5 % den **niedrigsten** Anteil auffälliger Häuser, alle drei Notfallstufen (1–3) liegen mit 57–62 % deutlich höher — ungefähr gleichauf untereinander, aber klar über Stufe 0. Häuser mit Notfallversorgung behandeln komplexere, schwerere Fälle und fallen dadurch häufiger auffällig, unabhängig von der tatsächlichen Versorgungsqualität. Die in der ursprünglichen, fehlerhaften Auswertung nötige Sonder-Erklärung über den „kleine-Zahlen-Effekt" ist damit hinfällig — das Muster erklärt sich direkt durch Fallschwere.

r = +0,181 ist statistisch stark und bestätigt: die Notfallstufe ist ein **relevanter Strukturindikator**.

### Mehrwert

- Zweitstärkster neu gefundener Zusammenhang (r = +0,181)
- Erklärt direkt und ohne Umweg die höhere Auffälligkeit von Häusern mit Notfallversorgung (Fallschwere-Confounder)
- Empfehlung: **In `analysetabelle.csv` aufnehmen**, besonders als Kontrollvariable für die Fallschwere

---

## 4. MM.csv — Mindestmengen-Compliance

### Was ist diese Datei?

`MM.csv` (236 KB) enthält Mindestmengen-Daten: Hat ein Krankenhaus die gesetzlich vorgeschriebene Mindestfallzahl für bestimmte Eingriffe erreicht? Beispiel: Mindestens 50 Knie-TEP pro Jahr.

Die Join-Kette war komplex: `MM.csv` hat keinen direkten `SO.QBID`, sondern nur `MM.Key`. Über `MM.KeyPrognose` lässt sich an `MM.Leistungsberechtigung.Prognose.csv` joinen, die `MMLBProg.QBID` (= `SO.QBID`) enthält.

### Hypothese

Häuser, die Mindestmengen **nicht** erfüllen, haben möglicherweise weniger Routine bei bestimmten Eingriffen → mehr Qualitätsprobleme.

### Ergebnis

```
Häuser mit Mindestmengen-Daten: 1.018
Match: 1.013 von 1.821 Häusern
Korrelation mit hat_viele_Probleme: r = −0,011  (p = 0,7155)

Median Compliance-Rate:
  Wenige Probleme: 100,0 %
  Viele Probleme:  100,0 %
```

**Interpretation (korrigiert):** Der Median beider Gruppen liegt weiterhin bei 100 % — fast alle Häuser mit Mindestmengen-Daten erfüllen die Vorgaben vollständig. Es gibt kaum Differenzierung zwischen den Gruppen. Die Korrelation ist mit der korrigierten Ziel-Variable sogar noch schwächer geworden und jetzt **nicht mehr statistisch signifikant** (r = −0,011, p = 0,7155 — vorher r = +0,071, p = 0,025). Zudem deckt die Datei nur 1.018 von 1.821 Häusern ab (Häuser ohne bestimmte Eingriffe haben gar keine Mindestmengen-Pflicht).

### Mehrwert

Keiner für die aktuelle Analyse. Empfehlung: **Nicht einbinden** — zu geringe Varianz, zu viele fehlende Werte.

---

## 5. Fazit & Empfehlungen

| Datei | Merkmal | r | p | Empfehlung |
|---|---|---|---|---|
| `QS.Leistungsbereich.csv` | mittl_doku_rate | **+0,208** | < 0,0001 | ✅ Einbinden — starker Zusammenhang |
| `Notfallversorgung.csv` | notfall_stufe (0–3) | **+0,181** | < 0,0001 | ✅ Einbinden — erklärt Fallschwere |
| `MM.csv` | mm_compliance_rate | −0,011 | 0,7155 | ❌ Nicht einbinden — kein signifikanter Effekt, Median 100 % in beiden Gruppen |

### Was würde sich ändern, wenn man die zwei empfohlenen Merkmale einbindet?

1. **Decision Tree:** `mittl_doku_rate` (r = +0,208) liegt jetzt fast gleichauf mit `aerzte_pro_bett` (r = +0,210, aktuell wichtigstes Merkmal mit 72,8 % Feature Importance) — ob es das wichtigste Merkmal ablöst, müsste ein Nachtraining zeigen. Da das aktuelle Modell mit R² = −0,007 praktisch keine lineare Erklärungskraft hat, wäre ein zusätzliches, ähnlich starkes Merkmal ein sinnvoller nächster Versuch, auch wenn ein großer Sprung nicht garantiert ist.
2. **Trägerschaftseffekt:** Entfällt als Motivation — die ANOVA in `02_Analyse.ipynb` zeigt nach der Korrektur **keinen** signifikanten Trägerschaftseffekt mehr (F=0,031, p=0,969), den man mit der Dokumentationsrate erklären müsste.
3. **Erklärbarkeit:** Die Notfallstufe erklärt jetzt direkt und ohne Paradox, warum Häuser mit Notfallversorgung eine höhere Auffälligkeitsquote haben (Fallschwere) — anders als in der ursprünglichen Auswertung, wo Stufe 0 unerwartet am höchsten lag.

### Nächste Schritte

1. `mittl_doku_rate` und `notfall_stufe` in `01_Exploration.ipynb` als neue Spalten in `analysetabelle.csv` aufnehmen
2. `03_Decision_Tree.ipynb` neu trainieren und Feature Importance vergleichen
3. In `02_Analyse.ipynb` einen Gruppenvergleich nach Notfallstufe ergänzen

---

*Zuletzt aktualisiert: 2026-08-14 — vollständig gegen den korrigierten Stand von `Notebooks/04_Potenzielle_Erweiterungen.ipynb` (15 Zellen) abgeglichen. Wichtigste Änderung: Alle Korrelationen mit `hat_viele_Probleme` wurden mit der korrigierten Ziel-Variable neu berechnet und haben sich im Vorzeichen gedreht (Dokumentationsrate: r = +0,208 statt −0,237; Notfallstufe: r = +0,181 statt −0,179, jetzt ohne Paradox; Mindestmengen: r = −0,011, nicht mehr signifikant statt r = +0,071, p = 0,025).*
