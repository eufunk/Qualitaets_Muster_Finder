# ❓ Fragen und Antworten — Qualitäts-Muster-Finder

> Vorbereitung auf mögliche Rückfragen des Dozenten am Ende der Präsentation. 30 Fragen, gruppiert nach Themenblock. Alle Zahlen sind gegen die aktuellen Notebooks/MD-Dokumente verifiziert (`01_Exploration.md`, `02_Analyse.md`, `03_Decision_Tree.md`).

**Projektfrage:** Welche Krankenhausmerkmale hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme aufweist?

---

## A — Fragestellung & Projektrahmen

### 1. Was ist die zentrale Fragestellung des Projekts?
Gibt es Zusammenhänge zwischen Strukturmerkmalen eines Krankenhauses (Größe, Trägerschaft, Personal, Region, Uni-Status, Konzernzugehörigkeit, Fortbildung) und der Häufigkeit, mit der ein Haus in seinen Qualitätsindikatoren auffällig wird? Ausdrücklich Teil der Aufgabenstellung: Ein „kein Zusammenhang gefunden" ist ein genauso gültiges Ergebnis wie ein gefundener Zusammenhang.

### 2. Warum ist „Kein Zusammenhang ist ein valides Ergebnis" für dieses Projekt relevant?
Weil es sich in diesem konkreten Projekt tatsächlich bewahrheitet hat — nicht nur eine theoretische Warnung geblieben ist. Zwei Beispiele aus der eigenen Analyse: Die Trägerschaft zeigt im Balkendiagramm einen auffälligen Unterschied, ist aber statistisch nicht signifikant (ANOVA p = 0,969) — der optische Eindruck täuscht, der Zusammenhang ist nicht real. Und das lineare Modell erreichte auf der stetigen Zielgröße sogar ein negatives R² (−0,007), also eine schlechtere Vorhersage als der bloße Durchschnittswert. Beides sind echte „Kein Zusammenhang"-Ergebnisse, keine gescheiterten Analysen.

Der Satz selbst stammt wörtlich aus dem Einführungsvortrag des Dozenten (`Aufgabenstellung/Text_Presentation.docx`) — als ausdrückliche Warnung davor, ein Ergebnis so lange zu drehen, bis am Ende doch ein vorzeigbarer Zusammenhang „gefunden" wird.

### 3. Was bedeutet „auffällig" bei einem Qualitätsindikator? Ist ein auffälliges Haus automatisch schlecht?
Nein. „Rechnerisch auffällig" heißt nur: Ein gemessener Wert liegt außerhalb eines vorab definierten Referenzbereichs — ein statistisches Signal, kein Urteil. Ob wirklich ein Qualitätsproblem vorliegt, klärt danach der „Strukturierte Dialog": IQTIG bewertet bundesweit rechnerisch, eine Landesgeschäftsstelle (je Bundesland unterschiedlich organisiert, z. B. Landesärztekammer) klärt danach lokal mit dem Haus, ob es ein echtes Problem, ein Dokumentationsfehler oder ein Fallmix-Effekt ist — das mündet in die U-/A-Codes. Unsere Ziel-Variable bildet nur die erste, rechnerische Stufe ab, nicht dieses Endergebnis.

**Steht der Referenzbereich in unseren Rohdaten?** Ja, direkt in `QS.Qualitätsindikator.csv`: `QSQI.Referenzwert` (Schwellenwert), `QSQI.Operator` (Vergleichsrichtung, z. B. `<=`) und `QSQI.Ergebnis` (gemessener Wert) — pro Indikator individuell von IQTIG festgelegt. Im Projekt nutzen wir diese Spalten nicht selbst zum Nachrechnen, sondern übernehmen direkt `QSErgBewStrukDialog`, IQTIGs fertige Bewertung.

**Was, wenn wir selbst nachgerechnet hätten?** Als Kontrollrechnung geprüft (`01_Exploration_Ref.ipynb`/`.md`) — beide Pfade starten identisch, filtern dann nach unterschiedlichen Kriterien:

| Schritt | Offizieller Pfad | Eigenberechnungs-Pfad |
|---|---:|---:|
| 0. Rohdaten | 417.799 | 417.799 |
| 1. Nach QI-Filter | 308.726 | 308.726 |
| 2. Nächstes Kriterium | 198.770 (N*-Codes entfernt) | 207.844 (Operator vorhanden) |
| 3. Letztes Kriterium | 77.537 (Duplikate entfernt) | 111.061 (Ergebnis nicht maskiert) |
| Häuser am Ende | **1.821** | **1.710** |

