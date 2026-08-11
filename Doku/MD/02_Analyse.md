# 📊 02_Analyse.ipynb — Was wurde gemacht und warum?

> Dieses Dokument erklärt Schritt für Schritt, was im Notebook `Notebooks/02_Analyse.ipynb` passiert — und warum jeweils so entschieden wurde. Ergebnis: 12 Grafiken (`grafiken/`), fünf statistische Tests und eine erste inhaltliche Einschätzung, ob Krankenhausmerkmale mit Qualitätsproblemen zusammenhängen.

**Projektfrage:** Welche Krankenhausmerkmale hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme aufweist?

### Übergang von 01_Exploration.ipynb: X und y stehen — jetzt wird verglichen

`01_Exploration.ipynb` hat die Ziel-Variable (y) und 7 Merkmale (X) gebaut und in `Data/analysetabelle.csv` gespeichert (siehe `01_Exploration.md`). Dieses Notebook rührt an den Rohdaten **nicht mehr** — es lädt ausschließlich die fertige Analysetabelle und stellt die eigentliche inhaltliche Frage: **Unterscheiden sich Häuser mit vielen Problemen (`hat_viele_Probleme = 1`) systematisch von Häusern mit wenigen (`= 0`)?** Dafür passiert hier zweierlei, aber noch **kein maschinelles Lernen** (das kommt erst in `03_Decision_Tree.ipynb`):

1. **Deskriptive Analyse** — jedes Merkmal einzeln anschauen: Wie ist es verteilt? Unterscheiden sich die beiden Gruppen sichtbar?
2. **Inferenzstatistik** — die sichtbaren Unterschiede aus Schritt 1 statistisch absichern: Ist ein beobachteter Unterschied „echt" (statistisch signifikant) oder könnte er auch reiner Zufall sein?

---

## 1. Setup & Daten laden

**Was:** `Data/analysetabelle.csv` geladen, `SO.Latitude`/`SO.Longitude` von Komma- auf Punkt-Dezimalschreibweise umgestellt (dieselbe Fallstricke wie in `01_Exploration.ipynb`, hier nochmal nötig, weil dieses Notebook unabhängig von jenem läuft). Einheitliches Farbschema festgelegt: 🟢 Grün = wenige Probleme, 🔴 Rot = viele Probleme — zieht sich durch alle 12 Grafiken.

**Ergebnis:** 1.824 Zeilen × 18 Spalten, Ziel-Variable verteilt auf 925 (wenige Probleme) vs. 899 (viele Probleme).

---

## 2. Jedes Merkmal einzeln betrachten (Grafiken 1–7, 11–12)

### Warum einzeln, bevor man Zusammenhänge sucht?

Erst muss jedes Merkmal für sich geprüft werden — sinnvoll verteilt? Ausreißer? Gruppen überhaupt unterschiedlich? — sonst würde man Tests auf Merkmale anwenden, die offensichtlich nichts hergeben, oder Ausreißer übersehen, die das Ergebnis verzerren.

### Grafik 1 — Verteilung der auffällig-Quote

![Grafik 1 — Verteilung der auffällig-Quote](../../grafiken/g1_auffaellig_quote.png)

**Was ist das:** `auffaellig_quote` ist die kontinuierliche Vorstufe der Ziel-Variable (`01_Exploration.md` Kap. 3): pro Haus (Anzahl auffälliger Qualitätsindikatoren) ÷ (Anzahl aller bewerteten Indikatoren). Ein Qualitätsindikator ist eine vom **IQTIG** (Institut für Qualitätssicherung und Transparenz im Gesundheitswesen, im Auftrag des **G-BA** / Gemeinsamer Bundesausschuss) festgelegte Messgröße je Behandlung. Liegt der Wert außerhalb des IQTIG-Referenzbereichs, gilt der Indikator als „auffällig" (Code `R*`), sonst „nicht auffällig" (`N01`/`N02`) — ein statistisches Signal, kein automatisches Qualitätsurteil. `hat_viele_Probleme` (die eigentliche 0/1-Ziel-Variable) wird erst daraus abgeleitet: 1, wenn die Quote über dem Median liegt.

**Diagramm lesen:** X-Achse = Quote in % (0–100), Y-Achse = Anzahl Häuser, 30 gleich breite Balken — nur die Höhe zeigt, wie viele der 1.824 Häuser in diesen Bereich fallen. Die dunkle Linie mit Punkten verbindet die Balkenspitzen und macht die genauen Y-Werte leichter ablesbar. **Farbe der Balken:** Blau = Balken links vom Median (Quote ≤ 77 %, Gruppe „Wenige Probleme"), Orange = Balken rechts vom Median (Quote > 77 %, Gruppe „Viele Probleme"). Die graue gestrichelte Linie markiert den Median als Trennwert.

