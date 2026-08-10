
# 🔍 04_Potenzielle_Erweiterungen.ipynb — Was wurde gemacht und warum?

> Dieses Dokument erklärt Schritt für Schritt, was im Notebook `Notebooks/04_Potenzielle_Erweiterungen.ipynb` passiert — und warum jeweils so entschieden wurde.  
> **Ergebnis:** Zwei neue Merkmale identifiziert, die die Modellgüte verbessern könnten. Ein drittes wurde getestet und verworfen.

**Projektfrage (übergeordnet):** Welche Krankenhausmerkmale hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme aufweist?

---

## Einordnung: Warum dieses Notebook?

`01_Exploration.ipynb` bis `03_Decision_Tree.ipynb` haben mit **7 von 86 CSV-Dateien** gearbeitet. Von den verbleibenden 79 Dateien wurden 33 als „möglicherweise relevant" eingestuft, aber bewusst nicht in die Analysetabelle aufgenommen — aus Zeitgründen und weil die Kernergebnisse auch ohne sie aussagekräftig sind.

Dieses Notebook beantwortet die Folgefrage: **Hätten einzelne dieser Dateien das Modell oder die Analyse nennenswert verbessert?**

**Warum das wichtig ist:**  
Das aktuelle Modell erklärt nur **3,3 % der Varianz** (R² = 0,033) — ein ehrliches, aber bescheidenes Ergebnis. Wenn unter den nicht eingebundenen Dateien Merkmale stecken, die einen wesentlich stärkeren Zusammenhang zeigen, sollte das für eine Erweiterung bekannt sein. Außerdem gibt es zwei bekannte **Confounders** (störende Drittvariablen), die die bisherigen Ergebnisse verzerren könnten:

1. **Dokumentationsqualität** — Häuser mit lückenhafter Dokumentation fallen häufiger „rechnerisch auffällig", nicht wegen schlechterer Versorgung, sondern wegen fehlender Datensätze.
2. **Fallschwere (Patientenmix)** — Häuser, die die schwersten Fälle behandeln (hohe Notfallstufe), werden an denselben Indikatoren gemessen wie Normalhäuser — ein systematischer Nachteil.

Beide Confounders tauchen im bisherigen Modell nicht auf, weil die nötigen Daten in den bisher nicht eingebundenen Dateien liegen.

---

## 1. Setup & Daten laden

**Was:** `analysetabelle.csv` geladen (1.824 Häuser), Pfade zu `Data/CSV/` gesetzt.

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
Match: 1.817 von 1.824 Häusern (99,6 % Match-Rate)
Korrelation mit hat_viele_Probleme: r = −0,237  (p < 0,001)
```

**Interpretation:** r = −0,237 ist **stärker als Ärzte pro Bett (r = −0,14)** — das stärkste Merkmal im bisherigen Modell. Das negative Vorzeichen bedeutet: Je höher die Dokumentationsrate, desto seltener gehört ein Haus zur Gruppe „viele Probleme".

Das ist inhaltlich plausibel: Ein Haus mit lückenhafter Dokumentation wird vom IQTIG häufiger als auffällig bewertet, weil fehlende Datensätze statistisch wie negative Bewertungen zählen. Die Dokumentationsrate ist damit ein **wichtiger Confounder**, der in der bisherigen Analyse nicht kontrolliert wurde.

### Mehrwert

- Stärkstes neu gefundenes Merkmal
- Erklärt möglicherweise einen Teil des Trägerschaftseffekts (private Häuser sind im Schnitt kleiner und haben weniger Kapazität für vollständige QS-Dokumentation)
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
Match: 1.421 von 1.824 Häusern (77,9 % Match-Rate)

Anteil viele Probleme je Stufe:
  Stufe 0 (keine NV):  62,9 %  (n = 568)
  Stufe 1 (Basis):     37,2 %  (n = 537)
  Stufe 2 (Erweitert): 39,0 %  (n = 205)
  Stufe 3 (Umfassend): 41,4 %  (n = 111)

Korrelation mit hat_viele_Probleme: r = −0,179  (p < 0,001)
```

**Interpretation:** Das Ergebnis ist auf den ersten Blick paradox — Stufe 0 hat den **höchsten** Anteil auffälliger Häuser (62,9 %), nicht Stufe 3 wie erwartet. Das hat eine strukturelle Erklärung: Häuser **ohne** Notfallversorgung sind im Schnitt kleine Häuser mit wenigen Fällen pro Indikator. Wenige Fälle bedeuten hohe statistische Schwankungsbreite — schon ein oder zwei auffällige Indikatoren genügen für eine Quote über dem Median. Das ist derselbe kleine-Zahlen-Effekt wie bei der 100 %-Spitze in Grafik 1 von `02_Analyse.ipynb`.