„Nicht maskiert" = Datenschutz bei kleinen Fallzahlen: Bei wenigen Fällen ersetzt IQTIG den echten Wert durch „≤3" (23 % der Zeilen) — ohne exakten Wert kein eigener Vergleich möglich, diese Zeilen fallen bei der Eigenberechnung raus. Drei echte Beispielzeilen:

| SO.QBID | Indikator (gekürzt) | Ergebnis | Referenzwert | Bewertung |
|---|---|---|---|---|
| 6858 | Infektionen bei Gallenblasenentfernung | ≤3 | 3 | R10 |
| 6416 | Komplikationen (Blutgerinnsel, Lungenentzündung, Herz-Kreislauf) | ≤3 | 3,29 | R10 |
| 6325 | Blasenkatheter länger als 24 Stunden | ≤3 | 7,25 | R10 |

Trotz unbekanntem Ergebnis überall R10 (nicht auffällig) — plausibel, weil selbst der ungünstigste mögliche Wert (3) noch im Referenzbereich liegt (Details: `01_Exploration_Ref.md`).

Die beiden Pfade teilen sich die ersten beiden Schritte komplett — dieselben Rohdaten, derselbe QI-Filter —, filtern ab Schritt 2 aber nach völlig unterschiedlichen Kriterien: Der offizielle Pfad filtert nach **Bewertungsinhalt** (ist der Code überhaupt eine echte Bewertung, keine Dopplung), der Eigenberechnungs-Pfad filtert nach **Datenverfügbarkeit** (stehen Referenzwert und Operator überhaupt zur Verfügung, ist das Ergebnis nicht aus Datenschutzgründen maskiert). Das Ergebnis: 111 Häuser weniger als bei der offiziellen Methode, und selbst bei den verbleibenden 1.710 Häusern nur eine kleinere, andere Auswahl an Indikatoren pro Haus. Details und die Auswirkung auf die Ziel-Variable (Median 5,00 % statt 5,88 %, nur 75,9 % Übereinstimmung bei der Gruppenzuordnung): siehe `01_Exploration_Ref.md`.

### 4. Wer sind IQTIG und G-BA, und warum sind sie relevant?
IQTIG (Institut für Qualitätssicherung und Transparenz im Gesundheitswesen) ist die Bundesbehörde, die im Auftrag des G-BA (Gemeinsamer Bundesausschuss, oberstes Beschlussgremium der Selbstverwaltung im deutschen Gesundheitswesen) die jährlichen Qualitätsberichte aller deutschen Krankenhäuser erhebt, auswertet und veröffentlicht. Unsere gesamte Datenbasis (Berichtsjahr 2023) stammt aus diesen offiziellen Berichten.

---

## B — Daten

### 5. Wie viele Krankenhäuser wurden verwendet, und warum ist 1.821 nicht gleich 2.310?
Die finale Analysetabelle enthält 1.821 Krankenhäuser. `SO.csv` (Stammdaten) listet 2.310 Standorte insgesamt — davon haben 486 keine einzige Zeile in `QS.Qualitätsindikator.csv` (bleiben bei 1.824), und von diesen 1.824 haben zusätzlich 3 Häuser laut der Code-Definition keine einzige bewertbare Zeile mehr (alle ihre Indikatoren sind N*-Codes) — macht 1.821 übrige Häuser mit einer gültigen Ziel-Variable.

### 6. Wie habt ihr entschieden, welche der 86 CSV-Dateien verwendet werden?
In zwei Schritten: Erstens eine Häufigkeits- und Spalten-Präfix-Analyse (nur Header, `nrows=0`) — jede Spalte folgt dem Muster `PRÄFIX.Beschreibung` (SO = Standort, FA = Fachabteilung, QS = Qualitätssicherung), das zeigt, welche Dateien thematisch zusammengehören und wie sie sich verknüpfen lassen. Zweitens eine inhaltliche Prüfung: Gehört die Datei zum A-Teil (Strukturdaten → mögliches Merkmal) oder C-Teil (Qualitätsindikatoren → Ziel-Variable)? Lässt sie sich sauber über `SO.QBID` verknüpfen und liegt für nahezu alle 1.821 Häuser vor? Am Ende blieben 7 von 86 Dateien aktiv genutzt, 33 als „möglicherweise relevant" für spätere Erweiterungen markiert, 46 ausgeschlossen (Lookup-Tabellen, Verwaltungsdaten, DSGVO-Daten).