**Befund:** Zwei getrennte Muster. Ein breiter Hügel von ~40–85 % (Mehrheit der Häuser, normal gestreut) — plus ein eigenständiger, höchster Balken exakt bei 100 % mit **393 Häusern (21,5 %)**. Grund: Diese Häuser haben im Median nur **2 bewertete Indikatoren** (statt 68 bei den übrigen) — bei so wenigen reicht es, dass beide zufällig auffällig sind, um auf 100 % zu kommen (kleine-Zahlen-Effekt, kein echtes Qualitätssignal). Praktische Folge: **43,7 %** der 899 Häuser mit `hat_viele_Probleme = 1` stammen aus genau dieser Spitze — ihre Ziel-Variable beruht auf sehr wenigen Messwerten und ist entsprechend unsicherer.

**Medianlinie = grau gestrichelt:** `ax.axvline(median, color="gray", linestyle="--", ...)` — Median ist 0,7692, als **77 %** beschriftet. Das ist genau der Schwellenwert, mit dem `hat_viele_Probleme` gebaut wurde. (In früheren Versionen war diese Linie rot — geändert auf grau, damit sie sich farblich von den Balken abhebt ohne eine eigene Bedeutung zu suggerieren.)

**Warum das wichtig ist:** Bevor man Gruppen vergleicht, muss man wissen, wie die Ziel-Variable selbst aussieht. Die 100 %-Spitze ist eine echte Einschränkung: Bei Häusern mit wenigen Indikatoren ist die Quote statistisch unsicherer als bei Häusern mit vielen — im Hinterkopf behalten bei der Interpretation in Kapitel 3/4.

### Grafik 2 — Bettenzahl

![Grafik 2 — Bettenzahl](../../grafiken/g2_bettenzahl.png)

**Diagramm lesen:**
- **Links (Histogramm):** X-Achse = Bettenzahl, Y-Achse = Anzahl Häuser. **"Gekappt bei 1.500" heißt konkret:** Das größte Haus im Datensatz hat 3.011 Betten, aber nur 11 von 1.824 Häusern haben überhaupt mehr als 1.500 Betten. Ohne Kappung müsste die X-Achse bis 3.011 reichen — dann würden sich fast alle Häuser (Median: 190 Betten) in einem winzigen Streifen ganz links zusammendrängen, kaum noch als Balken erkennbar, nur um Platz für diese 11 Ausreißer zu schaffen. Die Kappung (`clip(upper=1500)`) setzt für die Darstellung alle Werte über 1.500 einfach auf 1.500 — die 11 Großkliniken landen dadurch gesammelt im letzten Balken, und die eigentlich interessante Verteilung der übrigen 1.813 Häuser bleibt gut lesbar. Die echten Daten in `analysetabelle.csv` sind davon nicht betroffen, nur dieses eine Diagramm. Man sieht: die meisten Häuser haben wenige Betten (Spitze bei ~100–200), nach rechts wird es schnell dünner.
- **Rechts (Boxplot):** Zeigt dieselbe Bettenzahl, aber getrennt nach Gruppe (grün = wenige, rot = viele Probleme) — **hier nicht gekappt**, deshalb reicht die Y-Achse bis 3.000. Die **Box** umfasst die mittleren 50 % der Häuser (25.–75. Perzentil), der Strich in der Box ist der **Median**, die **Antennen** (Striche nach oben/unten) zeigen den typischen Wertebereich außerhalb der Box, und jeder einzelne **Punkt** darüber ist ein statistischer Ausreißer (ein Haus, das deutlich aus dem Rahmen fällt — bis hin zu einem Einzelfall mit ca. 3.000 Betten).

**Was:** Histogramm der Bettenzahl (gekappt bei 1.500, damit einzelne Großkliniken die Skala nicht verzerren) + Boxplot Bettenzahl MIT vs. OHNE viele Probleme.

**Befund:** Man vergleicht die Bettenzahl der beiden Gruppen aus dem Boxplot. Gruppe "wenige Probleme" (925 Häuser): mittlere 50 % liegen zwischen 120 und 384 Betten, Median 214. Gruppe "viele Probleme" (899 Häuser): mittlere 50 % liegen zwischen 83 und 321 Betten, Median 170. Die Mediane liegen zwar 44 Betten auseinander, aber die beiden Bereiche (120–384 vs. 83–321) **überlappen sich fast vollständig** — ein 200-Betten-Haus ist in beiden Gruppen ganz normal. Deshalb: **kein klarer Größenunterschied.** Würde man raten, ob ein Haus zur einen oder anderen Gruppe gehört, würde die Bettenzahl allein kaum helfen.

**Warum interessiert uns das:** Hypothese: größere Häuser haben mehr Fälle und andere Auffälligkeitsmuster. Bettenzahl allein erklärt aber praktisch nichts — auch das ein valides Ergebnis.

### Grafik 3 — Trägerschaft

![Grafik 3 — Trägerschaft](../../grafiken/g3_traegerschaft.png)

**Diagramm lesen:** X-Achse = die drei Trägerarten. Y-Achse = Prozent. Pro Trägerart stehen **zwei Balken nebeneinander**: grün = Anteil der Häuser dieser Trägerart mit wenigen Problemen, rot = Anteil mit vielen Problemen. Wichtig: Grün + Rot ergeben für jede Trägerart zusammen **100 %** — die Balken zeigen also nicht absolute Hauszahlen, sondern die interne Aufteilung innerhalb jeder Trägerart. Bei "privat" z. B. ist der rote Balken höher als der grüne: Von allen privaten Häusern hat die Mehrheit viele Probleme.

