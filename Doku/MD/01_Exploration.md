# 📓 01_Exploration.ipynb — Was wurde gemacht und warum?

> Dieses Dokument erklärt Schritt für Schritt, was im Notebook `Notebooks/01_Exploration.ipynb` passiert — und warum jeweils so entschieden wurde. Ergebnis des gesamten Notebooks: `Data/analysetabelle.csv` (1.824 Krankenhäuser × 18 Spalten), die zentrale Datengrundlage für Baustein 2–4.

**Projektfrage:** Welche Krankenhausmerkmale hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme aufweist?

> **📌 Woher kommt „~1.900 Krankenhäuser"?** Diese Zahl taucht in vielen Projektdokumenten auf — sie stammt aus `Aufgabenstellung/Fragestellung.docx` selbst („Qualitätsindikatoren (C-1.2): Bewertungen für ~1.900 Krankenhäuser") und ist eine **grobe Schätzung der Aufgabensteller**, keine im Notebook berechnete Zahl. Tatsächlich nachgezählt (2026-07-30) ergeben sich **zwei unterschiedliche, aber beide exakte** Werte:
> - **2.310** eindeutige `SO.QBID` in `SO.csv` (alle Häuser mit Stammdaten)
> - **1.824** eindeutige `SO.QBID` in `QS.Qualitätsindikator.csv` (Häuser mit tatsächlichen Qualitätsbewertungen)
>
> **1.824** ist damit auch die exakte Zeilenzahl der fertigen `analysetabelle.csv` — beim Filtern (N99 raus, Dedup) geht kein Haus verloren, nur einzelne Indikator-Zeilen. Die 486 Häuser, die in `SO.csv`, aber nicht in `QS.Qualitätsindikator.csv` stehen, fallen beim Merge automatisch raus, weil ohne Ziel-Variable keine Analyse möglich ist. Wo in diesem Dokument „~1.900" vorkam, wurde es durch die passende exakte Zahl ersetzt.

---

## 1. Setup & Datensatz erkunden

**Was:** `DATA = Path("Data/CSV")` als Basispfad gesetzt. Alle 86 CSV-Dateien im Ordner aufgelistet, mit Dateigröße (0,3 MB bis 911,7 MB).

**Warum:** Bevor irgendetwas geladen wird, muss klar sein, was überhaupt im Datensatz steckt. 86 Dateien lassen sich nicht alle manuell durchlesen — deshalb zuerst eine systematische Übersicht (Name + Größe), dann gezielt vertiefen.

### Spaltenverbindungen analysieren

**Was:** Für alle 86 Dateien nur die Kopfzeile eingelesen (`nrows=0`, kostet kaum Zeit), gemeinsame Spaltennamen über alle Dateien gezählt.

**Ergebnis:**
- `SO.QBID` kommt in **34 Dateien** vor → universeller Krankenhaus-Schlüssel
- `ABTID` kommt in **11 Dateien** vor → Abteilungs-Schlüssel (verbindet `FA.csv` ↔ `FA.Personalliste.csv`)
- `QS.ID` kommt in **2 Dateien** vor (`QS.csv`, `QS.Nachweis.csv`) — **nicht** in `QS.Qualitätsindikator.csv`

**Warum wichtig:** Das dritte Ergebnis ist der Grund, warum `QS.csv` im fertigen Notebook **nirgends geladen wird**, obwohl es lange als „notwendige Brückentabelle" galt (siehe Abschnitt 9 „Korrigierte Annahme" unten). `QS.Qualitätsindikator.csv` trägt `SO.QBID` bereits direkt selbst — ein Join über `QS.csv` ist für die Zusammenführung schlicht nicht nötig.

---

## 2. Stammdaten laden — `SO.csv`

### Was ist ein „Merkmal" und wozu brauchen wir es?