### 7. Was ist SO.QBID, und warum ist es so wichtig?
Die Qualitätsbericht-ID des Standorts — eine eindeutige Nummer, die jedem Krankenhaus-Standort zugeteilt ist und in rund 60 der 86 Dateien vorkommt. Sie ist der universelle Verbindungsschlüssel des gesamten Datensatzes: Ohne sie ließen sich Stammdaten, Personal, Fortbildung und Qualitätsbewertungen nicht dem richtigen Haus zuordnen.

### 8. Warum wurden Personen.csv und FA.Personen.csv nicht verwendet?
Beide enthalten personenbezogene Daten (Name, E-Mail, Telefon, Funktion von Kontaktpersonen bzw. ärztlichen Leitungen). Sie wurden aus DSGVO-Gründen bewusst ausgeschlossen. Der gesamte `Data/`-Ordner ist zusätzlich per `.gitignore` von der Versionierung ausgenommen, sodass keine Rohdaten ins Code-Repository gelangen.

---

## C — Ziel-Variable & Bewertungscodes

### 9. Wie wurde die Ziel-Variable berechnet?
Aus `QS.Qualitätsindikator.csv` (911,7 MB, größte Datei im Datensatz): Filterkaskade von 417.799 Zeilen → Zählkennzahlen wie EKez/TKez entfernt (308.726) → alle N*-Codes entfernt (198.770) → Duplikate je Haus+Indikator entfernt (77.537, Schlüssel `SO.QBID` + `QSQI.Indikator`). Pro Haus wird `auffaellig_quote = auffällig_n / total_qi` berechnet, der Median (5,88 %) dient als Trennwert für die binäre Variable `hat_viele_Probleme`.