**Was:** Balkendiagramm — Anteil `hat_viele_Probleme = 1` je Trägerart.

**Befund:** Privat 56,5 %, freigemeinnützig 46,4 %, öffentlich 46,7 % haben viele Probleme.

**Warum interessiert uns das:** Hypothese: Träger könnten unterschiedliche Qualitätsanreize haben (z. B. Kostendruck bei privaten Häusern). Bislang der **klarste Unterschied** — aber noch kein statistischer Beweis (Kapitel 4 dieses Dokuments) und noch nicht um Störfaktoren bereinigt (Grafik 10).

### Grafik 4 — Uni-Kliniken vs. normale Häuser

![Grafik 4 — Uni-Kliniken vs. normale Häuser](../../grafiken/g4_uni.png)

**Diagramm lesen:** Anders als bei Grafik 3 steht hier **pro Gruppe nur ein Balken** — die Farben (blau/orange, siehe Legende) unterscheiden lediglich die beiden Gruppen, sie bedeuten nicht "wenige/viele Probleme". Die Balkenhöhe ist jeweils der **Anteil der Häuser dieser Gruppe, die viele Probleme haben**; der Rest zu 100 % ist nicht eingezeichnet. Die Legende nennt zusätzlich die Gruppengröße: 1.731 normale Häuser gegenüber nur 93 Uni-Kliniken — die Uni-Gruppe ist also klein, was ihr Ergebnis unsicherer macht.

**Befund:** Uni-Kliniken 47,3 % vs. normale Häuser 49,4 % — kaum Unterschied.

**Warum interessiert uns das:** Uni-Kliniken behandeln oft schwerere Fälle — höhere oder (durch bessere Ausstattung) niedrigere Auffälligkeit wären beide plausibel. Ergebnis: praktisch kein Unterschied.

### Grafik 5 + 6 — Fortbildungsquote & Ärzte pro Bett

![Grafik 5+6 — Fortbildungsquote & Ärzte pro Bett](../../grafiken/g5_6_fortbildung_aerzte.png)

**Diagramm lesen:** Zwei Boxplots nebeneinander — links das Merkmal `fortbildungsquote`, rechts `aerzte_pro_bett`. Beide sind **eigenständige Diagramme mit eigener Y-Achse**; die Höhen sind untereinander nicht vergleichbar, nur jeweils innerhalb eines Diagramms. In jedem Diagramm stehen die beiden Gruppen nebeneinander: **grün = wenige Probleme, rot = viele Probleme** (durchgängiges Farbschema des Projekts). Aufbau jeder Box wie bei Grafik 2: Die Box umfasst die mittleren 50 % der Häuser, der waagerechte Strich darin ist der **Median**, die Antennen zeigen den übrigen Wertebereich. Unterschied zu Grafik 2: Hier sind Ausreißer-Punkte **ausgeblendet** (`showfliers=False`), damit die Boxen nicht von wenigen Extremwerten zusammengedrückt werden.

**Worauf man beim Vergleich achtet:** Nicht die Antennen, sondern **wie stark sich die beiden Boxen gegeneinander verschieben**. Links (Fortbildungsquote) liegen grüne und rote Box praktisch übereinander, beide Mediane sind exakt gleich (0,667) — kein Unterschied. Rechts (Ärzte pro Bett) ist die rote Box sichtbar nach unten verschoben: Bei Häusern mit vielen Problemen liegen die mittleren 50 % zwischen 0,23 und 0,55 Ärzten pro Bett, bei Häusern mit wenigen Problemen zwischen 0,34 und 0,58. Die Boxen überlappen weiterhin stark — das allein macht noch keinen Beweis —, aber anders als links ist hier überhaupt eine Verschiebung da, die sich lohnt, in Kapitel 4 mit einem Test zu prüfen.

**Befund:**
- Fortbildungsquote: Median wenige Probleme = 0,667, viele Probleme = 0,667 — **identisch, kein Unterschied.**
- Ärzte pro Bett: Median wenige Probleme = 0,468, viele Probleme = 0,390 — **sichtbarer Unterschied.**

**Warum interessiert uns das:** Beide waren als plausible Kandidaten motiviert (`01_Exploration.md`, Abschnitt 3+5). Hier trennen sich die Hypothesen zum ersten Mal: Fortbildungsquote scheint **keine** Rolle zu spielen, Ärzte pro Bett schon — wird in Kapitel 4 dieses Dokuments (Inferenzstatistik) statistisch geprüft und ist später (Baustein 4) sogar das wichtigste Merkmal der gesamten Analyse.