Dennoch: r = −0,179 ist statistisch stark und zeigt, dass die Notfallstufe ein **relevanter Strukturindikator** ist.

### Mehrwert

- Zweitstärkster neu gefundener Zusammenhang (r = −0,179)
- Erklärt den kleinen-Häuser-Effekt und den paradoxen Befund zu Stufe 0
- Empfehlung: **In `analysetabelle.csv` aufnehmen**, besonders als Kontrollvariable für Stufe 0

---

## 4. MM.csv — Mindestmengen-Compliance

### Was ist diese Datei?

`MM.csv` (236 KB) enthält Mindestmengen-Daten: Hat ein Krankenhaus die gesetzlich vorgeschriebene Mindestfallzahl für bestimmte Eingriffe erreicht? Beispiel: Mindestens 50 Knie-TEP pro Jahr.

Die Join-Kette war komplex: `MM.csv` hat keinen direkten `SO.QBID`, sondern nur `MM.Key`. Über `MM.KeyPrognose` lässt sich an `MM.Leistungsberechtigung.Prognose.csv` joinen, die `MMLBProg.QBID` (= `SO.QBID`) enthält.

### Hypothese

Häuser, die Mindestmengen **nicht** erfüllen, haben möglicherweise weniger Routine bei bestimmten Eingriffen → mehr Qualitätsprobleme.

### Ergebnis

```
Häuser mit Mindestmengen-Daten: 1.018 (von 1.824 Häusern)
Korrelation mit hat_viele_Probleme: r = +0,071  (p = 0,025)

Median Compliance-Rate:
  Wenige Probleme: 100,0 %
  Viele Probleme:  100,0 %
```

**Interpretation:** Der Median beider Gruppen liegt bei 100 % — fast alle Häuser mit Mindestmengen-Daten erfüllen die Vorgaben vollständig. Es gibt kaum Differenzierung zwischen den Gruppen. Die schwache positive Korrelation (r = +0,071) ist statistisch zwar signifikant (p = 0,025), aber inhaltlich nicht bedeutsam. Zudem deckt die Datei nur 1.018 von 1.824 Häusern ab (Häuser ohne bestimmte Eingriffe haben gar keine Mindestmengen-Pflicht).

### Mehrwert

Keiner für die aktuelle Analyse. Empfehlung: **Nicht einbinden** — zu geringe Varianz, zu viele fehlende Werte.

---

## 5. Fazit & Empfehlungen

| Datei | Merkmal | r | p | Empfehlung |
|---|---|---|---|---|
| `QS.Leistungsbereich.csv` | mittl_doku_rate | **−0,237** | < 0,001 | ✅ Einbinden — stärkster neuer Zusammenhang |
| `Notfallversorgung.csv` | notfall_stufe (0–3) | **−0,179** | < 0,001 | ✅ Einbinden — erklärt Fallschwere und kleinen-Häuser-Effekt |
| `MM.csv` | mm_compliance_rate | +0,071 | 0,025 | ❌ Nicht einbinden — Median 100 % in beiden Gruppen |

### Was würde sich ändern, wenn man die zwei empfohlenen Merkmale einbindet?

1. **Decision Tree:** `mittl_doku_rate` (r = −0,237) würde `aerzte_pro_bett` (r = −0,14) als wichtigstes Merkmal ablösen. Die Accuracy würde voraussichtlich von 63,6 % steigen.
2. **Trägerschaftseffekt:** Der Befund „private Häuser haben mehr Probleme" (Folie 9 / `02_Analyse.ipynb`) könnte sich abschwächen, wenn die Dokumentationsrate kontrolliert wird — private Häuser sind kleiner und dokumentieren möglicherweise lückenhafter.
3. **Erklärbarkeit:** Die Notfallstufe erklärt, warum Stufe-0-Häuser paradoxerweise die höchste Auffälligkeitsquote haben.

### Nächste Schritte

1. `mittl_doku_rate` und `notfall_stufe` in `01_Exploration.ipynb` als neue Spalten in `analysetabelle.csv` aufnehmen
2. `03_Decision_Tree.ipynb` neu trainieren und Feature Importance vergleichen
3. In `02_Analyse.ipynb` einen Gruppenvergleich nach Notfallstufe ergänzen
