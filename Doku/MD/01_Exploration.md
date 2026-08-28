# 📓 01_Exploration.ipynb — Was wurde gemacht und warum?

> Dieses Dokument erklärt Schritt für Schritt, was im Notebook `Notebooks/01_Exploration.ipynb` passiert — und warum jeweils so entschieden wurde. Ergebnis des gesamten Notebooks: `Data/analysetabelle.csv` (1.821 Krankenhäuser × 18 Spalten), die zentrale Datengrundlage für Baustein 2–4.

> **⚠️ Korrektur (2026-08-14):** Die Bewertungsspalte `QSErgBewStrukDialog` wurde ursprünglich falsch gelesen — Code `R10` wurde als „auffällig" gezählt. Der offizielle IQTIG-Bericht (*Bericht zum Strukturierten Dialog 2021, Erfassungsjahr 2020*) belegt: `R10` bedeutet „Ergebnis liegt im Referenzbereich", also **nicht auffällig** — das genaue Gegenteil. Dieses Dokument beschreibt die bereits korrigierte Version des Notebooks. Details zu Fehler, Beweis und Auswirkung: `BI_Analyse/Korrektur_Auffaellig_Quote_Dokumentation.docx`.

**Projektfrage:** Welche Krankenhausmerkmale hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme aufweist?

**Reihenfolge im Notebook (bewusste Designentscheidung):** Das Notebook baut zuerst die **Ziel-Variable y** (`QS.Qualitätsindikator.csv`, Abschnitt 1) und erst danach die **Merkmale X** (`SO.csv`, Abschnitt 2 ff.). Das ist eine Umstellung gegenüber einer früheren Notebook-Version, die mit den Stammdaten begann. Begründung direkt aus der Notebook-Einleitung: „Zuerst bauen wir, was wir erklären wollen (y = Ziel-Variable), dann bauen wir die erklärenden Merkmale (X)." Inhaltlich ändert das nichts an den Ergebnissen — nur die Lesereihenfolge folgt jetzt der logischen Abhängigkeit statt der Dateistruktur.

> **📌 Woher kommt „~1.900 Krankenhäuser"?** Die Zahl steht wörtlich in der Original-Aufgabenstellung (`Aufgabenstellung/Fragestellung.docx`, Abschnitt „Die Daten": „Qualitätsindikatoren (C-1.2): Bewertungen für ~1.900 Krankenhäuser"). Es ist aber nur eine grobe Rundung des Auftraggebers, keine berechnete Zahl.
>
> Tatsächlich nachgezählt: **2.310** eindeutige Häuser in `SO.csv` (Rohdaten) und **1.824** eindeutige Häuser in `QS.Qualitätsindikator.csv` — beides schon in den ungefilterten Rohdaten so, nicht erst durch Bereinigung entstanden. Die finale Zeilenzahl von `analysetabelle.csv` ist aber **1.821**, nicht 1.824: Die übrigen 486 Häuser aus `SO.csv` haben keine Zeile in `QS.Qualitätsindikator.csv` und fallen beim Merge in Abschnitt 4 automatisch raus — zusätzlich haben 3 der 1.824 Häuser unter der korrigierten Definition (Abschnitt 1.4) keine einzige bewertbare Zeile mehr (alle ihre Indikatoren sind mit einem N\*-Code versehen) und fallen bei der Ziel-Variablen-Berechnung selbst schon raus.

---

## Setup

**Was:** Bibliotheken laden (`pandas`, `numpy`, `pathlib`, `os`), Arbeitsverzeichnis auf den Projekt-Root wechseln (`if Path.cwd().name == 'Notebooks': os.chdir(Path.cwd().parent)` — funktioniert unabhängig davon, ob das Notebook aus `Notebooks/` oder vom Projekt-Root heraus gestartet wird), `DATA = Path("Data/CSV")` als Basispfad setzen. Alle 86 CSV-Dateien im Ordner werden mit ihrer Dateigröße aufgelistet (0,3 MB bis 911,7 MB).

**Warum:** Bevor irgendetwas geladen wird, muss klar sein, was überhaupt im Datensatz steckt — und alle nachfolgenden relativen Pfade (`Data/CSV/...`, am Ende `Data/analysetabelle.csv`) müssen unabhängig vom Startort des Notebooks korrekt auflösen.

---

## Tabellenverbindungen analysieren — Wie hängen die 86 Dateien zusammen?

**Problem:** Der Datensatz besteht aus 86 CSV-Dateien. Unklar ist, welche Dateien sich verknüpfen lassen und über welche Spalte (Join-Schlüssel).

**Ansatz:** Von jeder Datei wird nur der Header eingelesen (`nrows=0` — keine einzige Datenzeile, dadurch auch für die 911 MB große `QS.Qualitätsindikator.csv` in Millisekunden möglich), danach werden Spaltennamen gezählt, die in mehreren Dateien vorkommen.