**Welche Schlüsse man daraus ziehen sollte:** Zwei unterschiedliche Konsequenzen für zwei Merkmale, die beide plausibel klangen.
- **Fortbildungsquote:** Identische Mediane sind ein starkes Signal, dass hier **kein** Zusammenhang mit Qualitätsproblemen besteht — dieses Merkmal kann man für die weitere Analyse gedanklich zurückstellen, ganz ohne Test.
- **Ärzte pro Bett:** Die sichtbare, aber moderate Verschiebung reicht **allein nicht** als Beweis (dafür überlappen sich die Boxen noch zu stark) — sie reicht aber, um das Merkmal als ernsten Kandidaten für den T-Test in Kapitel 4 dieses Dokuments zu behalten, statt es wie die Fortbildungsquote zu verwerfen. Der optische Eindruck aus diesem Boxplot bestätigt sich dort (p < 0,001) und macht `aerzte_pro_bett` später sogar zum wichtigsten Merkmal im Modell.

> **📌 Was bedeutet „p < 0,001"?** Der **p-Wert** beantwortet eine ganz bestimmte Frage: *Angenommen, es gäbe in Wirklichkeit gar keinen Unterschied zwischen "wenige" und "viele Probleme" — wie wahrscheinlich wäre es dann, per Zufall trotzdem einen Unterschied wie den beobachteten (oder größer) zu messen?* `p < 0,001` heißt: Diese Wahrscheinlichkeit liegt unter 0,1 % — unter 1 von 1.000. Das ist so unwahrscheinlich, dass man die Annahme "kein echter Unterschied" verwirft und den Unterschied als **statistisch signifikant** (also: wahrscheinlich real, nicht nur Stichprobenrauschen) bezeichnet. Übliche Schwelle dafür ist **α = 0,05** (5 %) — alles darunter gilt als signifikant, `p < 0,001` ist also ein besonders starkes Ergebnis. Wichtig: Der p-Wert sagt nichts darüber, **wie groß oder wie wichtig** der Unterschied ist, nur wie unwahrscheinlich er durch reinen Zufall entstanden wäre. Details zum konkreten Test (T-Test) folgen in Kapitel 4 dieses Dokuments.

### Grafik 7 — Bundesland

![Grafik 7 — Bundesland](../../grafiken/g7_bundesland.png)

**Befund:** Saarland (63,2 %) und Schleswig-Holstein (62,5 %) haben den höchsten Anteil, Berlin (33,3 %) und Sachsen-Anhalt (41,8 %) den niedrigsten.

**Warum interessiert uns das:** Region könnte über Landesvorgaben oder Versorgungsstrukturen mit Qualität zusammenhängen. **Einschränkung:** Manche Bundesländer haben nur wenige Häuser (z. B. Saarland: n=19 Häuser) — ein einzelnes Haus kann den Landes-Durchschnitt verschieben. Mit Vorsicht zu lesen.

### Grafik 11 — Pflegekräfte pro Bett 

![Grafik 11 — Pflegekräfte pro Bett](../../grafiken/g11_pflege_pro_bett.png)

**Befund:** Median wenige Probleme = 1,041, viele Probleme = 0,892 — ähnliches Muster wie Ärzte pro Bett (Grafik 6).

**Warum interessiert uns das:** Dieselbe Personalintensitäts-Hypothese wie bei den Ärzten (`01_Exploration.md`, Abschnitt 6). Das ähnliche Muster zu `aerzte_pro_bett` ist ein erster Hinweis, dass beide Merkmale Ähnliches messen (wird in Grafik 8 als Korrelation sichtbar).

### Grafik 12 — Konzernvergleich 

![Grafik 12 — Konzernvergleich](../../grafiken/g12_konzern_vergleich.png)

**Diagramm lesen:** Wie bei Grafik 4 steht hier **pro Gruppe ein Balken** — Höhe = Anteil der Häuser dieser Gruppe mit vielen Problemen. Die Beschriftung über jedem Balken (**n=1.466 Häuser** bzw. **n=358 Häuser**) gibt die **Gruppengröße** an, also wie viele der 1.824 Häuser insgesamt unabhängig bzw. einem Konzern zugehörig sind — nicht zu verwechseln mit der Balkenhöhe (die zeigt nur den *Anteil in Prozent*, nicht die Anzahl).

**Befund:** Konzernhäuser 49,7 % vs. unabhängige Häuser 49,2 % viele Probleme — **praktisch kein Unterschied.**

**Warum interessiert uns das:** Die Hypothese aus `01_Exploration.md` Abschnitt 7 (zentrale Qualitätssicherung im Konzern beeinflusst die Auffälligkeit) bestätigt sich hier schon optisch nicht — beide Balken gleich hoch. Wird in Kapitel 4 dieses Dokuments mit dem Chi²-Test formal bestätigt.

---

## 3. Zusammenhänge zwischen Merkmalen (Grafiken 8–10)

### Übergang: Von Einzelbetrachtung zu Zusammenhängen