### 10. Wie wird die Bewertungsspalte `QSErgBewStrukDialog` interpretiert, und wodurch ist das belegt?
Die Spalte kennt sieben Bewertungscodes. Belegt durch ein offizielles IQTIG-Dokument („Bericht zum Strukturierten Dialog 2021, Erfassungsjahr 2020"), das die Bedeutung aller sieben Codes eindeutig dokumentiert: `R10` bedeutet „Ergebnis liegt im Referenzbereich" (nicht auffällig), alle N\*-Codes bedeuten „nicht bewertet" (nicht bewertbar, ausgeschlossen), alle übrigen Codes zählen als auffällig.

### 11. Was bedeutet der Code R10 konkret, und warum ist er für die Ziel-Variable so wichtig?
R10 bedeutet „Ergebnis liegt im Referenzbereich" — also **nicht** auffällig. Da R10 der mit Abstand häufigste Code ist, bestimmt seine korrekte Einordnung maßgeblich, wie die Ziel-Variable für den Großteil der Häuser ausfällt.

| Code | Bedeutung | Auffällig? |
|---|---|---|
| R10 | Ergebnis liegt im Referenzbereich | Nein |
| N01/N02/N99 | Bewertung nicht vorgesehen | Nicht bewertbar — ausgeschlossen |
| H20/H99 | Auf Auffälligkeit hingewiesen | Ja |
| U30–33/U99 | Qualitativ unauffällig (entkräftet) | Ja (initial gezählt) |
| A40–42/A99 | Qualitativ auffällig (bestätigt) | Ja, bestätigt |
| D50/51/99 · S90/91/99 | Nicht bewertbar/Sonstiges | Ja |

### 12. Wie stellt ihr sicher, dass eure Interpretation der Bewertungscodes richtig ist?
Per Summenprobe gegen den offiziellen IQTIG-Bericht: Die Summe der als auffällig gezählten Codes (H+U+A+D+S) ergibt exakt die im IQTIG-Bericht veröffentlichte Zahl „Rechnerisch auffällige Ergebnisse gesamt". Zusätzlich kommen unsere Python-Auswertung und die unabhängige Power-BI-Auswertung der BI-Kollegen zum selben Ergebnis — ein zweiter, unabhängiger Beleg.

### 13. Wie ausgewogen ist die Ziel-Variable, und warum ist das für ein Modell wichtig?
Von 1.821 Häusern haben 905 (49,7 %) viele und 916 (50,3 %) wenige Probleme — dank Median-Split fast perfekt balanciert. Eine ausgewogene Klassenverteilung ist wichtig, damit ein Modell nicht einfach durch reines Raten der Mehrheitsklasse fast immer richtig liegt, ohne etwas gelernt zu haben — genau das misst die Basislinie von 50,4 % in Kapitel 4.

### 14. Warum wurde der Median statt Mittelwert oder ein fester Schwellenwert (z. B. 80 %) als Trennwert gewählt?
Der Median ist robuster gegenüber Ausreißern als der Mittelwert und teilt die Häuser automatisch in zwei etwa gleich große Gruppen (916 vs. 905) — das verhindert ein starkes Klassenungleichgewicht, bei dem ein Modell schon durch reines Raten der Mehrheitsklasse fast immer richtig läge, ohne etwas gelernt zu haben. Ein fixer Wert wie 80 % wäre willkürlich und nicht an die tatsächliche Verteilung der Daten angepasst.

---

## D — Merkmale

### 15. Welche Merkmale wurden verwendet, und warum genau diese?
Sieben Merkmale: Bettenzahl, Trägerschaft, Bundesland, Uni-Status, Fortbildungsquote, Ärzte pro Bett, Pflegekräfte pro Bett, Konzernzugehörigkeit. Die Aufgabenstellung fordert 5–8 aussagekräftige Strukturmerkmale und nennt einen Großteil davon explizit als Beispiel. Jedes Merkmal musste zusätzlich zwei Kriterien erfüllen: sauber über `SO.QBID` verknüpfbar sein und für nahezu alle 1.821 Häuser vollständig vorliegen.

### 16. Wie wurde „Ärzte pro Bett" berechnet, und was war technisch schwierig daran?
Über zwei Joins: `FA.Personalliste.csv` (Personal pro Fachabteilung) → `FA.csv` über `ABTID` → `SO.csv` über `FA.QBID = SO.QBID`. Die Personalanzahl war zusätzlich im deutschen Dezimalformat gespeichert („13,47" statt „13.47") und musste vor der Summenbildung konvertiert werden (`str.replace(',', '.')` + `pd.to_numeric`), sonst hätte pandas den Wert als Text behandelt und die Summe wäre 0 gewesen.

### 17. Warum wurde Pflegepersonal über SO.Personalliste.csv statt AQ.Pflege.csv berechnet?
`AQ.Pflege.csv` enthält nur Qualifikationsnachweise, keine tatsächlichen Personalanzahlen. `SO.Personalliste.csv` hat direkt `SO.QBID` und `SO.Personal.Anzahl` — kein Umweg über eine Brückentabelle nötig, einfacher als der Ärzte-Weg über `FA.csv`.

---

## E — Deskriptive Analyse & Statistik

### 18. Welches Merkmal hängt am stärksten mit Qualitätsproblemen zusammen?
Ärzte pro Bett — statistisch der stärkste abgesicherte Einzelbefund (T-Test t=−9,13, p<0,0001; Korrelation r=+0,210) und mit 72,8 % Feature Importance auch im Decision Tree mit Abstand das wichtigste Merkmal. Pflegekräfte pro Bett zeigt dasselbe Muster (t=−7,51, p<0,0001), korreliert aber stark mit Ärzte pro Bett (r=0,577) — beide messen vermutlich teilweise dieselbe zugrunde liegende Eigenschaft „Personalausstattung".

### 19. Bei der Trägerschaft zeigt die Grafik einen optischen Unterschied, die ANOVA sagt aber „nicht signifikant". Wie erklärt ihr diesen Widerspruch?
Das ist kein Widerspruch, sondern zeigt genau, warum Inferenzstatistik nötig ist. Die drei Trägerarten-Mittelwerte sind auf der stetigen `auffaellig_quote` praktisch identisch (0,0856/0,0857/0,0872). Der optisch klare Balkendiagramm-Unterschied (43,8 % vs. 53,5 %) entsteht erst durch den Median-Split: Schon kleine, statistisch nicht abgesicherte Unterschiede in der stetigen Quote können bei einem Split in zwei Gruppen zu sichtbar unterschiedlichen Prozentsätzen führen.

### 20. Was ist ein Störfaktor (Confounder), und wo kommt er im Projekt vor?
Eine dritte Variable, die mit beiden Seiten eines beobachteten Zusammenhangs gleichzeitig zu tun hat und dadurch einen Zusammenhang vortäuschen kann. Konkret geprüft: Private Häuser sind im Median deutlich kleiner (125 Betten) als freigemeinnützige (218) und öffentliche (232) — kleinere Häuser haben pro Indikator weniger Fälle, was die statistische Schwankung erhöht. Da die ANOVA aber schon auf Ebene der stetigen Quote keinen Trägereffekt findet, muss hier nichts mehr bereinigt werden — der Confounder-Check bleibt trotzdem ein wichtiger methodischer Schritt, um nicht vorschnell zu schließen.

### 21. Warum ist eine Korrelation von r=+0,14 bei p<0,0001 signifikant, aber trotzdem schwach?
Das ist kein Widerspruch: Der p-Wert sagt nur, dass ein Unterschied wahrscheinlich real ist und kein Stichprobenrauschen — bei einer großen Stichprobe (1.821 Häuser) werden schon kleine, echte Effekte statistisch signifikant. Wie groß der Effekt praktisch ist, zeigt die Korrelation r selbst, und r=+0,14 (Bettenzahl) ist schwach: Das Merkmal erklärt nur einen kleinen Teil davon, ob ein Haus viele Probleme hat, obwohl der Zusammenhang real ist.

### 22. Was zeigt die Korrelationsmatrix, und warum ist total_qi die stärkste Korrelation, aber inhaltlich nicht relevant?
Sie fasst die Korrelation r jedes Merkmals mit der Ziel-Variable in einer Zahl zusammen. `total_qi` (Anzahl bewerteter Indikatoren pro Haus) korreliert mit +0,241 am stärksten, ist aber ein Strukturartefakt, kein Qualitätsmerkmal: Mehr bewertete Indikatoren bedeuten einfach mehr Gelegenheiten, dass einer davon auffällig ausfällt. Inhaltlich aussagekräftiger sind `aerzte_pro_bett` (+0,210) und `pflege_pro_bett` (+0,174).

---

## F — Machine Learning / Decision Tree

### 23. Warum wurde ein Decision Tree gewählt und keine komplexeren Modelle wie Random Forest?
Fünf Gründe: Interpretierbarkeit (nachvollziehbare Wenn-Dann-Regeln statt Black Box), Passung zum Datensatz (ein flacher Baum ist ehrlich darüber, was mit diesen Daten überhaupt lernbar ist), keine Vorverarbeitung nötig (anders als SVM/neuronale Netze), vollständige Bewertbarkeit (Accuracy, Precision, Recall, F1, Feature Importance auf einen Blick) und Ergänzung durch eine parallele lineare Regression (liefert mit R² eine zweite, unabhängige Perspektive). Ein Random Forest hätte vermutlich eine leicht bessere Accuracy geliefert, aber auf Kosten der Interpretierbarkeit — bei dieser Datenlage kein guter Tausch.

### 24. Wie gut ist das Modell wirklich? Ist 57 % Accuracy nicht schlecht?
57,0 % Accuracy liegt nur 6,6 Prozentpunkte über der Basislinie (50,4 % — der Anteil, den man durch bloßes Raten der Mehrheitsklasse träfe). Das ist ehrlich betrachtet ein schwaches, aber reales Signal: Precision 55,2 %, Recall 70,2 %, F1 61,8 %, 5-Fold-Cross-Validation 61,6 % ± 3,7 % (stabil, kein Zufallstreffer). Das Modell ist „großzügig" — es sagt eher „Viele Probleme" und findet dadurch die meisten echten Problemfälle (hoher Recall), produziert aber auch relativ viele falsche Alarme (niedrigere Precision). Wichtiger als die Accuracy-Zahl selbst ist die ehrliche Einordnung: Strukturmerkmale allein reichen nicht für eine zuverlässige Vorhersage.

### 25. Was bedeutet die Feature Importance, und wieso hat Trägerschaft 0 %?
Sie zeigt, wie stark jedes Merkmal zu den Entscheidungen des Baums beigetragen hat (alle Werte zusammen = 100 %): `aerzte_pro_bett` 72,77 %, `SO.Betten` 16,48 %, `pflege_pro_bett` 10,75 %, alle übrigen Merkmale 0,00 % bei `max_depth=3`. Trägerschaft (`traeger_enc`) trägt 0 % bei, weil der Baum bei nur 3 Ebenen Tiefe die stärkeren Merkmale bevorzugt — passend dazu findet auch die ANOVA für die Trägerschaft keinen signifikanten Zusammenhang (F=0,031, p=0,969). Zwei unabhängige Methoden kommen also zum selben Schluss.

### 26. Was bedeutet ein negatives R², und ist das nicht ein Zeichen für gescheiterte Analyse?
R² = −0,007 (lineare Regression auf der stetigen `auffaellig_quote`) bedeutet: Das Modell ist schlechter als der einfachste denkbare Vergleichswert — einfach für jedes Haus den Durchschnittswert aller Häuser vorherzusagen. Ein negatives R² ist möglich, weil es anders als Accuracy keine Untergrenze bei 0 gibt. Das ist kein Scheitern, sondern ein valides, ehrlich berichtetes Ergebnis: Die sieben Strukturmerkmale liefern in einem linearen Modell keinen brauchbaren Erklärungsbeitrag für die Höhe der Auffälligkeitsquote — die Ursachen dafür liegen offenbar überwiegend außerhalb der hier erfassten Daten.

### 27. Wie wurde Overfitting vermieden?
Durch `max_depth=3` — der Baum darf maximal drei Ebenen tief verzweigen (bis zu 8 Endknoten), statt beliebig tief zu wachsen und Trainingsdaten auswendig zu lernen. Zusätzlich bestätigt die 5-Fold Cross-Validation (61,6 % ± 3,7 %) die geringe Schwankung über verschiedene Trainings-/Test-Aufteilungen hinweg — ein Hinweis, dass das Ergebnis nicht von einer günstigen Zufallsaufteilung abhängt, sondern die generelle, aber begrenzte Vorhersagekraft der Daten widerspiegelt.

---

## G — Dashboard

### 28. Was kann das Dashboard, und wie hängt es mit dem Modell zusammen?
Ein Streamlit-Dashboard mit vier Seiten: Gesamtüberblick (KPI-Kacheln, Deutschlandkarte, Verteilung), Einflussfaktoren (Merkmal wählen, Gruppen vergleichen), Häuser vergleichen (Filter, ähnliche Krankenhäuser finden) und Qualitätsvorhersage. Die letzte Seite lädt das gespeicherte Decision-Tree-Modell (`Data/modell_krankenhaus.pkl`, per `joblib`) direkt und nutzt es als Risiko-Rechner: Für ein frei wählbares oder neu eingegebenes Krankenhausprofil liefert es eine Live-Vorhersage samt Wahrscheinlichkeit.

---

## H — Grenzen & kritische Reflexion

### 29. Was sind die größten Grenzen eurer Analyse?
Erstens Patientenmix: Häuser mit schwierigeren oder komplexeren Fällen fallen möglicherweise öfter auffällig, ohne dass das ein echtes Qualitätsproblem ist — dieser Faktor steckt nicht in unseren Daten. Zweitens Dokumentation: Manche Auffälligkeiten könnten Dokumentationsfehler statt Versorgungsfehler sein. Drittens Korrelation ≠ Kausalität — kein einziger unserer Befunde beweist eine Ursache-Wirkungs-Beziehung. Und viertens ganz grundsätzlich: Das negative R² zeigt, dass die verfügbaren Strukturmerkmale die eigentliche Höhe der Auffälligkeitsquote kaum erklären.

### 30. Was würdet ihr als Nächstes tun, wenn ihr mehr Zeit hättet?
`QS.Leistungsbereich.csv`, `Notfallversorgung.csv` und `MM.csv` wurden separat geprüft (`04_Potenzielle_Erweiterungen.ipynb`) — zwei davon zeigen dort bereits ein stärkeres Signal als jedes bisherige Merkmal, sind aber noch nicht in die Analysetabelle übernommen. Außerdem: eine Regression mit Patientenstruktur als Kontrollvariable, um den Patientenmix-Einwand aus Frage 29 direkt zu adressieren, sowie ggf. eine Sentiment-Analyse der freitextlichen Kommentare in den Qualitätsberichten.

---

*Stand: siehe Datum der letzten Aktualisierung dieses Dokuments. Quellen: `01_Exploration.md`, `02_Analyse.md`, `03_Decision_Tree.md`, `Aufgabenstellung/Text_Presentation.docx`.*