**Ergebnis (Häufigkeitsanalyse):**
- `SO.QBID` — universeller Krankenhaus-Schlüssel, kommt in vielen Dateien vor
- `ABTID` — Abteilungs-Schlüssel (verbindet `FA.csv` ↔ `FA.Personalliste.csv`)
- `QS.ID` — kommt nur in `QS.csv` und `QS.Nachweis.csv` vor, **nicht** in `QS.Qualitätsindikator.csv`

**Warum das dritte Ergebnis wichtig ist:** Es ist der Grund, warum `QS.csv` im fertigen Notebook **nirgends geladen wird**, obwohl es lange als „notwendige Brückentabelle" galt (siehe „Was in diesem Notebook *nicht* passiert" unten). `QS.Qualitätsindikator.csv` trägt `SO.QBID` bereits direkt selbst — ein Join über `QS.csv` ist für die Zusammenführung schlicht nicht nötig.

### Spalten-Präfix-Analyse — warum zusätzlich zur Häufigkeitsanalyse?

**Was:** Alle Spaltennamen im Datensatz folgen dem Muster `PRÄFIX.Beschreibung` (z. B. `SO.Betten`, `FA.Personal.Bereich`, `QS.Fortbildungspflichtige`). Das Notebook gruppiert alle 86 Dateien danach, welchen Spalten-Präfix (`SO`, `FA`, `QS`, …) sie führen.

**Warum ein zweiter Analyseschritt nötig ist:** Die Häufigkeitsanalyse beantwortet *„Womit verknüpfen wir die Dateien?"* — aber nicht, *„Welche Dateien gehören thematisch zusammen?"* Dass `SO.QBID` in vielen Dateien vorkommt, sagt noch nichts darüber, ob diese Dateien über Stammdaten, Personal oder Qualitätssicherung sprechen. Die Präfix-Analyse liefert diesen thematischen Überblick, ohne eine einzige Datenzeile zu lesen:
- Spalten-Präfix `SO` → **Standort**-Daten (Krankenhaus-Stammdaten)
- Spalten-Präfix `FA` → **Fachabteilungs**-Daten
- Spalten-Präfix `QS` → **Qualitätssicherungs**-Daten

**Kurzfassung:** Häufigkeitsanalyse = *Wie verknüpfen wir?* · Präfix-Analyse = *Was enthält jede Dateigruppe thematisch?*

---

## 1 — Qualitätsindikatoren (Ziel-Variable) — `QS.Qualitätsindikator.csv`

### Warum zuerst diese Datei, noch vor den Stammdaten?

Die Projektfrage fragt nach Zusammenhängen mit „Qualitätsproblemen" — aber nirgends im Datensatz steht fertig, *wie viele* Qualitätsprobleme ein Haus hat. Diese Information steckt ausschließlich im C-Teil des Qualitätsberichts (`QS.Qualitätsindikator.csv`) und muss aus rohen R\*/N\*-Bewertungscodes erst noch **selbst gebaut** werden — das ist die eigentliche „Knobelaufgabe" laut Aufgabenstellung (`Text_Presentation.docx`, Folie 3–4). Weil alles andere im Notebook (Merkmale, Analysetabelle) sich an dieser Ziel-Variable ausrichtet, steht sie jetzt bewusst am Anfang.

**Warum genau diese Datei:** Sie ist vom IQTIG im Auftrag des G-BA erstellt — alle Häuser werden nach denselben gesetzlich festgelegten Regeln bewertet. Das ist der einzige Datensatz im Projekt mit dieser Eigenschaft; ohne ihn gäbe es keine vergleichbare, einheitlich erhobene Qualitätsaussage.

> **📌 Was ist IQTIG, und was sind „IQTIG-Regeln"?** Das **IQTIG** (Institut für Qualitätssicherung und Transparenz im Gesundheitswesen) führt im Auftrag des **G-BA** (Gemeinsamer Bundesausschuss) die bundesweite Qualitätssicherung für Krankenhäuser durch. Für jeden Qualitätsindikator legt das IQTIG einen **Referenzbereich** fest, in dem der Wert eines Hauses normalerweise liegen sollte — diese Regeln sind **bundesweit einheitlich**. Ob ein Ergebnis außerhalb des Referenzbereichs am Ende wirklich ein echtes Qualitätsproblem ist, klärt ein separates Prüfverfahren, der **Strukturierte Dialog** (daher der Spaltenname `QSErgBewStrukDialog`). Deshalb gilt durchgehend: „Kein Zusammenhang ist ein valides Ergebnis" — Auffälligkeit ist kein automatisches Qualitätsurteil.

### 1.1 — Datei laden

Lädt die gesamte Datei (911 MB, 29 Spalten) und zeigt die ersten 3 Zeilen.

### 1.2 — Bewertungsspalte identifizieren

**Wie wird `QSErgBewStrukDialog` gefunden?** Der Spaltenname enthält Abkürzungen: `Erg` = Ergebnis, `Bew` = Bewertung, `Struk` = Strukturierter, `Dialog` = Dialog. Eine Suche nach dem Teilstring `'bew'` trifft `qsergbewstrukdialog` und findet die Spalte.