Kapitel 2 hat jedes Merkmal isoliert betrachtet. Jetzt geht es um zwei neue Fragen: **Welches Merkmal hängt am stärksten mit der Ziel-Variable zusammen** (Grafik 8), und **hängen die Merkmale auch untereinander zusammen**, sodass ein scheinbarer Befund eigentlich durch ein drittes, verstecktes Merkmal verursacht wird — ein sogenannter **Störfaktor** (Grafik 9–10, ausführlich erklärt bei Grafik 10)?

### Grafik 8 — Korrelationsmatrix

![Grafik 8 — Korrelationsmatrix](../../grafiken/g8_korrelation.png)

**Diagramm lesen:** Sowohl Zeilen als auch Spalten sind dieselben 8 Merkmale — jede Zelle zeigt den Korrelationswert `r` **zwischen dem Zeilen- und dem Spalten-Merkmal**. Die Diagonale (links oben nach rechts unten) ist immer 1,00 — ein Merkmal korreliert perfekt mit sich selbst. Die Matrix ist **gespiegelt**: Die Zelle (`SO.Betten`-Zeile, `total_qi`-Spalte) zeigt denselben Wert wie (`total_qi`-Zeile, `SO.Betten`-Spalte), nämlich 0,68 — man muss also nur eine Hälfte der Matrix wirklich lesen. Die Farbe kodiert die Stärke: **dunkelrot** = starker positiver Zusammenhang (nahe +1), **dunkelblau** = starker negativer Zusammenhang (nahe −1), **blass/weiß** = kein Zusammenhang (nahe 0) — siehe Farbskala rechts. Um zu sehen, wie stark ein Merkmal mit der Ziel-Variable zusammenhängt, sucht man einfach die Zeile (oder Spalte) `hat_viele_Probleme` und liest sie von links nach rechts durch.

**Was:** Pearson-Korrelation (`r`, Wertebereich −1 bis +1) zwischen allen numerischen Spalten, als Heatmap dargestellt.

**Befund — Korrelation mit `hat_viele_Probleme`, sortiert nach Stärke:**

| Merkmal | r | Interpretation |
|---|---|---|
| `total_qi` | −0,28 | stärkste Korrelation — aber ein Struktur-, kein Qualitätsmerkmal (siehe unten) |
| `aerzte_pro_bett` | −0,139 | schwach, aber vorhanden |
| `pflege_pro_bett` | −0,136 | ähnlich stark wie Ärzte/Bett |
| `SO.Betten` | −0,08 | sehr schwach |
| `ist_konzern` | +0,004 | praktisch null |
| `fortbildungsquote` | +0,008 | praktisch null |

**Warum interessiert uns das:** Das ist die kompakteste Zusammenfassung der ganzen deskriptiven Analyse — eine einzige Zahl pro Merkmal statt zwölf einzelner Grafiken. `total_qi` (Anzahl bewerteter Indikatoren pro Haus) ist zwar rechnerisch am stärksten korreliert, sagt aber nichts über Qualität aus — es ist ein reines Strukturmerkmal (wie viele Indikatoren ein Haus überhaupt bewertet bekommt, hängt z. B. von Spezialisierung ab). Der interessantere Befund: `aerzte_pro_bett` (−0,139) und `pflege_pro_bett` (−0,136) korrelieren **fast, aber nicht exakt gleich** stark — in der Heatmap oben werden beide auf zwei Nachkommastellen gerundet als −0,14 angezeigt, was identisch aussieht, aber der Unterschied in der dritten Nachkommastelle ist so klein, dass er praktisch keine Rolle spielt: Beide sind in etwa gleich bedeutsam, deutlich vor allen anderen Merkmalen.