Die Projektfrage lautet: *Welche Krankenhaus**merkmale** hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme hat?* Ein **Merkmal** (auch „Feature" genannt) ist dabei einfach eine **messbare Eigenschaft eines Krankenhauses** — z. B. seine Bettenzahl, sein Träger oder seine Region. In der Sprache des maschinellen Lernens/der Statistik heißen diese Eigenschaften **X** (die Eingaben), im Gegensatz zur **Ziel-Variable y** (`hat_viele_Probleme`, siehe Abschnitt 3) — dem Ergebnis, das wir erklären wollen.

**Wozu brauchen wir sie:** Ohne Merkmale gibt es nichts zu vergleichen. Die gesamte Analyse (Baustein 2: Vergleicht sich der Median der Bettenzahl zwischen auffälligen und unauffälligen Häusern? Baustein 4: Kann ein Decision Tree aus den Merkmalen vorhersagen, ob ein Haus auffällig ist?) beruht darauf, dass für jedes Haus dieselben Eigenschaften in derselben Tabelle stehen. `SO.csv` ist die Quelle für die meisten davon.

**Was:** `SO.csv` geladen, `merkmale_cols` ausgewählt — mit folgender Rolle pro Spalte:

| Spalte | Rolle | Warum genau diese |
|---|---|---|
| `SO.QBID` | **Schlüssel**, kein Merkmal | Eindeutige Krankenhaus-ID — damit werden später alle anderen Tabellen (Fortbildung, Personal, Konzern, …) an das richtige Haus angehängt |
| `SO.Name` | Beschreibung | Für Lesbarkeit im Dashboard („Ähnliche Häuser"-Steckbrief) — kein Analysemerkmal |
| `SO.Betten` | **Merkmal** | Bettenzahl — Größenindikator, in der Aufgabenstellung explizit genannt |
| `SO.Bundesland` | **Merkmal** | Region — mögliche geografische Unterschiede in der Auffälligkeit |
| `SO.Uni` | **Merkmal** | Universitätsklinikum ja/nein — Uni-Kliniken behandeln tendenziell komplexere Fälle |
| `KH.Träger` | Beschreibung | Trägername im Klartext — nur für Anzeige, nicht kategorisiert genug für eine Analyse |
| `KH.Träger.Art` | **Merkmal** | Bereinigte Trägerkategorie (privat/freigemeinnützig/öffentlich) — das ist die tatsächlich auswertbare Version von `KH.Träger` |
| `SO.Latitude` / `SO.Longitude` | **Merkmal** (indirekt) | Geo-Koordinaten — kein Merkmal für den Decision Tree, aber Grundlage für die Deutschlandkarte im Dashboard |
| `SO.Standortnummer` | **Schlüssel**, kein Merkmal | Wird selbst nicht analysiert, sondern nur gebraucht, um später `Konzern.csv` korrekt anzubinden (Abschnitt 8) |

**Warum diese Datei überhaupt:** `SO.csv` ist die einzige Tabelle, die **alle** in der Aufgabenstellung genannten Strukturmerkmale in einer einzigen Zeile pro Haus enthält — Betten, Träger, Bundesland, Uni-Status, Geo-Koordinaten. Alternativdateien wie `SO.Personalliste.csv` enthalten nur Detailpersonal, keine Stammdaten. Ohne diese eine „Ankertabelle" müsste man Merkmale aus mehreren unzusammenhängenden Quellen zusammensuchen, ohne einen gemeinsamen Bezugspunkt (Haus) zu haben.

**Warum `SO.Standortnummer` mit ausgewählt:** Wird später für den `Konzern.csv`-Join gebraucht (Abschnitt 8). Stand ursprünglich **nicht** in `merkmale_cols` — genau das hat den Konzern-Join-Bug verursacht (siehe unten).

---

## 3. Ziel-Variable erstellen — `QS.Qualitätsindikator.csv`

### Übergang: Wir haben X — jetzt brauchen wir y

Aus `SO.csv` (Abschnitt 2) haben wir die **Merkmale** — die Eigenschaften eines Hauses (Betten, Träger, Region, …). Damit lässt sich aber noch **gar nichts** vergleichen: Merkmale allein beantworten nicht die Projektfrage. Uns fehlt noch die andere Seite der Gleichung — die **Ziel-Variable** (y): eine einzige Zahl pro Haus, die sagt, *wie viele Qualitätsprobleme* dieses Haus hat. Erst wenn X (Merkmale) **und** y (Ziel-Variable) für jedes Haus in derselben Tabelle stehen, lässt sich fragen: „Haben Häuser mit mehr Betten öfter viele Probleme?"

**Warum dafür eine ganz andere Datei nötig ist:** `SO.csv` enthält nur Strukturdaten (A-Teil des Qualitätsberichts) — dort steht nirgends, ob ein Haus qualitativ auffällig ist. Diese Information steckt ausschließlich im C-Teil des Qualitätsberichts, in `QS.Qualitätsindikator.csv`. Deshalb wechseln wir jetzt komplett die Datenquelle: weg von den Stammdaten, hin zu den ~150 Qualitätsindikator-Bewertungen pro Haus, aus denen die Ziel-Variable erst noch **selbst gebaut** werden muss (sie steht nirgends fertig in einer Spalte — das ist die eigentliche „Knobelaufgabe" laut Aufgabenstellung, siehe `Text_Presentation.docx` Folie 3–4).

**Was:** Datei ist mit 911 MB die größte im Datensatz — zuerst nur `nrows=5` geladen, um die 29 Spalten zu prüfen, danach vollständig geladen (`qi = pd.read_csv(qi_pfad)`).

**Bewertungsspalte:** `QSErgBewStrukDialog`
- `R*` (R10, R20, …) = **rechnerisch auffällig**
- `N01`, `N02` = **nicht auffällig**
- `N99` = **nicht bewertet**

**Warum genau diese Spalte:** Sie ist der einzige standardisierte, für alle 1.824 Häuser mit Bewertungen nach denselben IQTIG-Regeln vergebene Bewertungscode. Andere Dateien (z. B. `QS.Extern.Sonstige.csv`) haben zwar Zahlenwerte, aber keine einheitliche Klassifikation.

> **📌 Was ist IQTIG, und was sind „IQTIG-Regeln"?** Das **IQTIG** (Institut für Qualitätssicherung und Transparenz im Gesundheitswesen) ist die Institution, die im Auftrag des **G-BA** (Gemeinsamer Bundesausschuss, oberstes Beschlussgremium der Selbstverwaltung im deutschen Gesundheitswesen) die bundesweite Qualitätssicherung für Krankenhäuser durchführt. Konkret bedeutet das: Für jeden Qualitätsindikator (z. B. „Komplikationsrate bei Hüft-OPs") legt das IQTIG einen **Referenzbereich** fest — den Bereich, in dem der Wert eines Hauses normalerweise liegen sollte. Diese Referenzbereiche und die Methode, wie „auffällig" berechnet wird, sind die „IQTIG-Regeln". Wichtig für uns: Diese Regeln sind **bundesweit einheitlich** — jedes Haus wird nach denselben Maßstäben bewertet. Genau das macht `QSErgBewStrukDialog` zur einzigen fair vergleichbaren Bewertungsspalte im gesamten Datensatz. Ohne diese Einheitlichkeit könnte man Häuser aus verschiedenen Regionen oder Trägerschaften gar nicht sinnvoll gegenüberstellen.
>
> Wichtig zur Einordnung (siehe auch Abschnitt „Was in diesem Notebook *nicht* passiert" unten): „Auffällig" (`R*`) ist dabei nur ein **statistisches Signal** — ein Hinweis, dass ein Wert außerhalb des Referenzbereichs liegt. Ob dahinter wirklich ein echtes Qualitätsproblem steckt, klärt ein separates Prüfverfahren, der **Strukturierte Dialog** (daher der Spaltenname `QSErgBewStrukDialog` = „QS-Ergebnis der Bewertung im Strukturierten Dialog"). Das ist auch der Grund, warum das Projekt durchgehend betont: „Kein Zusammenhang ist ein valides Ergebnis" — Auffälligkeit ist kein automatisches Qualitätsurteil.

### Berechnungsschritte — die Ziel-Variable Schritt für Schritt

Zur Erinnerung, worauf das alles hinausläuft: Am Ende soll **jedes Haus genau eine Zahl** bekommen — den Anteil seiner Qualitätsindikatoren, die „auffällig" bewertet wurden — und daraus ein einfaches 0/1-Etikett: „hat überdurchschnittlich viele Probleme" oder nicht. `QS.Qualitätsindikator.csv` liefert aber **~55 Zeilen pro Haus** (eine Zeile pro Indikator), nicht eine. Die folgenden 7 Schritte reduzieren diese vielen Zeilen pro Haus auf genau eine Zahl — und jeder Schritt beseitigt dabei eine konkrete Fallstricke in den Rohdaten.

**Kurzübersicht:**

| Schritt | Code | Was |
|---|---|---|
| 1 | `QSQI.ArtDesWertes == 'QI'` | Nur echte Indikator-Bewertungen behalten |
| 2 | `QSErgBewStrukDialog != 'N99'` | Nicht bewertete Indikatoren rauswerfen |
| 3 | `drop_duplicates(['SO.QBID', 'QSQI.Indikator'])` | Doppelte Zeilen je Haus+Indikator entfernen |
| 4 | `str.startswith('R')` → Flag | Auffällig-Flag (0/1) pro Indikator-Zeile setzen |
| 5 | `groupby('SO.QBID').agg(count, sum)` | Von ~55 Zeilen/Haus auf 1 Zeile/Haus verdichten |
| 6 | `auffaellig_quote = auffaellig_n / total_qi` | Anteil auffälliger Indikatoren berechnen |
| 7 | `quote > Median → hat_viele_Probleme = 1` | Aus der Quote ein 0/1-Etikett machen |

**Schritt 1 — Nur echte Qualitätsindikatoren behalten (`QSQI.ArtDesWertes == 'QI'`)**
Nicht jede Zeile in `QS.Qualitätsindikator.csv` ist ein bewerteter Qualitätsindikator. Die Spalte `QSQI.ArtDesWertes` unterscheidet mehrere Werttypen — unter anderem `QI` (ein echter, mit R*/N* bewerteter Qualitätsindikator) sowie `EKez`/`TKez` (Ergebnis- bzw. Teil-Kennzahlen — das sind reine **Zählwerte** ohne Auffällig/Unauffällig-Bewertung, z. B. „wie oft wurde eine bestimmte OP durchgeführt"). Würde man diese mitzählen, würden in Schritt 5 plötzlich Zeilen in `total_qi` landen, die gar keine Bewertung haben — die Quote würde dadurch verwässert, ohne dass das inhaltlich Sinn ergibt.

**Schritt 2 — Nicht bewertete Indikatoren ausschließen (`QSErgBewStrukDialog != 'N99'`)**
`N99` bedeutet „nicht bewertet" — meist weil zu wenige Fälle vorlagen, um überhaupt einen Referenzbereich sinnvoll anzuwenden. Das ist inhaltlich etwas völlig anderes als „unauffällig" (`N01`/`N02`). Würde man `N99` als „nicht auffällig" mitzählen, würde jedes Haus mit vielen `N99`-Indikatoren künstlich besser dastehen, als es die tatsächlich bewerteten Indikatoren hergeben — die Quote wäre systematisch nach unten verzerrt.

**Schritt 3 — Duplikate entfernen (`drop_duplicates(['SO.QBID', 'QSQI.Indikator'])`)**
Ein Haus kann für denselben Indikator mehrfach in den Rohdaten auftauchen (z. B. durch Nachmeldungen oder überlappende Erfassungszeiträume). Ohne Deduplizierung würde derselbe Indikator mehrfach in die Zählung eingehen und das Ergebnis verfälschen. Entscheidend ist, **worüber** dedupliziert wird: über die Kombination aus Haus (`SO.QBID`) und Indikator (`QSQI.Indikator`) — **nicht** über `QSQI.AEKey`. `AEKey` sieht auf den ersten Blick wie ein Indikator-Schlüssel aus, ist aber tatsächlich pro Haus vergeben. Hätte man darüber dedupliziert, wäre pro Haus nur noch **eine einzige Zeile** übrig geblieben statt der ~55 Indikator-Zeilen — die gesamte Ziel-Variable wäre unbrauchbar geworden, ohne dass der Fehler beim ersten Hinsehen auffällt (der Code liefe fehlerfrei durch, nur das Ergebnis wäre falsch).

**Schritt 4 — Auffällig-Flag setzen (`str.startswith('R')`)**
Jetzt wird pro verbliebener Zeile geprüft, ob der Bewertungscode mit `R` beginnt (`R10`, `R20`, …). Das Ergebnis ist ein neues 0/1-Flag pro Indikator-Zeile: 1 = rechnerisch auffällig, 0 = nicht auffällig. Das ist die Vorstufe für die Aggregation im nächsten Schritt — vorher stand in der Spalte ein Text-Code, jetzt eine Zahl, mit der man rechnen (summieren) kann.

**Schritt 5 — Pro Haus verdichten (`groupby('SO.QBID').agg(count, sum)`)**
Das ist der eigentliche „Von-vielen-Zeilen-zu-einer-Zeile"-Schritt: Alle Indikator-Zeilen desselben Hauses werden zusammengefasst. `count` zählt, wie viele Indikatoren insgesamt bewertet wurden (`total_qi`), `sum` addiert die 0/1-Flags aus Schritt 4 (`auffaellig_n` = wie viele davon auffällig waren). Aus ~1.824 × ~55 Zeilen werden so 1.824 Zeilen — eine pro Haus.

**Schritt 6 — Quote berechnen (`auffaellig_quote = auffaellig_n / total_qi`)**
Warum nicht einfach die absolute Anzahl auffälliger Indikatoren (`auffaellig_n`) als Zielgröße nehmen? Weil nicht jedes Haus gleich viele Indikatoren bewertet bekommt (kleinere oder spezialisierte Häuser haben oft weniger). Ein Haus mit 3 auffälligen von 10 bewerteten Indikatoren steht schlechter da als eines mit 3 von 60 — absolut gesehen aber gleich. Die **Quote** (Anteil statt absoluter Zahl) macht Häuser unterschiedlicher Größe erst vergleichbar.

**Schritt 7 — Binäre Ziel-Variable (`quote > Median → hat_viele_Probleme = 1`)**
Zuletzt wird aus der kontinuierlichen Quote (einem Wert zwischen 0 % und 100 %) ein einfaches Ja/Nein gemacht: Liegt ein Haus über dem Median, gilt es als „hat überdurchschnittlich viele Probleme" (1), sonst nicht (0). Das entspricht genau der Formulierung der Projektfrage und ist außerdem die Eingabeform, die spätere Verfahren (Gruppenvergleiche in Baustein 2, Klassifikation in Baustein 4) brauchen.

**Warum ausgerechnet der Median als Schwelle (nicht Mittelwert oder ein fixer Wert wie 80 %):** Der Median (76,92 %) teilt die Häuser automatisch in zwei **gleich große** Gruppen (899 vs. 925 — 49,3 % zu 50,7 %). Das ist für ein Machine-Learning-Modell die ideale, ausgewogene Klassenverteilung — ein Modell, das nur die häufigere Klasse rät, läge sonst schon fast immer richtig, ohne etwas gelernt zu haben. Ein willkürlicher fester Schwellenwert (z. B. „ab 80 % auffällig") wäre außerdem nicht robust gegenüber der tatsächlichen Verteilung dieses Datensatzes — der Median passt sich automatisch an, egal wie die Werte tatsächlich verteilt sind.

**Ergebnis:** 1.824 Häuser (nach Deduplizierung und Filterung — kein Haus geht dabei verloren, siehe Hinweis-Kasten oben zu „~1.900"), Median-Quote 76,92 %.

---

## 4. Fortbildungsquote — `QS.Fortbildung.csv`

### Übergang: y steht — jetzt fehlende Merkmale ergänzen

Die Ziel-Variable (y) ist jetzt fertig: Jedes Haus hat eine `auffaellig_quote` und ein `hat_viele_Probleme`-Etikett. Auf der Merkmals-Seite (X) haben wir aus `SO.csv` (Abschnitt 2) bereits mehrere Merkmale — `SO.Betten`, `SO.Bundesland`, `SO.Uni`, `KH.Träger.Art`. Diese kamen sozusagen „kostenlos" mit, weil sie alle direkt in einer einzigen Tabelle stehen. Die Aufgabenstellung verlangt aber 5–8 Merkmale insgesamt, und nicht jedes davon steht in `SO.csv` — die Fortbildungsquote zum Beispiel steht in einer ganz anderen Datei und muss, genau wie die Ziel-Variable in Abschnitt 3, erst noch **berechnet** werden. Deshalb wechseln wir hier erneut die Datenquelle — als Ergänzung zu den bereits vorhandenen Merkmalen, nicht als Ersatz.

**Warum interessiert uns die Fortbildungsquote überhaupt?** Die Idee dahinter: Ärztinnen und Ärzte, die regelmäßig an Pflichtfortbildungen teilnehmen, sind fachlich auf dem aktuellen Stand — das könnte sich in weniger Behandlungsfehlern bzw. einer niedrigeren Auffälligkeitsquote niederschlagen. Es ist also ein plausibler **Kandidat** für einen Zusammenhang mit unserer Ziel-Variable. Ob dieser Zusammenhang tatsächlich existiert, wird hier in `01_Exploration.ipynb` noch **nicht** geprüft — das passiert erst in `02_Analyse.ipynb` (Gruppenvergleich, Korrelation). An dieser Stelle wird die Zahl nur berechnet und bereitgestellt. Ein weiterer, unabhängiger Grund, warum sie trotzdem berechnet werden muss: Die Aufgabenstellung (`Fragestellung.docx`) nennt die Fortbildungsquote **explizit** als zu untersuchendes Merkmal — sie ist damit gesetzt, unabhängig davon, ob sich später ein Zusammenhang zeigt oder nicht.

**Was:** Datei geladen, `fortbildungsquote = QS.Fortbildungsnachweis_Erbracht_Habende / QS.Fortbildungspflichtige` berechnet.

**Warum als Quote und nicht als absolute Zahl:** Genau wie bei der Ziel-Variable (Abschnitt 3, Schritt 6) haben nicht alle Häuser gleich viele Ärzte und damit gleich viele Pflichtfortbildungen. Die Quote (Erbrachte ÷ Pflichtige) macht Häuser unterschiedlicher Größe vergleichbar — ein großes Haus mit vielen absolvierten Fortbildungen ist nicht automatisch „fortbildungsaktiver" als ein kleines Haus mit wenigen, wenn man nur die absolute Zahl betrachtet.

**Warum diese Datei:** `QS.Fortbildung.csv` ist die einzige Datei im gesamten Datensatz mit den beiden benötigten Zählern (erbrachte und pflichtige Fortbildungen) in auswertbarer Form.

---

## 5. Erste Analysetabelle zusammenführen

**Was:** `SO.csv` + `QS.Qualitätsindikator.csv` (Ziel-Variable) + `QS.Fortbildung.csv` über `SO.QBID` gemerged, als `Data/analysetabelle.csv` gespeichert (erste Version).

**Warum per Skript statt manuell:** Damit die gesamte Datenaufbereitung jederzeit reproduzierbar ist — kein manuelles Zusammenklicken, das sich nicht nachvollziehen lässt.

---

## 6. Ärzte pro Bett — `FA.Personalliste.csv` × `FA.csv`

### Warum interessiert uns „Ärzte pro Bett"?

Die erste Analysetabelle aus Abschnitt 5 hat mit `SO.Betten`, `SO.Bundesland`, `SO.Uni`, `KH.Träger.Art` und `fortbildungsquote` bereits 5 Merkmale — formal genug, um die in der Aufgabenstellung geforderte Mindestzahl von 5–8 Merkmalen zu erfüllen. `Fragestellung.docx` nennt „Ärzte pro Bett" aber als eigenes Beispiel-Merkmal, und die Idee dahinter ist inhaltlich naheliegend: **Ärzte pro Bett ist ein Maß für die Personalintensität** — wie viele Ärzte stehen rechnerisch für die Versorgung eines Bettes zur Verfügung? Die Hypothese: Häuser mit wenigen Ärzten im Verhältnis zu ihrer Bettenzahl könnten überlasteter sein, was sich in mehr Behandlungsfehlern bzw. einer höheren Auffälligkeitsquote niederschlagen könnte.

Anders als bei der Fortbildungsquote (Abschnitt 4) ist die Beschaffung hier aber technisch aufwändiger — die Ärztezahl steht nicht direkt in `SO.csv`, sondern muss aus einer ganz anderen, feiner granularen Tabelle (`FA.Personalliste.csv`, Personal **pro Fachabteilung**, nicht pro Haus) zusammengerechnet werden. Das ist der Grund für die zwei Dateien und den Join in diesem Abschnitt.

*Vorgriff (wird erst in Baustein 2/4 wirklich geprüft):* Anders als die Fortbildungsquote wird sich `aerzte_pro_bett` später tatsächlich als das mit Abstand wichtigste Merkmal der gesamten Analyse herausstellen — das war an dieser Stelle im Notebook aber noch nicht bekannt, sondern ein späterer, rein datengetriebener Befund.

**Was:**
- `FA.csv` geladen (Brückentabelle: `ABTID` ↔ `FA.QBID` = `SO.QBID`)
- `FA.Personalliste.csv` geladen, gefiltert auf `FA.Personal.Bereich == "Ärzte"`
- `FA.Personal.Anzahl` ist **Komma-Dezimal** (z. B. `"13,47"`) → `.str.replace(",", ".")` → `float`
- Summe Ärzte pro `ABTID` → über `FA.csv` auf `SO.QBID` aggregiert → `aerzte_pro_bett = aerzte_gesamt / SO.Betten`

**Warum der Umweg über `FA.csv`:** `FA.Personalliste.csv` kennt nur `ABTID` (Abteilungs-ID), nicht `SO.QBID` (Haus-ID). `FA.csv` ist die einzige Tabelle, die beide Schlüssel hat. Ohne sie lässt sich die Ärzteanzahl keinem Krankenhaus zuordnen.

**Warum NaN bei `SO.Betten == 0` nicht aufgefüllt wird:** 4 von 5 fehlenden Werten sind Tageskliniken ohne stationäre Betten. Ärzte/Bett ist für sie **nicht definiert** — 0 Betten ergibt kein sinnvolles Verhältnis. NaN ist hier die korrekte Aussage, kein Datenfehler.

**Ergebnis:** Ø 0,451 Ärzte/Bett. Dieses Merkmal wird sich später (Baustein 4) als **stärkster Prädiktor** herausstellen (Feature Importance 53,6 % im Decision Tree) — das war zum Zeitpunkt dieses Notebook-Abschnitts noch nicht bekannt, sondern ein späterer, datengetriebener Befund.

---

## 7. Pflegekräfte pro Bett — `SO.Personalliste.csv` *(ergänzt 2026-07-29)*

**Hintergrund:** Explizit in `Fragestellung.docx` gefordertes Merkmal — stand lange als offener Punkt in `ToDo.md`. Kollegen im BI-Tool-Vergleich (`BI_Datenanalyse.docx`) empfahlen dafür entweder `AQ.Pflege.csv` oder `FA.Personalliste.csv` mit Pflege-Filter.

**Was:** `SO.Personalliste.csv` geladen, gefiltert auf `SO.Personal.Bereich == "Pflege"`, Summe pro `SO.QBID` gebildet, `pflege_pro_bett = pflege_gesamt / SO.Betten`.

**Warum `SO.Personalliste.csv` statt `AQ.Pflege.csv` oder `FA.Personalliste.csv`:** `AQ.Pflege.csv` enthält nur Qualifikationsnachweise, **keine Anzahlen** — für ein Verhältnis wie „Pflegekräfte pro Bett" nutzlos. `SO.Personalliste.csv` hat direkt `SO.QBID` **und** `SO.Personal.Anzahl` — kein Umweg über `FA.csv` nötig, einfacher als der Ärzte-Weg in Abschnitt 6.

**Ergebnis:** Ø 1,01 Pflegekräfte/Bett, 4 fehlende Werte. Wurde später zum **zweitwichtigsten** Merkmal im Decision Tree (Feature Importance 23,8 %).

---

## 8. Konzernzugehörigkeit — `Konzern.csv` *(ergänzt 2026-07-29)*

**Hintergrund:** Von den Kollegen im BI-Tool-Vergleich als „interessante Ergänzung" vorgeschlagen — Konzernhäuser könnten durch zentrale Qualitätssicherung ein systematisch anderes QI-Profil haben.

**Was:** `Konzern.csv` geladen, Spalten `Konzern`, `Krankenhaus`, `SO.Standortnummer`.

> ⚠️ **Bug gefunden und behoben:** `Konzern.csv` nutzt `SO.Standortnummer` als Schlüssel — **nicht** `SO.QBID`. Der erste Join-Versuch verglich `Konzern.csv`s `SO.Standortnummer` versehentlich gegen `SO.csv`s `SO.QBID` → **0 Treffer**, `ist_konzern` wäre für alle 1.824 Häuser 0 gewesen. Grund: `SO.Standortnummer` war ursprünglich gar nicht in `merkmale_cols` (Abschnitt 2) enthalten, obwohl `SO.csv` diese Spalte selbst hat. Nach Korrektur (Vergleich `SO.Standortnummer` gegen `SO.Standortnummer`): **358 von 1.824 Häusern (19,6 %)** sind Konzernhäuser.

**Ergebnis:** `ist_konzern` (0/1). Ein späterer Chi²-Test (Baustein 2) zeigt **keinen** signifikanten Zusammenhang mit `hat_viele_Probleme` (p=0,90); der Decision Tree bestätigt das mit 0 % Feature Importance. Das Merkmal blieb trotzdem im Modell — kein Zusammenhang ist ein valider, dokumentierter Befund, keine fehlgeschlagene Analyse.

---

## 9. Analysetabelle aktualisieren & speichern

**Was:** `pflege_pro_bett` und `ist_konzern` per `merge()` über `SO.QBID` in die bestehende Analysetabelle eingebunden, fehlende `ist_konzern`-Werte auf 0 gesetzt (Häuser ohne Konzern-Treffer = unabhängig), Ergebnis als `Data/analysetabelle.csv` gespeichert.

**Ergebnis — finale Analysetabelle:**

| Kennzahl | Wert |
|---|---|
| Zeilen (Krankenhäuser) | 1.824 |
| Spalten | 18 |
| `hat_viele_Probleme = 1` | 899 (49,3 %) |
| `hat_viele_Probleme = 0` | 925 (50,7 %) |
| Fehlende Werte `aerzte_pro_bett` | 5 |
| Fehlende Werte `pflege_pro_bett` | 4 |
| Konzernhäuser (`ist_konzern = 1`) | 358 (19,6 %) |

**Wozu die Analysetabelle genutzt wird:** Rohdaten → Analysetabelle → **alles andere**. Baustein 2 (Grafiken/Statistik), Baustein 3 (Dashboard) und Baustein 4 (Decision Tree) greifen ausschließlich auf `Data/analysetabelle.csv` zu — die 86 Rohdateien werden danach nicht mehr gebraucht.

### Pfad-Korrektur (2026-07-29)

Alle drei Speicherstellen im Notebook (Abschnitt 5, eine Zwischenspeicherung nach Abschnitt 6, und Abschnitt 9) schrieben ursprünglich nach `analysetabelle.csv` **im Projekt-Root**. Tatsächlich liegt die Datei aber in `Data/` (dort greifen auch `dashboard_utils.py` und `modell_klasse.py` zu). Alle drei Stellen wurden auf `Data/analysetabelle.csv` korrigiert, damit ein frischer Notebook-Lauf die Datei am richtigen Ort ablegt.

---

## Was in diesem Notebook *nicht* passiert (bewusste Abgrenzung)

- **`QS.csv`** wird nie geladen — siehe Abschnitt 1. Ursprünglich als Brückentabelle vermutet, aber nicht nötig.
- **`AQ.Pflege.csv`** wird nie geladen — bewusst durch `SO.Personalliste.csv` ersetzt (Abschnitt 7).
- **`QS.Leistungsbereich.csv`** (`QSLB.Dokumentationsrate`) wurde identifiziert, aber bis heute nicht eingebunden — bleibt offener Punkt für eine künftige Erweiterung.
- Statistische Auswertung (T-Test, ANOVA, Chi²-Test, Grafiken) passiert **nicht** hier, sondern in `02_Analyse.ipynb`. Dieses Notebook liefert nur die Datengrundlage.

---

*Zuletzt aktualisiert: 2026-07-30*