**Wichtig — korrigierte Interpretation:** `QSErgBewStrukDialog` hat sieben Bewertungskategorien, nicht zwei. Belegt durch den offiziellen IQTIG-Bericht (*Bericht zum Strukturierten Dialog 2021, EJ 2020*, Tabelle 2 + Tabelle 4):

| Code | Bedeutung | Auffällig? |
|---|---|---|
| `R10` | Ergebnis liegt im Referenzbereich | **Nein** |
| `N01`/`N02`/`N99` | Bewertung nicht vorgesehen | Nicht bewertbar |
| `H20`/`H99` | Einrichtung auf rechnerische Auffälligkeit hingewiesen | Ja |
| `U30`–`33`/`U99` | Nach Strukturiertem Dialog qualitativ unauffällig | Ja (initial), entkräftet |
| `A40`–`42`/`A99` | Nach Strukturiertem Dialog qualitativ auffällig | Ja, bestätigt |
| `D50`/`51`/`99` | Bewertung nicht möglich (fehlerhafte Doku) | Ja |
| `S90`/`91`/`99` | Sonstiges | Ja |

`R10` bedeutet also „unauffällig", nicht „auffällig" — die frühere Annahme `R* = auffällig` war invertiert. Details und Beweis (u. a. eine Summenprobe: H+U+A+D+S ergibt exakt die im IQTIG-Bericht gemeldete Zahl „Rechnerisch auffällige Ergebnisse gesamt") in `BI_Analyse/Korrektur_Auffaellig_Quote_Dokumentation.docx`.

### 1.3 — Alle Spalten mit kleiner Kardinalität prüfen

**Kardinalität** = Anzahl verschiedener Werte in einer Spalte. `QSErgBewStrukDialog` hat ~10 verschiedene Werte (niedrige Kardinalität → kategorial), `SO.QBID` hat ~2.300 (hohe Kardinalität → ID-Spalte). Die Grenze von 15 ist ein pragmatischer Erfahrungswert, kein festes Gesetz — echte kategoriale Spalten haben in der Praxis fast immer deutlich weniger als 15 verschiedene Werte.

### 1.4 — Ziel-Variable berechnen

**Warum diese Designentscheidungen:**
- **Nur `QSQI.ArtDesWertes == 'QI'`** — andere Typen (`EKez`, `TKez`, `TKEZ`, `KKez`) sind reine Zählkennzahlen ohne Auffällig/Unauffällig-Bewertung, keine echten Qualitätsindikatoren. Sie würden `total_qi` verwässern.
- **Alle N\*-Codes ausschließen** (`N01`, `N02`, `N99`), nicht nur `N99` — laut IQTIG-Tabelle 2 bedeutet die ganze N-Kategorie „Bewertung nicht vorgesehen", nicht nur `N99`. Ursprünglich wurde nur `N99` ausgeschlossen und `N01`/`N02` fälschlich als „nicht auffällig" mitgezählt.
- **Deduplizierung über `(SO.QBID, QSQI.Indikator)`, nicht über `QSQI.AEKey`** — `AEKey` sieht wie ein Indikator-Schlüssel aus, ist aber tatsächlich pro Haus vergeben. Hätte man darüber dedupliziert, wäre pro Haus nur eine einzige Zeile übrig geblieben statt ~43 — die Ziel-Variable wäre unbrauchbar geworden, ohne dass der Fehler beim ersten Hinsehen auffällt.
- **Median als Schwelle** (nicht Mittelwert oder ein fixer Wert wie 80 %) — robuster gegenüber Ausreißern und teilt die Häuser automatisch in zwei etwa gleich große Gruppen. Ein Modell, das nur die häufigere Klasse rät, läge sonst schon fast immer richtig, ohne etwas gelernt zu haben.

**Berechnungsschritte (korrigiert):**

| Schritt | Code | Was |
|---|---|---|
| 1 | `QSQI.ArtDesWertes == 'QI'` | Nur echte Indikator-Bewertungen behalten |
| 2 | `~QSErgBewStrukDialog.str.startswith('N')` | Alle nicht bewerteten Indikatoren (N01/N02/N99) rauswerfen |
| 3 | `drop_duplicates(['SO.QBID', 'QSQI.Indikator'])` | Doppelte Zeilen je Haus+Indikator entfernen |
| 4 | `~str.startswith('R')` → Flag | Auffällig-Flag (0/1): alles außer R10 zählt als auffällig |
| 5 | `groupby('SO.QBID').agg(count, sum)` | Von ~43 Zeilen/Haus auf 1 Zeile/Haus verdichten |
| 6 | `auffaellig_quote = auffaellig_n / total_qi` | Anteil auffälliger Indikatoren berechnen |
| 7 | `quote > Median → hat_viele_Probleme` | Aus der Quote ein 0/1-Etikett machen |

**Ergebnis (tatsächlicher, korrigierter Notebook-Output):** Median auffällig-Quote **5,88 %** (statt der ursprünglich fehlerhaften 76,92 %), Ziel-Variable-Verteilung `hat_viele_Probleme`: 916 Häuser mit 0 (unauffälliger), 905 mit 1 (auffälliger) — 1.821 Häuser insgesamt (3 weniger als die 1.824 Häuser mit QI-Daten, weil diese 3 unter der korrigierten Definition keine bewertbare Zeile mehr haben).

### Wie kommt 42,6 zustande — und woher wissen wir, dass es 1.821 Häuser sind?

Jede der 77.537 bereinigten Zeilen trägt eine `SO.QBID`. `nunique()` zählt, wie viele *verschiedene* IDs vorkommen: **1.821**. Daraus folgt direkt:

```
Ø Indikatoren pro Haus = 77.537 Zeilen ÷ 1.821 Häuser = 42,6
```

Deutlich weniger als die ursprünglichen 54,7 — weil jetzt auch `N01` und `N02` ausgeschlossen werden, nicht nur `N99` (siehe oben). Kleine Häuser haben oft nur wenige bewertete Indikatoren, große Häuser deutlich mehr.

### 1.5 — Bereinigungsstatistik: die komplette Filterkaskade

**Neu gegenüber früheren Notebook-Versionen:** Ein eigener Abschnitt zeigt jetzt explizit, wie viele Zeilen nach jedem Filterschritt übrig bleiben — nicht nur das Endergebnis. Tatsächlicher Notebook-Output:

| Schritt | Zeilen danach | Entfernt |
|---|---:|---:|
| Ausgangsdatensatz | 417.799 | — |
| 1. Zählkennzahlen entfernt (`EKez` 33.557 · `TKez` 51.921 · `TKEZ` 5.056 · `KKez` 18.539) | 308.726 | 109.073 |
| 2. `N*` entfernt (N01/N02/N99, korrigiert — vorher nur N99) | 198.770 | 109.956 |
| 3. Duplikate entfernt | **77.537** | 121.233 (61,0 % der Zeilen nach Schritt 2!) |

**Warum das aufschlussreich ist:** 61,0 % der nach Schritt 2 verbliebenen Zeilen waren Duplikate — ein deutlich höherer Anteil, als man auf den ersten Blick vermuten würde, und ein starker nachträglicher Beleg dafür, wie wichtig die korrekte Deduplizierungslogik aus Schritt 3 (Abschnitt 1.4) tatsächlich war. Auffällig ist außerdem, dass die Kategorie „Zählkennzahlen" uneinheitlich geschrieben im Rohdatensatz vorkommt (`TKez` **und** separat `TKEZ`, komplett großgeschrieben, mit 5.056 eigenen Zeilen) — eine kleine Dateninkonsistenz der Quelle, die die Filterlogik (`QSQI.ArtDesWertes == 'QI'`) automatisch mit erfasst, ohne dass sie einzeln behandelt werden musste.

**Korrektur gegenüber der ursprünglichen Version:** Schritt 2 entfernte ursprünglich nur `N99` (272.368 Zeilen übrig, 36.358 entfernt) — nach IQTIG-Tabelle 2 gehören aber auch `N01` und `N02` zur Kategorie „Bewertung nicht vorgesehen" und müssen ebenso ausgeschlossen werden. Das ändert die Grundgesamtheit für Schritt 3 spürbar (198.770 statt 272.368 Zeilen).

---

## 2 — Stammdaten — `SO.csv`

### Was ist ein „Merkmal" und wozu brauchen wir es?

Ein **Merkmal** (Feature) ist eine messbare Eigenschaft eines Krankenhauses — z. B. Bettenzahl, Träger oder Region. In der Sprache von Statistik/ML heißen diese Eigenschaften **X** (die Eingaben), im Gegensatz zur bereits fertigen **Ziel-Variable y** (`hat_viele_Probleme`, Abschnitt 1). `SO.csv` ist die **Ankertabelle** des gesamten Datenmodells: einziger Ort, an dem alle in der Aufgabenstellung genannten Strukturmerkmale (Betten, Träger, Bundesland, Uni-Status, Geo-Koordinaten) in einer einzigen Zeile pro Haus stehen, und Quelle von `SO.QBID` — der ID, über die alle anderen Tabellen verknüpft werden.

### 2.1 — Erste Zeilen anzeigen

Prüft Datenformat und Spaltenwerte anhand der ersten 3 Zeilen.

### 2.2 — Relevante Spalten auswählen

**Was:** `merkmale_cols` ausgewählt, mit folgender Rolle pro Spalte:

| Spalte | Rolle | Warum genau diese |
|---|---|---|
| `SO.QBID` | **Schlüssel**, kein Merkmal | Eindeutige Krankenhaus-ID — damit werden später alle anderen Tabellen (Fortbildung, Personal, Konzern, …) an das richtige Haus angehängt |
| `SO.Name` | Beschreibung | Für Lesbarkeit im Dashboard — kein Analysemerkmal |
| `SO.Betten` | **Merkmal** | Bettenzahl — Größenindikator, in der Aufgabenstellung explizit genannt |
| `SO.Bundesland` | **Merkmal** | Region — mögliche geografische Unterschiede in der Auffälligkeit |
| `SO.Uni` | **Merkmal** | Universitätsklinikum ja/nein — Uni-Kliniken behandeln tendenziell komplexere Fälle |
| `KH.Träger` | Beschreibung | Trägername im Klartext — nur für Anzeige, nicht kategorisiert genug für eine Analyse |
| `KH.Träger.Art` | **Merkmal** | Bereinigte Trägerkategorie (privat/freigemeinnützig/öffentlich) |
| `SO.Latitude` / `SO.Longitude` | **Merkmal** (indirekt) | Geo-Koordinaten — kein Merkmal für den Decision Tree, aber Grundlage für die Deutschlandkarte im Dashboard |
| `SO.Standortnummer` | **Schlüssel**, kein Merkmal | Wird selbst nicht analysiert, sondern nur gebraucht, um später `Konzern.csv` korrekt anzubinden (Abschnitt 7) |

**Ergebnis:** 2.310 eindeutige Krankenhäuser in `SO.csv` (Stammdaten-Ebene, vor dem Zusammenführen mit der Ziel-Variable — siehe „~1.900"-Hinweis oben, warum daraus am Ende 1.821 werden).

### 2.3 — Trägerschaft & Uni-Status prüfen

Gibt die Häufigkeitsverteilung der Trägerarten (privat / freigemeinnützig / öffentlich) und die Anzahl Uni-Kliniken aus — Grundlage für die spätere Gruppenanalyse in `02_Analyse.ipynb`.

---

## 3 — Fortbildungsquote — `QS.Fortbildung.csv`

**Warum interessiert uns die Fortbildungsquote überhaupt?** Ärztinnen und Ärzte, die regelmäßig an Pflichtfortbildungen teilnehmen, sind fachlich auf dem aktuellen Stand — das könnte sich in weniger Behandlungsfehlern niederschlagen. Ob dieser Zusammenhang tatsächlich existiert, wird hier **nicht** geprüft, sondern erst in `02_Analyse.ipynb` (Gruppenvergleich, Korrelation) — an dieser Stelle wird die Zahl nur berechnet. Unabhängig vom späteren Ergebnis: Die Aufgabenstellung nennt die Fortbildungsquote explizit als zu untersuchendes Merkmal.

**Was:** `fortbildungsquote = QS.Fortbildungsnachweis_Erbracht_Habende / QS.Fortbildungspflichtige` (Division durch 0 über `replace(0, np.nan)` abgesichert).

**Warum als Quote und nicht als absolute Zahl:** Nicht alle Häuser haben gleich viele Ärzte und damit gleich viele Pflichtfortbildungen — die Quote macht Häuser unterschiedlicher Größe vergleichbar.

**Ergebnis:** 2.310 Häuser mit Fortbildungsdaten, davon 2.252 mit gültiger Quote (58 mit `Fortbildungspflichtige = 0` → NaN), Mittelwert 59,95 %, Median 66,67 %.

---

## 4 — Analysetabelle zusammenführen (erste Version)

**Was:** `auffaellig_quote` (Ziel-Variable, Abschnitt 1) + `so_klein` (Merkmale, Abschnitt 2) + `fb_quote` (Fortbildungsquote, Abschnitt 3) per Left Join über `SO.QBID` zusammengeführt.

**Warum `how='left'` ausgehend von der Ziel-Variable:** Alle 1.821 Häuser mit einer gültigen Ziel-Variable bleiben erhalten, auch wenn ihnen z. B. Fortbildungsdaten fehlen (→ NaN bei `fortbildungsquote`). Ein Inner Join hätte Häuser ohne vollständige Merkmale unnötig verloren.

### 4.1 — Zwischenstand speichern (ohne `aerzte_pro_bett`)

Speichert die bisherige Analysetabelle als erste Version nach `Data/analysetabelle.csv`. Diese Zwischenspeicherung wird in Abschnitt 5.2 und erneut in Abschnitt 8 durch vollständigere Versionen überschrieben — kein manuelles Zusammenklicken, jeder Zwischenstand ist per Skript reproduzierbar.

---

## 5 — Ärzte pro Bett — `FA.Personalliste.csv` × `FA.csv`

### Warum interessiert uns „Ärzte pro Bett"?

Ein Maß für die **Personalintensität**: Wie viele Ärzte stehen rechnerisch für die Versorgung eines Bettes zur Verfügung? Hypothese: Häuser mit wenig Ärzten im Verhältnis zur Bettenzahl könnten überlasteter sein, was sich in mehr Behandlungsfehlern niederschlagen könnte.

*Vorgriff (erst in Baustein 2/4 wirklich geprüft):* `aerzte_pro_bett` wird sich später als das mit Abstand wichtigste Merkmal der gesamten Analyse herausstellen (Feature Importance 53,6 % im Decision Tree) — an dieser Stelle im Notebook war das noch nicht bekannt, sondern ein späterer, rein datengetriebener Befund.

**Warum dieser Schritt technisch aufwändiger ist als die anderen:** Die Ärztezahl steht nicht direkt in `SO.csv`, sondern in `FA.Personalliste.csv` — Personal **pro Fachabteilung**, nicht pro Haus. Es braucht zwei Joins: `FA.Personalliste.csv` → `FA.csv` über `ABTID`, dann `FA.csv` → `SO.csv` über `FA.QBID = SO.QBID`. Zusätzlich ist `FA.Personal.Anzahl` Komma-Dezimal (`"13,47"`) und muss vor der Aggregation konvertiert werden, sonst behandelt pandas den Wert als String.

### 5.1 — Berechnung (2 Joins + Komma-Fix)

Filtert `FA.Personal.Bereich == "Ärzte"`, konvertiert `"13,47"` → `13.47`, summiert Ärzte je Abteilung, aggregiert über `FA.csv` auf Hausebene, teilt durch `SO.Betten`.

**Warum NaN bei `SO.Betten == 0` nicht aufgefüllt wird:** 4 von 5 fehlenden Werten sind Tageskliniken ohne stationäre Betten. Ärzte/Bett ist für sie nicht definiert — NaN ist hier die korrekte Aussage, kein Datenfehler.

### 5.2 — In Analysetabelle einmergen & speichern

**Ergebnis (tatsächlicher Notebook-Output):** Analysetabelle jetzt (1821, 16) — 5 fehlende Werte bei `aerzte_pro_bett`, davon 4 mit `SO.Betten == 0` (Tageskliniken). Ø Ärzte/Bett: **0,451**.

---

## 6 — Pflegekräfte pro Bett — `SO.Personalliste.csv`

**Hintergrund:** Explizit in `Fragestellung.docx` gefordertes Merkmal. Kollegen im BI-Tool-Vergleich (`BI_Analyse/BI_Datenanalyse.docx`) empfahlen dafür entweder `AQ.Pflege.csv` oder `FA.Personalliste.csv` mit Pflege-Filter.

**Was:** `SO.Personalliste.csv` geladen (78.637 Zeilen, Bereiche: Ärzte / Pflege / Hygiene / Sonstige Ther. / Psych), gefiltert auf `SO.Personal.Bereich == "Pflege"` (30.371 Zeilen), Summe pro `SO.QBID` gebildet, `pflege_pro_bett = pflege_gesamt / SO.Betten`.

**Warum `SO.Personalliste.csv` statt `AQ.Pflege.csv` oder erneut `FA.Personalliste.csv`:** `AQ.Pflege.csv` enthält nur Qualifikationsnachweise, keine Anzahlen. `SO.Personalliste.csv` hat direkt `SO.QBID` **und** `SO.Personal.Anzahl` — kein Umweg über `FA.csv` nötig, einfacher als der Ärzte-Weg in Abschnitt 5, obwohl die Datei technisch auch eine `Ärzte`-Kategorie führt (dort aber nicht verwendet, da `aerzte_pro_bett` bereits über `FA.Personalliste.csv` etabliert war).

**Ergebnis:** 2.310 Häuser mit Pflegedaten, Ø 0,900 Pflegekräfte/Bett (auf Basis aller Häuser mit Personalliste), 97 NaN-Werte (Tageskliniken mit `SO.Betten = 0`). In der finalen 1.821-Zeilen-Analysetabelle bleiben davon 4 fehlende Werte übrig. Wurde später zum **zweitwichtigsten** Merkmal im Decision Tree (Feature Importance 23,8 %).

---

## 7 — Konzernzugehörigkeit — `Konzern.csv`

**Hintergrund:** Von den Kollegen im BI-Tool-Vergleich als „interessante Ergänzung" vorgeschlagen — Konzernhäuser könnten durch zentrale Qualitätssicherung ein systematisch anderes QI-Profil haben.

**Was:** `Konzern.csv` geladen (1.506 Zeilen, Spalten `Konzern`, `Krankenhaus`, `SO.Standortnummer`).

> ⚠️ **Bug gefunden und behoben:** `Konzern.csv` nutzt `SO.Standortnummer` als Schlüssel — **nicht** `SO.QBID`. Ein früherer Join-Versuch verglich `Konzern.csv`s `SO.Standortnummer` versehentlich gegen `SO.csv`s `SO.QBID` → 0 Treffer. Grund: `SO.Standortnummer` war ursprünglich gar nicht in `merkmale_cols` (Abschnitt 2.2) enthalten, obwohl `SO.csv` diese Spalte selbst führt. Nach der Korrektur (Vergleich `SO.Standortnummer` gegen `SO.Standortnummer`): **1.395 von 1.506** Konzern-Einträgen finden eine Übereinstimmung in `SO.csv`.

**Ergebnis (tatsächlicher Notebook-Output):** Auf Ebene aller 2.310 Häuser aus `SO.csv`: 466 Konzernhäuser, 1.844 unabhängige Häuser. In der finalen, auf 1.821 Häuser mit Ziel-Variable begrenzten Analysetabelle sind es **358 von 1.821 (19,7 %)** — der Unterschied zu den 466 erklärt sich daraus, dass die Analysetabelle nur Häuser mit Qualitätsbewertung enthält, `SO.csv` aber alle 2.310 Standorte.

Ein späterer Chi²-Test (Baustein 2) zeigt **keinen** signifikanten Zusammenhang mit `hat_viele_Probleme` (p=0,90); der Decision Tree bestätigt das mit 0 % Feature Importance. Das Merkmal blieb trotzdem im Modell — kein Zusammenhang ist ein valider, dokumentierter Befund, keine fehlgeschlagene Analyse.

---

## 8 — Analysetabelle aktualisieren — alle neuen Merkmale einmergen

**Was:** `pflege_pro_bett` und `ist_konzern` per `merge()` über `SO.QBID` in die bestehende Analysetabelle eingebunden, fehlende `ist_konzern`-Werte auf 0 gesetzt (Häuser ohne Konzern-Treffer = unabhängig), Ergebnis final als `Data/analysetabelle.csv` gespeichert.

**Ergebnis — finale Analysetabelle (tatsächlicher Notebook-Output):**

| Kennzahl | Wert |
|---|---|
| Zeilen (Krankenhäuser) | 1.821 |
| Spalten | 18 |
| `hat_viele_Probleme = 1` | 905 (49,7 %) |
| `hat_viele_Probleme = 0` | 916 (50,3 %) |
| Fehlende Werte `aerzte_pro_bett` | 5 |
| Fehlende Werte `pflege_pro_bett` | 4 |
| Konzernhäuser (`ist_konzern = 1`) | 358 (19,7 %) |

**Alle 18 Spalten:** `SO.QBID`, `total_qi`, `auffaellig_n`, `auffaellig_quote`, `hat_viele_Probleme`, `SO.Name`, `SO.Betten`, `SO.Bundesland`, `SO.Uni`, `KH.Träger`, `KH.Träger.Art`, `SO.Latitude`, `SO.Longitude`, `SO.Standortnummer`, `fortbildungsquote`, `aerzte_pro_bett`, `pflege_pro_bett`, `ist_konzern`.

**Wozu die Analysetabelle genutzt wird:** Rohdaten → Analysetabelle → **alles andere**. Baustein 2 (Grafiken/Statistik), Baustein 3 (Dashboard) und Baustein 4 (Decision Tree) greifen ausschließlich auf `Data/analysetabelle.csv` zu — die 86 Rohdateien werden danach nicht mehr gebraucht.

**Speicherpfad:** Alle drei Speicherstellen im Notebook (Abschnitt 4.1, Abschnitt 5.2, Abschnitt 8) schreiben konsistent relativ nach `"Data/analysetabelle.csv"` — das funktioniert korrekt, weil Setup (siehe oben) das Arbeitsverzeichnis vorab auf den Projekt-Root setzt, egal von wo das Notebook gestartet wird.

---

## 9 — Deskriptive Analyse der Analysetabelle

**Was:** Neuer Abschnitt am Ende des Notebooks (nach dem finalen Speichern in Abschnitt 8), der `Data/analysetabelle.csv` noch einmal frisch von der Festplatte lädt und rein deskriptiv durchleuchtet: Überblick (Shape, Spalten, erste Zeilen, Datentypen), Anzahl nicht-leerer Werte je Spalte, `describe()`, Mittelwert, Median, Minimum/Maximum, Standardabweichung, Quartile und zuletzt eine kombinierte Gesamtübersichts-Tabelle mit allen Kennzahlen nebeneinander.

**Warum das ein eigener Abschnitt ist, obwohl `analysetabelle.csv` schon fertig ist:** Es ist ein bewusster Kontrollschritt — nachdem die Tabelle über 8 Abschnitte hinweg schrittweise zusammengebaut wurde (siehe Abschnitt 4 und 8), prüft dieser Abschnitt unabhängig von der Konstruktionslogik, ob das Endergebnis plausibel aussieht: Passen Zeilen-/Spaltenzahl, fehlende Werte und Wertebereiche zu dem, was man aus den vorherigen Abschnitten erwarten würde?

**Ergebnis (tatsächlicher Notebook-Output):**

- **Vollständigkeit:** Nur 4 von 18 Spalten haben fehlende Werte — `fortbildungsquote` (33 fehlend), `KH.Träger.Art` (28 fehlend), `aerzte_pro_bett` (5 fehlend, siehe Abschnitt 5.1) und `pflege_pro_bett` (4 fehlend, siehe Abschnitt 6). Alle anderen 14 Spalten sind für alle 1.821 Häuser vollständig gefüllt.
- **Ziel-Variable bestätigt sich unabhängig (korrigiertes Niveau):** `auffaellig_quote` hat Mittelwert 0,086 und Median 0,059 (5,9 %) — passt zum in Abschnitt 1.4 berechneten Median von 5,88 %. Deutlich niedriger als die ursprünglich fehlerhaften 76,0 %/76,9 %. `hat_viele_Probleme` hat einen Mittelwert von 0,497 (= Anteil der Einsen) — deckt sich mit 905 von 1.821 Häusern.
- **Bettenzahl stark rechtsschief (unverändert):** Mittelwert 268 liegt deutlich über dem Median 190, die Standardabweichung (262) ist fast so groß wie der Mittelwert selbst — Kennzeichen einer rechtsschiefen Verteilung mit wenigen sehr großen Ausreißern (Maximum: 3.011 Betten). Erklärt rückblickend, warum die Histogramme in `02_Analyse.ipynb` bei 1.500 Betten gekappt werden. Diese Kennzahl ist von der Korrektur nicht betroffen, da sie nicht auf `QSErgBewStrukDialog` basiert.
- **Uni-Kliniken (unverändert):** `SO.Uni`-Mittelwert 0,051 → 5,1 % der Häuser sind Uni-Kliniken (92 von 1.821), die übrigen 1.729 sind normale Häuser.
- **Konzernanteil (unverändert):** `ist_konzern`-Mittelwert 0,197 → 19,7 % Konzernhäuser, passt zu den 358 von 1.821 Häusern aus Abschnitt 7.
- **Personalkennzahlen plausibel (unverändert):** `aerzte_pro_bett` (Median 0,434, Max 2,4) und `pflege_pro_bett` (Median 0,982, Max 3,7) — keine negativen Werte oder unplausiblen Ausreißer.

**Warum in der Gesamtübersicht (letzte Teilzelle) manche Zeilen nur `NaN` zeigen:** `KH.Träger`, `KH.Träger.Art`, `SO.Bundesland`, `SO.Latitude`, `SO.Longitude` und `SO.Name` sind Text-Spalten (`dtype: str`) — Mittelwert, Median, Min/Max und Standardabweichung sind auf Text nicht definiert und bleiben deshalb leer (`numeric_only=True`). Das ist kein Fehler, sondern das erwartete Verhalten; nur die Spalte „Anzahl" (`df.count()`) ist für sie trotzdem gefüllt, weil Zählen auch bei Text funktioniert.

**Einschränkung:** `SO.QBID` und `SO.Standortnummer` sind ID-Spalten — ihr Mittelwert/Median in der Tabelle (z. B. `SO.QBID`-Mittelwert 6.026,76) ist statistisch bedeutungslos, da IDs keine inhaltliche numerische Größe sind, sondern nur eindeutige Kennungen.

**Zum Vergleich mit der ursprünglichen (fehlerhaften) Version:** Nur 27,5 % der Häuser landen unter der korrigierten Definition in derselben Gruppe (viele/wenige Probleme) wie vorher — 72,5 % wechseln. Details zu Fehler, Beweis und Vergleich: `BI_Analyse/Korrektur_Auffaellig_Quote_Dokumentation.docx`.

---

## Was in diesem Notebook *nicht* passiert (bewusste Abgrenzung)

- **`QS.csv`** wird nie geladen — siehe „Tabellenverbindungen analysieren". Ursprünglich als Brückentabelle vermutet, aber nicht nötig.
- **`AQ.Pflege.csv`** wird nie geladen — bewusst durch `SO.Personalliste.csv` ersetzt (Abschnitt 6).
- **`QS.Leistungsbereich.csv`**, **`Notfallversorgung.csv`** und **`MM.csv`** werden hier nicht eingebunden — sie wurden separat in `Notebooks/04_Potenzielle_Erweiterungen.ipynb` (siehe `Doku/MD/04_Potenzielle_Erweiterungen.md`) auf zusätzliches Signal geprüft. Zwei der drei Dateien zeigen dort ein stärkeres Signal als jedes bisherige Merkmal, sind aber (Stand dieses Dokuments) noch nicht in `analysetabelle.csv` übernommen.
- Statistische Auswertung (T-Test, ANOVA, Chi²-Test, Grafiken) passiert **nicht** hier, sondern in `02_Analyse.ipynb`. Dieses Notebook liefert nur die Datengrundlage.

---

*Zuletzt aktualisiert: 2026-08-14 — vollständig gegen den korrigierten Stand von `Notebooks/01_Exploration.ipynb` (58 Zellen) abgeglichen. Wichtigste Änderung: `QSErgBewStrukDialog` wurde neu interpretiert (`R10` = unauffällig statt auffällig, alle `N*`-Codes statt nur `N99` ausgeschlossen), belegt durch den offiziellen IQTIG-Bericht — siehe `BI_Analyse/Korrektur_Auffaellig_Quote_Dokumentation.docx`. Dadurch ändern sich Median auffällig-Quote (5,88 % statt 76,92 %), Zeilenzahl von `analysetabelle.csv` (1.821 statt 1.824) und die Verteilung von `hat_viele_Probleme` (905/916 statt 899/925).*