**Wichtiger Nebenbefund:** `aerzte_pro_bett` und `pflege_pro_bett` korrelieren auch **untereinander** recht stark (r ≈ 0,58) — Häuser mit vielen Ärzten pro Bett haben tendenziell auch viel Pflegepersonal pro Bett. Das ist ein Hinweis auf **Multikollinearität**: Beide Merkmale könnten teilweise dieselbe zugrundeliegende Eigenschaft messen („allgemeine Personalausstattung"), nicht zwei komplett unabhängige Informationen.

### Grafik 9 — Scatter: Bettenzahl vs. Ärzte pro Bett

![Grafik 9 — Scatter Bettenzahl vs. Ärzte pro Bett](../../grafiken/g9_scatter_betten_aerzte.png)

**Was:** Streudiagramm, jeder Punkt ein Haus, eingefärbt nach Ziel-Variable.

**Befund:** Kein klares Trennmuster — die grünen (wenige Probleme) und roten (viele Probleme) Punkte überlappen stark.

**Warum interessiert uns das:** Ein Streudiagramm zeigt, ob sich zwei Gruppen anhand von zwei Merkmalen gemeinsam trennen lassen — mehr als eine einzelne Korrelationszahl verrät. Starke Überlappung bestätigt: Mit diesen beiden Merkmalen allein lässt sich kein Haus zuverlässig der einen oder anderen Gruppe zuordnen.

### Grafik 10 — Störfaktor: Trägerschaft × Bettengröße

![Grafik 10 — Störfaktor Trägerschaft × Bettengröße](../../grafiken/g10_stoerfaktor_traeger.png)

> **📌 Was ist ein Störfaktor?** Ein Störfaktor (auch Confounder) ist eine **dritte Variable**, die mit beiden Seiten eines beobachteten Zusammenhangs gleichzeitig zu tun hat und dadurch einen Zusammenhang vortäuschen oder verstärken kann, der bei genauerem Hinsehen ganz oder teilweise etwas anderes erklärt. Konkretes Beispiel hier: Grafik 3 zeigte, dass private Häuser einen höheren Anteil an Qualitätsproblemen haben als andere Trägerarten. Bevor man daraus schließt "privat verursacht schlechtere Qualität", muss man prüfen, ob Träger und Häuser mit vielen Problemen vielleicht beide mit einer dritten Eigenschaft zusammenhängen — hier: der **Größe** des Hauses. Genau das prüft dieses Diagramm.

**Diagramm lesen:** Drei Boxplots nebeneinander, einer pro Trägerart (`privat`, `freigemeinnützig`, `öffentlich`) — Y-Achse ist die Bettenzahl. Aufbau jeder Box wie bei den vorigen Boxplots: Box = mittlere 50 % der Häuser, Strich in der Box = Median, Antennen = übriger Wertebereich (Ausreißer hier ausgeblendet). Anders als bei Grafik 2/5+6 geht es hier **nicht** um "wenige vs. viele Probleme" (keine grün/rot-Einfärbung), sondern rein um die Bettengröße je Trägerart — die drei Farben unterscheiden nur die drei Trägerarten.

**Was:** Boxplot der Bettenzahl, gruppiert nach Trägerart.

**Befund:** Private Häuser sind im Median deutlich kleiner (125 Betten) als freigemeinnützige (217) und öffentliche (233).

**Warum interessiert uns das — der wichtigste Punkt in diesem Abschnitt:** Der Befund bestätigt den Verdacht aus der Störfaktor-Box oben: Private Häuser sind systematisch **kleiner**. Kleinere Häuser haben pro Qualitätsindikator weniger Fälle — das kann die statistische Schwankungsbreite erhöhen und macht es wahrscheinlicher, rein zufällig außerhalb eines Referenzbereichs zu landen. Der scheinbare „Träger-Effekt" aus Grafik 3 könnte also in Wahrheit (ganz oder teilweise) ein **Größen-Effekt** sein, der sich hinter der Trägerart versteckt, statt ein echter Effekt der Trägerschaft selbst. Deshalb wird der Träger-Befund in der Gesamteinschätzung (Kapitel 6) bewusst mit dieser Einschränkung versehen, statt unkommentiert als „privat = schlechter" stehen zu bleiben.

---

### Zwischenstand im Notebook: „Zusammenfassung der deskriptiven Befunde"

Direkt nach Grafik 12 enthält das Notebook eine eigene Markdown-Zelle mit einer kompakten **Kernbefunde-Tabelle**, die alle 12 Grafiken auf einen Blick zusammenfasst (Richtung + Stärke jedes Zusammenhangs mit `hat_viele_Probleme`) — inhaltlich deckt sie sich mit den Einzelbefunden aus Kapitel 2–3 dieses Dokuments, dient im Notebook aber als Brücke, bevor die Befunde im nächsten Schritt statistisch abgesichert werden.

---

## 4. Inferenzstatistik — sind die Unterschiede „echt"?

### Übergang: Von „sieht anders aus" zu „ist wirklich anders"

Kapitel 2 hat gezeigt: Manche Merkmale unterscheiden sich zwischen den Gruppen sichtbar (z. B. Ärzte/Bett), andere nicht (z. B. Fortbildungsquote). Aber ein sichtbarer Unterschied in einer Grafik ist noch kein Beweis — er könnte durch Zufall entstanden sein, besonders bei kleineren Gruppen. **Inferenzstatistik** beantwortet genau diese Frage: Wie wahrscheinlich wäre ein beobachteter Unterschied, *wenn es in Wahrheit gar keinen Unterschied gäbe*? Ist diese Wahrscheinlichkeit sehr klein, gilt der Unterschied als **statistisch signifikant**.

### T-Test: Ärzte pro Bett (Wenige vs. Viele Probleme)

**Was ist ein T-Test:** Ein Test, der prüft, ob sich die **Mittelwerte** zweier Gruppen (hier: wenige/viele Probleme) bei einer numerischen Größe (hier: Ärzte pro Bett) signifikant unterscheiden. Er liefert eine Teststatistik (`t`) und einen **p-Wert** — die Wahrscheinlichkeit, einen mindestens so großen Unterschied rein zufällig zu beobachten, wenn es in Wahrheit keinen echten Unterschied gibt (die so­genannte Nullhypothese H0: „kein Unterschied"). Ist der p-Wert kleiner als das übliche Signifikanzniveau α = 0,05 (5 %), gilt der Unterschied als statistisch abgesichert.

**Befund:** Wenige Probleme Ø = 0,483, viele Probleme Ø = 0,418, t = 6,002, **p < 0,001** → hoch signifikant.

**Warum das wichtig ist:** Der optische Eindruck aus Grafik 6 wird bestätigt — und zwar sehr deutlich (p < 0,001 bedeutet: eine solche Abweichung wäre bei tatsächlich gleichen Mittelwerten extrem unwahrscheinlich, viel weniger als 1 von 1.000 Malen). Das ist der stärkste bestätigte Einzelbefund der gesamten deskriptiven Analyse.

**Hinweis zur Methode:** Verwendet wird `scipy.stats.ttest_ind()` mit Standardeinstellung, also ein Zweistichproben-t-Test unter der Annahme gleicher Varianzen in beiden Gruppen (kein Welch-Test, der das nicht voraussetzt). Bei sehr unterschiedlichen Gruppengrößen oder Varianzen wäre der Welch-Test robuster — das wurde hier nicht separat geprüft.

### T-Test: Pflegekräfte pro Bett *(ergänzt 2026-07-29)*

**Befund:** Wenige Probleme Ø = 1,072, viele Probleme Ø = 0,951, t = 5,846, **p < 0,001** → ebenfalls hoch signifikant, fast identisch stark wie bei den Ärzten.

**Warum das wichtig ist:** Bestätigt den optischen Eindruck aus Grafik 11 statistisch. Zusammen mit der in Kapitel 3 erwähnten Korrelation zwischen `aerzte_pro_bett` und `pflege_pro_bett` (r ≈ 0,58) deutet das darauf hin, dass hier möglicherweise ein gemeinsamer, übergeordneter Effekt „Personalausstattung" gemessen wird, nicht zwei völlig unabhängige Phänomene.

### Chi²-Test: Konzernzugehörigkeit vs. viele Probleme *(ergänzt 2026-07-29)*

**Was ist ein Chi²-Test:** Anders als der T-Test (für numerische Größen) prüft der Chi²-Unabhängigkeitstest, ob zwei **kategoriale** Merkmale (hier: Konzern ja/nein, viele Probleme ja/nein) statistisch voneinander unabhängig sind. Er vergleicht die tatsächlich beobachteten Häufigkeiten in einer Kreuztabelle mit den Häufigkeiten, die man bei völliger Unabhängigkeit erwarten würde.

**Befund (Kreuztabelle):**

| | wenige Probleme | viele Probleme |
|---|---|---|
| unabhängig | 745 | 721 |
| Konzern | 180 | 178 |

χ² = 0,015, **p = 0,90** → **nicht signifikant**, deutlich über α = 0,05.

**Warum das wichtig ist:** Bestätigt Grafik 12 statistisch eindeutig: Es gibt **keinen** nachweisbaren Zusammenhang zwischen Konzernzugehörigkeit und Qualitätsproblemen. Ein p-Wert von 0,90 bedeutet: Ein Unterschied wie der beobachtete (oder größer) wäre bei tatsächlicher Unabhängigkeit in 90 von 100 Fällen zu erwarten — das ist genau das Gegenteil von „unwahrscheinlicher Zufall", also ein klares Nicht-Ergebnis.

### ANOVA: auffällig-Quote nach Trägerschaft

**Was ist eine ANOVA:** Eine einfaktorielle Varianzanalyse testet, ob sich die Mittelwerte von **mehr als zwei** Gruppen (hier: privat/freigemeinnützig/öffentlich, also 3 statt nur 2 wie beim T-Test) gleichzeitig unterscheiden. Sie liefert eine F-Statistik und einen p-Wert; ein signifikantes Ergebnis sagt nur „mindestens eine Gruppe unterscheidet sich von den anderen", aber nicht automatisch welche.

**Befund:** privat Ø = 0,793, freigemeinnützig Ø = 0,745, öffentlich Ø = 0,752, F = 11,323, **p < 0,001** → signifikant.

**Warum das wichtig ist:** Bestätigt statistisch, dass der in Grafik 3 gesehene Unterschied zwischen den Trägerarten nicht zufällig ist. Wichtig ist aber die Einschränkung aus Grafik 10: Dieses Ergebnis ist **nicht** um die Bettengröße bereinigt — die ANOVA allein kann nicht zwischen einem echten Träger-Effekt und einem versteckten Größen-Effekt unterscheiden.

### 95 %-Konfidenzintervalle: Ärzte pro Bett

**Was ist ein Konfidenzintervall:** Ein Wertebereich, der den „wahren" Mittelwert einer Grundgesamtheit mit einer festgelegten Sicherheit (hier 95 %) einschließt — eine Ergänzung zum reinen Punktschätzwert (Mittelwert), die zeigt, wie präzise dieser Schätzwert ist.

**Befund:** Wenige Probleme: [0,468; 0,497], Viele Probleme: [0,402; 0,433].

**Warum das wichtig ist:** Die beiden Intervalle **überlappen sich nicht** — ein weiteres, anschauliches Indiz (neben dem p-Wert des T-Tests) dafür, dass der Unterschied zwischen den Gruppen real und nicht nur Stichprobenrauschen ist.

---

## 5. Pivot-Tabelle: Trägerschaft × Uni-Status

**Was:** Kreuztabelle der durchschnittlichen `auffaellig_quote`, aufgeschlüsselt nach Trägerart (Zeilen) und Uni-Status (Spalten), plus Gesamtspalte je Trägerart.

**Befund (tatsächlicher Notebook-Output):**

| Trägerart | Nicht-Uni | Uni-Klinik | Gesamt |
|---|---:|---:|---:|
| freigemeinnützig | 0,745 | 0,713 | 0,745 |
| privat | 0,793 | 0,791 | 0,793 |
| öffentlich | 0,755 | 0,723 | 0,752 |

Bei freigemeinnützig und öffentlich liegt die Quote der Uni-Kliniken sichtbar niedriger als bei Nicht-Uni-Häusern (−0,032 bzw. −0,032). Bei privaten Häusern ist der Unterschied dagegen minimal (0,793 vs. 0,791) — hier macht der Uni-Status praktisch keinen Unterschied.

**Warum interessiert uns das:** Grafik 4 hatte „Uni-Kliniken vs. alle anderen" nur pauschal verglichen. Die Pivot-Tabelle prüft, ob dieser (schwache) Uni-Effekt **innerhalb jeder Trägerart** gleich aussieht, oder ob er nur durch eine bestimmte Trägerart getrieben wird. Ergebnis: Bei zwei von drei Trägerarten (freigemeinnützig, öffentlich) ist der Uni-Effekt in etwa gleich stark, bei privaten Häusern verschwindet er fast — ein Hinweis, dass der insgesamt schwache Uni-Effekt aus Grafik 4 nicht gleichmäßig über alle Trägerarten verteilt ist, statistisch aber ohnehin zu schwach ist, um daraus mehr als eine Beobachtung abzuleiten.

---

## 6. Grafiken speichern & Gesamteinschätzung

**Was:** Das Notebook ruft per `subprocess.run()` ein externes Skript auf (`../scripts/Grafiken_Speichern.py`), das alle 12 Grafiken noch einmal (identisch zu den Kapiteln 2–3) erzeugt und als PNG in `grafiken/` speichert — diesmal ohne Anzeige im Notebook, nur zum Abspeichern für Dashboard und Präsentation.

> ⚠️ **Defekter Verweis (Stand 2026-08-10):** Der im Notebook aufgerufene Pfad `scripts/Grafiken_Speichern.py` existiert im aktuellen `scripts/`-Ordner nicht mehr — die Datei (unter dem ursprünglichen Namen `grafiken_speichern.py`) wurde im Rahmen einer Aufräumaktion gelöscht. Ein erneuter Lauf dieser Zelle würde daher mit `returncode != 0` fehlschlagen (`FEHLER: ... FileNotFoundError` o. ä.), das im Notebook gespeicherte Zellen-Output ist noch von einem früheren, erfolgreichen Lauf vor der Löschung. Die 12 PNGs in `grafiken/` sind davon nicht betroffen (sie liegen bereits vor), aber ein frischer Notebook-Durchlauf würde an dieser Stelle abbrechen, bis entweder das Skript wiederhergestellt oder diese Zelle entfernt/anders implementiert wird.

**Gesamtfazit des Notebooks:** Keine starken, eindeutigen Zusammenhänge zwischen Strukturmerkmalen und Qualitätsproblemen. Die einzigen statistisch abgesicherten Befunde sind `aerzte_pro_bett` und `pflege_pro_bett` (beide p < 0,001, aber beide nur schwach korreliert, r ≈ −0,14) sowie der Trägerschaft-Unterschied (ANOVA p < 0,001, aber mit dem in Grafik 10 aufgedeckten Größen-Störfaktor). `ist_konzern` und `fortbildungsquote` zeigen dagegen klar **keinen** Zusammenhang.

> **Warum das kein Scheitern ist:** Das Projekt betont durchgehend (siehe `Text_Presentation.docx`, Folie 3–4): Ein Qualitätsbericht-„auffällig" ist kein automatisches Qualitätsurteil, und viele Faktoren, die wirklich zählen könnten (Patientenmix, Spezialisierung, Dokumentationsqualität), stehen gar nicht im Datensatz. **„Kein Zusammenhang ist ein valides Ergebnis"** — die ehrliche Aussage aus dieser Analyse ist, dass Strukturmerkmale allein die Auffälligkeit eines Hauses nur sehr schwach erklären. Das wird in `03_Decision_Tree.ipynb` mit einem R² von nur 0,033 noch einmal zahlenmäßig bestätigt.

---

*Zuletzt aktualisiert: 2026-08-10 — gegen den aktuellen Stand von `Notebooks/02_Analyse.ipynb` (39 Zellen, inkl. Outputs) abgeglichen. Alle Grafik-Befunde und Testergebnisse geprüft (keine Zahlenabweichungen gefunden), Pivot-Tabelle um die volle Drei-Träger-Übersicht ergänzt, neue Notebook-Zusammenfassungszelle referenziert, defekter Skriptverweis in Kapitel 6 dokumentiert.*
