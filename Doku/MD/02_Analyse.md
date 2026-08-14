# 📊 02_Analyse.ipynb — Was wurde gemacht und warum?

> Dieses Dokument erklärt Schritt für Schritt, was im Notebook `Notebooks/02_Analyse.ipynb` passiert — und warum jeweils so entschieden wurde. Ergebnis: 12 Grafiken (`grafiken/`), fünf statistische Tests und eine erste inhaltliche Einschätzung, ob Krankenhausmerkmale mit Qualitätsproblemen zusammenhängen.

> **⚠️ Korrektur (2026-08-14):** Die Ziel-Variable `hat_viele_Probleme` wurde in `01_Exploration.ipynb` korrigiert (`QSErgBewStrukDialog` war zuvor falsch interpretiert — R10 wurde als „auffällig" statt korrekt als „nicht auffällig" gezählt, siehe `BI_Analyse`-Dokumentation). Dadurch haben 72,5 % der Krankenhäuser die Gruppe gewechselt, und **mehrere Befunde in diesem Dokument haben sich in der Richtung umgekehrt** — u. a. Bettenzahl, Ärzte/Bett, Pflege/Bett und Trägerschaft. Dieses Dokument beschreibt bereits die korrigierte Version.

**Projektfrage:** Welche Krankenhausmerkmale hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme aufweist?

### Übergang von 01_Exploration.ipynb: X und y stehen — jetzt wird verglichen

`01_Exploration.ipynb` hat die Ziel-Variable (y) und 7 Merkmale (X) gebaut und in `Data/analysetabelle.csv` gespeichert (siehe `01_Exploration.md`). Dieses Notebook rührt an den Rohdaten **nicht mehr** — es lädt ausschließlich die fertige Analysetabelle und stellt die eigentliche inhaltliche Frage: **Unterscheiden sich Häuser mit vielen Problemen (`hat_viele_Probleme = 1`) systematisch von Häusern mit wenigen (`= 0`)?** Dafür passiert hier zweierlei, aber noch **kein maschinelles Lernen** (das kommt erst in `03_Decision_Tree.ipynb`):

1. **Deskriptive Analyse** — jedes Merkmal einzeln anschauen: Wie ist es verteilt? Unterscheiden sich die beiden Gruppen sichtbar?
2. **Inferenzstatistik** — die sichtbaren Unterschiede aus Schritt 1 statistisch absichern: Ist ein beobachteter Unterschied „echt" (statistisch signifikant) oder könnte er auch reiner Zufall sein?

---

## 1. Setup & Daten laden

**Was:** `Data/analysetabelle.csv` geladen, `SO.Latitude`/`SO.Longitude` von Komma- auf Punkt-Dezimalschreibweise umgestellt (dieselbe Fallstricke wie in `01_Exploration.ipynb`, hier nochmal nötig, weil dieses Notebook unabhängig von jenem läuft). Einheitliches Farbschema festgelegt: 🟢 Grün = wenige Probleme, 🔴 Rot = viele Probleme — zieht sich durch alle 12 Grafiken.

**Ergebnis:** 1.821 Zeilen × 18 Spalten, Ziel-Variable verteilt auf 916 (wenige Probleme) vs. 905 (viele Probleme).

---

## 2. Jedes Merkmal einzeln betrachten (Grafiken 1–7, 11–12)

### Warum einzeln, bevor man Zusammenhänge sucht?

Erst muss jedes Merkmal für sich geprüft werden — sinnvoll verteilt? Ausreißer? Gruppen überhaupt unterschiedlich? — sonst würde man Tests auf Merkmale anwenden, die offensichtlich nichts hergeben, oder Ausreißer übersehen, die das Ergebnis verzerren.

### Grafik 1 — Verteilung der auffällig-Quote

![Grafik 1 — Verteilung der auffällig-Quote](../../grafiken/g1_auffaellig_quote.png)

**Was ist das:** `auffaellig_quote` ist die kontinuierliche Vorstufe der Ziel-Variable (`01_Exploration.md` Kap. 1.4): pro Haus (Anzahl auffälliger Qualitätsindikatoren) ÷ (Anzahl aller bewerteten Indikatoren). Ein Qualitätsindikator ist eine vom **IQTIG** (Institut für Qualitätssicherung und Transparenz im Gesundheitswesen, im Auftrag des **G-BA** / Gemeinsamer Bundesausschuss) festgelegte Messgröße je Behandlung. `QSErgBewStrukDialog` liefert dafür sieben Bewertungskategorien; **auffällig** ist alles außer dem Code `R10` (= „im Referenzbereich") und den `N*`-Codes (= „nicht bewertet") — Details siehe `01_Exploration.md`. `hat_viele_Probleme` (die eigentliche 0/1-Ziel-Variable) wird erst daraus abgeleitet: 1, wenn die Quote über dem Median liegt.

**Diagramm lesen:** X-Achse = Quote in % (0–100), Y-Achse = Anzahl Häuser, 30 gleich breite Balken — nur die Höhe zeigt, wie viele der 1.821 Häuser in diesen Bereich fallen. Die dunkle Linie mit Punkten verbindet die Balkenspitzen und macht die genauen Y-Werte leichter ablesbar. **Farbe der Balken:** Blau = Balken links vom Median (Quote ≤ 6 %, Gruppe „Wenige Probleme"), Orange = Balken rechts vom Median (Quote > 6 %, Gruppe „Viele Probleme"). Die graue gestrichelte Linie markiert den Median als Trennwert.

**Befund:** Die Verteilung ist **rechtsschief** — die meisten Häuser liegen zwischen 0 % und 11 % (Q1–Q3), **rund 28 % der Häuser haben sogar exakt 0 %** auffällige Indikatoren. Nur ein dünner, langer Ausläufer reicht bis 100 %: Genau **8 Häuser (0,4 %)** liegen exakt bei 100 %. Grund für diese Spitze: Diese 8 Häuser haben im Median nur **2 bewertete Indikatoren** (statt 36 bei den übrigen) — bei so wenigen reicht es, dass beide zufällig auffällig sind, um auf 100 % zu kommen (kleine-Zahlen-Effekt, kein echtes Qualitätssignal). Diese Spitze ist mit der korrigierten Interpretation viel kleiner geworden als ursprünglich angenommen (früher fälschlich 393 Häuser/21,5 %), weil „auffällig" jetzt seltener ist (Basisrate ~9 % statt ~77 %) — zwei zufällig auffällige Indikatoren in Folge sind entsprechend viel unwahrscheinlicher.

**Medianlinie = grau gestrichelt:** `ax.axvline(median, color="gray", linestyle="--", ...)` — Median ist 0,0588, als **6 %** beschriftet. Das ist genau der Schwellenwert, mit dem `hat_viele_Probleme` gebaut wurde.

**Warum das wichtig ist:** Bevor man Gruppen vergleicht, muss man wissen, wie die Ziel-Variable selbst aussieht. Die extrem schiefe Verteilung (Median 6 %, aber Maximum 100 %) bedeutet: Die meisten Häuser haben nur sehr wenige auffällige Indikatoren — „viele Probleme" ist hier eine **relative**, keine absolute Aussage (siehe Median-Split-Erklärung in `01_Exploration.md`).

### Grafik 2 — Bettenzahl

![Grafik 2 — Bettenzahl](../../grafiken/g2_bettenzahl.png)

**Diagramm lesen:**
- **Links (Histogramm):** X-Achse = Bettenzahl, Y-Achse = Anzahl Häuser. **"Gekappt bei 1.500" heißt konkret:** Das größte Haus im Datensatz hat 3.011 Betten, aber nur 11 von 1.821 Häusern haben überhaupt mehr als 1.500 Betten. Ohne Kappung müsste die X-Achse bis 3.011 reichen — dann würden sich fast alle Häuser (Median: 190 Betten) in einem winzigen Streifen ganz links zusammendrängen, kaum noch als Balken erkennbar, nur um Platz für diese 11 Ausreißer zu schaffen. Die Kappung (`clip(upper=1500)`) setzt für die Darstellung alle Werte über 1.500 einfach auf 1.500 — die 11 Großkliniken landen dadurch gesammelt im letzten Balken, und die eigentlich interessante Verteilung der übrigen 1.810 Häuser bleibt gut lesbar. Die echten Daten in `analysetabelle.csv` sind davon nicht betroffen, nur dieses eine Diagramm. Man sieht: die meisten Häuser haben wenige Betten (Spitze bei ~100–200), nach rechts wird es schnell dünner.
- **Rechts (Boxplot):** Zeigt dieselbe Bettenzahl, aber getrennt nach Gruppe (grün = wenige, rot = viele Probleme) — **hier nicht gekappt**, deshalb reicht die Y-Achse bis 3.000. Die **Box** umfasst die mittleren 50 % der Häuser (25.–75. Perzentil), der Strich in der Box ist der **Median**, die **Antennen** (Striche nach oben/unten) zeigen den typischen Wertebereich außerhalb der Box, und jeder einzelne **Punkt** darüber ist ein statistischer Ausreißer (ein Haus, das deutlich aus dem Rahmen fällt — bis hin zu einem Einzelfall mit ca. 3.000 Betten).

**Was:** Histogramm der Bettenzahl (gekappt bei 1.500, damit einzelne Großkliniken die Skala nicht verzerren) + Boxplot Bettenzahl MIT vs. OHNE viele Probleme.

**Befund:** Man vergleicht die Bettenzahl der beiden Gruppen aus dem Boxplot. Gruppe "wenige Probleme" (916 Häuser): mittlere 50 % liegen zwischen 80 und 315 Betten, Median 166. Gruppe "viele Probleme" (905 Häuser): mittlere 50 % liegen zwischen 126 und 390 Betten, Median 220. Die Mediane liegen 54 Betten auseinander (32,5 % relativ) — das ist real, nachgerechnet per T-Test statistisch signifikant (t=−5,93, p<0,0001), kein Zufall. Die Korrelation ist mit r=+0,14 schwach, aber diesmal **positiv**, und die beiden Bereiche (80–315 vs. 126–390) **überlappen sich stark** — ein 200-Betten-Haus ist in beiden Gruppen ganz normal. Würde man raten, ob ein Haus zur einen oder anderen Gruppe gehört, würde die Bettenzahl allein kaum helfen.

> **⚠️ Richtung umgekehrt gegenüber der ursprünglichen, fehlerhaften Auswertung:** Vorher hatten Häuser mit **wenigen** Problemen den höheren Median (214 vs. 170 Betten, r=−0,08). Mit der korrigierten Ziel-Variable ist es jetzt umgekehrt: Häuser mit **vielen** Problemen sind im Median größer (220 vs. 166 Betten, r=+0,14). Größere Häuser tendieren also jetzt eher zu mehr, nicht weniger, Qualitätsproblemen.

> **📌 Wie passt „statistisch signifikant" zu „schwacher Zusammenhang"?** Das ist kein Widerspruch. Der p-Wert sagt nur: Der Unterschied ist wahrscheinlich real, kein Stichprobenrauschen. Bei einer großen Stichprobe (hier 1.821 Häuser) werden schon kleine, echte Effekte statistisch signifikant. Wie **groß** der Effekt praktisch ist, zeigt die Korrelation (r) — und die ist mit +0,14 schwach: Bettenzahl erklärt nur einen kleinen Teil davon, ob ein Haus viele Probleme hat.

**Warum interessiert uns das:** Hypothese: größere Häuser haben mehr Fälle und andere Auffälligkeitsmuster. Der Unterschied ist zwar statistisch real, aber schwach und praktisch kaum nutzbar, um ein Haus vorherzusagen — auch das ein valides, differenziertes Ergebnis.

### Grafik 3 — Trägerschaft

![Grafik 3 — Trägerschaft](../../grafiken/g3_traegerschaft.png)

**Diagramm lesen:** X-Achse = die drei Trägerarten. Y-Achse = Prozent. Pro Trägerart stehen **zwei Balken nebeneinander**: grün = Anteil der Häuser dieser Trägerart mit wenigen Problemen, rot = Anteil mit vielen Problemen. Wichtig: Grün + Rot ergeben für jede Trägerart zusammen **100 %** — die Balken zeigen also nicht absolute Hauszahlen, sondern die interne Aufteilung innerhalb jeder Trägerart. Bei "privat" z. B. ist der rote Balken höher als der grüne: Von allen privaten Häusern hat die Mehrheit viele Probleme.

**Was:** Balkendiagramm — Anteil `hat_viele_Probleme = 1` je Trägerart.

**Befund:** Privat 43,8 % (n=502), freigemeinnützig 50,6 % (n=607), öffentlich 53,5 % (n=684) haben viele Probleme.

> **⚠️ Richtung umgekehrt gegenüber der ursprünglichen, fehlerhaften Auswertung:** Vorher hatte privat mit 56,5 % den **höchsten** Anteil. Jetzt hat privat mit 43,8 % den **niedrigsten** Anteil — öffentlich liegt jetzt vorn (53,5 %). Wichtig: Die ANOVA in Kapitel 4 zeigt, dass sich die zugrunde liegende kontinuierliche `auffaellig_quote` zwischen den drei Trägerarten praktisch **nicht** unterscheidet (0,0856 / 0,0857 / 0,0872, F=0,03, p=0,97) — dieser Balkendiagramm-Unterschied entsteht vermutlich, weil der Median-Schnitt bei sehr ähnlichen, eng beieinanderliegenden Quoten schon durch kleine Verschiebungen unterschiedlich viele Häuser auf die eine oder andere Seite fallen lässt, nicht durch einen echten Trägereffekt.

**Warum interessiert uns das:** Hypothese: Träger könnten unterschiedliche Qualitätsanreize haben (z. B. Kostendruck bei privaten Häusern). Optisch der auffälligste Unterschied — aber die ANOVA in Kapitel 4 relativiert das deutlich (siehe Warnhinweis oben) und noch nicht um Störfaktoren bereinigt (Grafik 10).

### Grafik 4 — Uni-Kliniken vs. normale Häuser

![Grafik 4 — Uni-Kliniken vs. normale Häuser](../../grafiken/g4_uni.png)

**Diagramm lesen:** Anders als bei Grafik 3 steht hier **pro Gruppe nur ein Balken** — die Farben (blau/orange, siehe Legende) unterscheiden lediglich die beiden Gruppen, sie bedeuten nicht "wenige/viele Probleme". Die Balkenhöhe ist jeweils der **Anteil der Häuser dieser Gruppe, die viele Probleme haben**; der Rest zu 100 % ist nicht eingezeichnet. Die Legende nennt zusätzlich die Gruppengröße: 1.729 normale Häuser gegenüber nur 92 Uni-Kliniken — die Uni-Gruppe ist also klein, was ihr Ergebnis unsicherer macht.

**Befund:** Uni-Kliniken **68,5 %** vs. normale Häuser **48,7 %** — ein deutlicher Unterschied.

> **⚠️ Deutlich anders als in der ursprünglichen, fehlerhaften Auswertung:** Vorher lagen beide Werte nah beieinander (47,3 % vs. 49,4 %, praktisch kein Unterschied). Mit der korrigierten Ziel-Variable zeigt sich jetzt ein deutlicher Unterschied — Uni-Kliniken haben einen fast 20 Prozentpunkte höheren Anteil an „vielen Problemen". Bei nur 92 Uni-Kliniken ist das Ergebnis aber weiterhin mit Vorsicht zu interpretieren (kleine Gruppe).

**Warum interessiert uns das:** Uni-Kliniken behandeln oft schwerere Fälle — höhere oder (durch bessere Ausstattung) niedrigere Auffälligkeit wären beide plausibel. Ergebnis: jetzt ein deutlicher Unterschied zugunsten von mehr Auffälligkeit bei Uni-Kliniken — möglicherweise, weil komplexere Fälle auch mehr/andere Indikatoren auslösen (vgl. `total_qi`-Korrelation, Grafik 8).

### Grafik 5 + 6 — Fortbildungsquote & Ärzte pro Bett

![Grafik 5+6 — Fortbildungsquote & Ärzte pro Bett](../../grafiken/g5_6_fortbildung_aerzte.png)

**Diagramm lesen:** Zwei Boxplots nebeneinander — links das Merkmal `fortbildungsquote`, rechts `aerzte_pro_bett`. Beide sind **eigenständige Diagramme mit eigener Y-Achse**; die Höhen sind untereinander nicht vergleichbar, nur jeweils innerhalb eines Diagramms. In jedem Diagramm stehen die beiden Gruppen nebeneinander: **grün = wenige Probleme, rot = viele Probleme** (durchgängiges Farbschema des Projekts). Aufbau jeder Box wie bei Grafik 2: Die Box umfasst die mittleren 50 % der Häuser, der waagerechte Strich darin ist der **Median**, die Antennen zeigen den übrigen Wertebereich. Unterschied zu Grafik 2: Hier sind Ausreißer-Punkte **ausgeblendet** (`showfliers=False`), damit die Boxen nicht von wenigen Extremwerten zusammengedrückt werden.

**Worauf man beim Vergleich achtet:** Nicht die Antennen, sondern **wie stark sich die beiden Boxen gegeneinander verschieben**. Links (Fortbildungsquote) liegen grüne und rote Box praktisch übereinander, beide Mediane sind exakt gleich (0,667) — kein Unterschied. Rechts (Ärzte pro Bett) ist die rote Box sichtbar **nach oben** verschoben: Bei Häusern mit vielen Problemen liegt der Median höher als bei Häusern mit wenigen Problemen. Die Boxen überlappen weiterhin stark — das allein macht noch keinen Beweis —, aber anders als links ist hier überhaupt eine Verschiebung da, die sich lohnt, in Kapitel 4 mit einem Test zu prüfen.

**Befund:**
- Fortbildungsquote: Median wenige Probleme = 0,667, viele Probleme = 0,667 — **identisch, kein Unterschied.**
- Ärzte pro Bett: Median wenige Probleme = 0,382, viele Probleme = 0,470 — **sichtbarer Unterschied.**

> **⚠️ Richtung umgekehrt gegenüber der ursprünglichen, fehlerhaften Auswertung:** Vorher hatten Häuser mit vielen Problemen den **niedrigeren** Ärzte/Bett-Median (0,390 vs. 0,468). Jetzt ist es umgekehrt: Häuser mit vielen Problemen haben den **höheren** Median (0,470 vs. 0,382). Mehr Ärzte pro Bett geht jetzt tendenziell mit mehr, nicht weniger, Qualitätsproblemen einher.

**Warum interessiert uns das:** Beide waren als plausible Kandidaten motiviert (`01_Exploration.md`, Abschnitt 5). Hier trennen sich die Hypothesen zum ersten Mal: Fortbildungsquote scheint **keine** Rolle zu spielen, Ärzte pro Bett schon — wird in Kapitel 4 dieses Dokuments (Inferenzstatistik) statistisch geprüft und ist auch in `03_Decision_Tree.ipynb` ein wichtiges Merkmal.

**Welche Schlüsse man daraus ziehen sollte:** Zwei unterschiedliche Konsequenzen für zwei Merkmale, die beide plausibel klangen.
- **Fortbildungsquote:** Identische Mediane sind ein starkes Signal, dass hier **kein** Zusammenhang mit Qualitätsproblemen besteht — dieses Merkmal kann man für die weitere Analyse gedanklich zurückstellen, ganz ohne Test.
- **Ärzte pro Bett:** Die sichtbare, aber moderate Verschiebung reicht **allein nicht** als Beweis (dafür überlappen sich die Boxen noch zu stark) — sie reicht aber, um das Merkmal als ernsten Kandidaten für den T-Test in Kapitel 4 dieses Dokuments zu behalten. Der optische Eindruck aus diesem Boxplot bestätigt sich dort (p < 0,0001), jetzt mit umgekehrtem Vorzeichen.

> **📌 Was bedeutet „p < 0,001"?** Der **p-Wert** beantwortet eine ganz bestimmte Frage: *Angenommen, es gäbe in Wirklichkeit gar keinen Unterschied zwischen "wenige" und "viele Probleme" — wie wahrscheinlich wäre es dann, per Zufall trotzdem einen Unterschied wie den beobachteten (oder größer) zu messen?* `p < 0,001` heißt: Diese Wahrscheinlichkeit liegt unter 0,1 % — unter 1 von 1.000. Das ist so unwahrscheinlich, dass man die Annahme "kein echter Unterschied" verwirft und den Unterschied als **statistisch signifikant** (also: wahrscheinlich real, nicht nur Stichprobenrauschen) bezeichnet. Übliche Schwelle dafür ist **α = 0,05** (5 %) — alles darunter gilt als signifikant, `p < 0,001` ist also ein besonders starkes Ergebnis. Wichtig: Der p-Wert sagt nichts darüber, **wie groß oder wie wichtig** der Unterschied ist, nur wie unwahrscheinlich er durch reinen Zufall entstanden wäre. Details zum konkreten Test (T-Test) folgen in Kapitel 4 dieses Dokuments.

### Grafik 7 — Bundesland

![Grafik 7 — Bundesland](../../grafiken/g7_bundesland.png)

**Befund:** Rheinland-Pfalz (64,0 %, n=89) und Sachsen-Anhalt (61,8 %, n=55) haben den höchsten Anteil, Thüringen (36,0 %, n=50) und Baden-Württemberg (37,3 %, n=220) den niedrigsten.

> **⚠️ Andere Bundesländer als in der ursprünglichen, fehlerhaften Auswertung:** Vorher lagen Saarland und Schleswig-Holstein vorn, Berlin und Sachsen-Anhalt hinten. Mit der korrigierten Ziel-Variable ist die Rangfolge komplett anders — Sachsen-Anhalt ist z. B. von „niedrigster Anteil" zu „zweithöchster Anteil" gewechselt.

**Warum interessiert uns das:** Region könnte über Landesvorgaben oder Versorgungsstrukturen mit Qualität zusammenhängen. **Einschränkung:** Manche Bundesländer haben nur wenige Häuser (z. B. Bremen: n=14 Häuser) — ein einzelnes Haus kann den Landes-Durchschnitt verschieben. Mit Vorsicht zu lesen.

### Grafik 11 — Pflegekräfte pro Bett 

![Grafik 11 — Pflegekräfte pro Bett](../../grafiken/g11_pflege_pro_bett.png)

**Befund:** Median wenige Probleme = 0,891, viele Probleme = 1,047 — ähnliches Muster wie Ärzte pro Bett (Grafik 5+6), inklusive derselben Richtungsumkehr.

> **⚠️ Richtung umgekehrt gegenüber der ursprünglichen, fehlerhaften Auswertung:** Vorher hatten Häuser mit vielen Problemen den **niedrigeren** Pflege/Bett-Median (0,892 vs. 1,041). Jetzt haben Häuser mit vielen Problemen den **höheren** Median (1,047 vs. 0,891) — genau wie bei Ärzte pro Bett.

**Warum interessiert uns das:** Dieselbe Personalintensitäts-Hypothese wie bei den Ärzten (`01_Exploration.md`, Abschnitt 6). Das ähnliche (jetzt: gleichgerichtete) Muster zu `aerzte_pro_bett` ist ein erster Hinweis, dass beide Merkmale Ähnliches messen (wird in Grafik 8 als Korrelation sichtbar).

### Grafik 12 — Konzernvergleich 

![Grafik 12 — Konzernvergleich](../../grafiken/g12_konzern_vergleich.png)

**Diagramm lesen:** Wie bei Grafik 4 steht hier **pro Gruppe ein Balken** — Höhe = Anteil der Häuser dieser Gruppe mit vielen Problemen. Die Beschriftung über jedem Balken (**n=1.463 Häuser** bzw. **n=358 Häuser**) gibt die **Gruppengröße** an, also wie viele der 1.821 Häuser insgesamt unabhängig bzw. einem Konzern zugehörig sind — nicht zu verwechseln mit der Balkenhöhe (die zeigt nur den *Anteil in Prozent*, nicht die Anzahl).

**Befund:** Konzernhäuser 52,5 % vs. unabhängige Häuser 49,0 % viele Probleme — **weiterhin praktisch kein Unterschied** (Werte leicht anders als in der ursprünglichen Auswertung, Schlussfolgerung unverändert).

**Warum interessiert uns das:** Die Hypothese aus `01_Exploration.md` Abschnitt 7 (zentrale Qualitätssicherung im Konzern beeinflusst die Auffälligkeit) bestätigt sich hier schon optisch nicht — die Balken liegen nah beieinander. Wird in Kapitel 4 dieses Dokuments mit dem Chi²-Test formal bestätigt.

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
| `total_qi` | +0,241 | stärkste Korrelation — aber ein Struktur-, kein Qualitätsmerkmal (siehe unten) |
| `aerzte_pro_bett` | +0,210 | schwach bis moderat |
| `pflege_pro_bett` | +0,174 | etwas schwächer als Ärzte/Bett |
| `SO.Betten` | +0,138 | schwach |
| `SO.Uni` | +0,087 | sehr schwach |
| `ist_konzern` | +0,028 | praktisch null |
| `fortbildungsquote` | +0,005 | praktisch null |

> **⚠️ Alle Vorzeichen umgekehrt gegenüber der ursprünglichen, fehlerhaften Auswertung:** Vorher waren `total_qi`, `aerzte_pro_bett`, `pflege_pro_bett` und `SO.Betten` **negativ** korreliert. Jetzt sind **alle** Korrelationen mit `hat_viele_Probleme` positiv — konsistent damit, dass 72,5 % der Häuser die Gruppe gewechselt haben. Die Rangfolge der Stärke bleibt ähnlich (`total_qi` weiterhin am stärksten, `fortbildungsquote`/`ist_konzern` weiterhin praktisch bedeutungslos), aber die Richtung jedes einzelnen Zusammenhangs hat sich gedreht.

**Warum interessiert uns das:** Das ist die kompakteste Zusammenfassung der ganzen deskriptiven Analyse — eine einzige Zahl pro Merkmal statt zwölf einzelner Grafiken. `total_qi` (Anzahl bewerteter Indikatoren pro Haus) ist zwar rechnerisch am stärksten korreliert, sagt aber nichts direkt über Qualität aus — es ist ein Strukturmerkmal (wie viele Indikatoren ein Haus überhaupt bewertet bekommt, hängt z. B. von Größe und Spezialisierung ab; mehr bewertete Indikatoren bedeuten auch mehr Gelegenheiten, dass einer davon auffällig ausfällt). Der interessantere Befund: `aerzte_pro_bett` (+0,210) und `pflege_pro_bett` (+0,174) korrelieren ähnlich stark, `aerzte_pro_bett` diesmal klar vor `pflege_pro_bett` (anders als vorher, wo beide fast identisch waren).

**Wichtiger Nebenbefund:** `aerzte_pro_bett` und `pflege_pro_bett` korrelieren auch **untereinander** recht stark (r = 0,577, praktisch unverändert zur ursprünglichen Auswertung) — Häuser mit vielen Ärzten pro Bett haben tendenziell auch viel Pflegepersonal pro Bett. Das ist ein Hinweis auf **Multikollinearität**: Beide Merkmale könnten teilweise dieselbe zugrundeliegende Eigenschaft messen („allgemeine Personalausstattung"), nicht zwei komplett unabhängige Informationen.

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

**Befund:** Private Häuser sind im Median weiterhin deutlich kleiner (125 Betten) als freigemeinnützige (218) und öffentliche (232) — dieser Befund hängt nicht von der Ziel-Variable ab und ist von der Korrektur praktisch unberührt.

**Warum interessiert uns das — der wichtigste Punkt in diesem Abschnitt:** Private Häuser sind systematisch **kleiner**. Kleinere Häuser haben pro Qualitätsindikator weniger Fälle — das kann die statistische Schwankungsbreite erhöhen und macht es wahrscheinlicher, rein zufällig außerhalb eines Referenzbereichs zu landen. Der scheinbare „Träger-Effekt" aus Grafik 3 könnte also (teilweise) ein **Größen-Effekt** sein. Nach der Korrektur zeigt die ANOVA in Kapitel 4 zusätzlich, dass die kontinuierliche Auffällig-Quote sich zwischen den Trägerarten ohnehin praktisch nicht unterscheidet — der Störfaktor-Verdacht aus diesem Abschnitt bleibt also relevant, ist aber inzwischen nicht mehr die einzige Einschränkung zum Träger-Befund.

---

### Zwischenstand im Notebook: „Zusammenfassung der deskriptiven Befunde"

Direkt nach Grafik 12 enthält das Notebook eine eigene Markdown-Zelle mit einer kompakten **Kernbefunde-Tabelle**, die alle 12 Grafiken auf einen Blick zusammenfasst (Richtung + Stärke jedes Zusammenhangs mit `hat_viele_Probleme`) — inhaltlich deckt sie sich mit den Einzelbefunden aus Kapitel 2–3 dieses Dokuments, dient im Notebook aber als Brücke, bevor die Befunde im nächsten Schritt statistisch abgesichert werden.

---

## 4. Inferenzstatistik — sind die Unterschiede „echt"?

### Übergang: Von „sieht anders aus" zu „ist wirklich anders"

Kapitel 2 hat gezeigt: Manche Merkmale unterscheiden sich zwischen den Gruppen sichtbar (z. B. Ärzte/Bett), andere nicht (z. B. Fortbildungsquote). Aber ein sichtbarer Unterschied in einer Grafik ist noch kein Beweis — er könnte durch Zufall entstanden sein, besonders bei kleineren Gruppen. **Inferenzstatistik** beantwortet genau diese Frage: Wie wahrscheinlich wäre ein beobachteter Unterschied, *wenn es in Wahrheit gar keinen Unterschied gäbe*? Ist diese Wahrscheinlichkeit sehr klein, gilt der Unterschied als **statistisch signifikant**.

### T-Test: Ärzte pro Bett (Wenige vs. Viele Probleme)

**Was ist ein T-Test:** Ein Test, der prüft, ob sich die **Mittelwerte** zweier Gruppen (hier: wenige/viele Probleme) bei einer numerischen Größe (hier: Ärzte pro Bett) signifikant unterscheiden. Er liefert eine Teststatistik (`t`) und einen **p-Wert** — die Wahrscheinlichkeit, einen mindestens so großen Unterschied rein zufällig zu beobachten, wenn es in Wahrheit keinen echten Unterschied gibt (die so­genannte Nullhypothese H0: „kein Unterschied"). Ist der p-Wert kleiner als das übliche Signifikanzniveau α = 0,05 (5 %), gilt der Unterschied als statistisch abgesichert.

**Befund:** Wenige Probleme Ø = 0,402 (n=912), viele Probleme Ø = 0,500 (n=904), t = −9,13, **p < 0,0001** → hoch signifikant.

> **⚠️ Richtung umgekehrt gegenüber der ursprünglichen, fehlerhaften Auswertung:** Vorher hatte die Gruppe „wenige Probleme" den höheren Mittelwert (0,483 vs. 0,418, t=6,00). Jetzt hat die Gruppe „viele Probleme" den höheren Mittelwert (0,500 vs. 0,402, t=−9,13) — das negative Vorzeichen von t zeigt nur, in welche Richtung die Differenz geht, die Signifikanz ist unverändert sehr hoch.

**Warum das wichtig ist:** Der optische Eindruck aus Grafik 5+6 wird bestätigt — und zwar sehr deutlich (p < 0,0001 bedeutet: eine solche Abweichung wäre bei tatsächlich gleichen Mittelwerten extrem unwahrscheinlich). Das ist der stärkste bestätigte Einzelbefund der gesamten deskriptiven Analyse — jetzt mit umgekehrtem Vorzeichen: mehr Ärzte pro Bett geht mit mehr, nicht weniger, Qualitätsproblemen einher.

**Hinweis zur Methode:** Verwendet wird `scipy.stats.ttest_ind()` mit Standardeinstellung, also ein Zweistichproben-t-Test unter der Annahme gleicher Varianzen in beiden Gruppen (kein Welch-Test, der das nicht voraussetzt). Bei sehr unterschiedlichen Gruppengrößen oder Varianzen wäre der Welch-Test robuster — das wurde hier nicht separat geprüft.

### T-Test: Pflegekräfte pro Bett *(ergänzt 2026-07-29)*

**Befund:** Wenige Probleme Ø = 0,936 (n=912), viele Probleme Ø = 1,091 (n=905), t = −7,51, **p < 0,0001** → ebenfalls hoch signifikant, in derselben Größenordnung wie bei den Ärzten.

> **⚠️ Richtung umgekehrt gegenüber der ursprünglichen, fehlerhaften Auswertung:** Vorher hatte „wenige Probleme" den höheren Mittelwert (1,072 vs. 0,951). Jetzt hat „viele Probleme" den höheren Mittelwert (1,091 vs. 0,936) — dieselbe Umkehrung wie bei Ärzte pro Bett.

**Warum das wichtig ist:** Bestätigt den optischen Eindruck aus Grafik 11 statistisch. Zusammen mit der in Kapitel 3 erwähnten Korrelation zwischen `aerzte_pro_bett` und `pflege_pro_bett` (r = 0,577) deutet das darauf hin, dass hier möglicherweise ein gemeinsamer, übergeordneter Effekt „Personalausstattung" gemessen wird, nicht zwei völlig unabhängige Phänomene.

### Chi²-Test: Konzernzugehörigkeit vs. viele Probleme *(ergänzt 2026-07-29)*

**Was ist ein Chi²-Test:** Anders als der T-Test (für numerische Größen) prüft der Chi²-Unabhängigkeitstest, ob zwei **kategoriale** Merkmale (hier: Konzern ja/nein, viele Probleme ja/nein) statistisch voneinander unabhängig sind. Er vergleicht die tatsächlich beobachteten Häufigkeiten in einer Kreuztabelle mit den Häufigkeiten, die man bei völliger Unabhängigkeit erwarten würde.

**Befund (Kreuztabelle):**

| | wenige Probleme | viele Probleme |
|---|---|---|
| unabhängig | 746 | 717 |
| Konzern | 170 | 188 |

χ² = 1,277, **p = 0,2585** → **nicht signifikant**, über α = 0,05.

**Warum das wichtig ist:** Bestätigt Grafik 12 statistisch: Es gibt weiterhin **keinen** nachweisbaren Zusammenhang zwischen Konzernzugehörigkeit und Qualitätsproblemen — die Schlussfolgerung ändert sich durch die Korrektur nicht, auch wenn χ² und p-Wert jetzt andere Werte haben als vorher (χ²=0,015, p=0,90). p=0,26 bedeutet: Ein Unterschied wie der beobachtete (oder größer) wäre bei tatsächlicher Unabhängigkeit in rund 26 von 100 Fällen zu erwarten — deutlich über der 5-%-Schwelle, also kein statistisch abgesicherter Zusammenhang.

### ANOVA: auffällig-Quote nach Trägerschaft

**Was ist eine ANOVA:** Eine einfaktorielle Varianzanalyse testet, ob sich die Mittelwerte von **mehr als zwei** Gruppen (hier: privat/freigemeinnützig/öffentlich, also 3 statt nur 2 wie beim T-Test) gleichzeitig unterscheiden. Sie liefert eine F-Statistik und einen p-Wert; ein signifikantes Ergebnis sagt nur „mindestens eine Gruppe unterscheidet sich von den anderen", aber nicht automatisch welche.

**Befund:** privat Ø = 0,0856, freigemeinnützig Ø = 0,0857, öffentlich Ø = 0,0872, F = 0,031, **p = 0,969** → **nicht signifikant**.

> **⚠️ Wichtigste Umkehrung durch die Korrektur:** In der ursprünglichen, fehlerhaften Auswertung war dieses Ergebnis **hoch signifikant** (F=11,32, p<0,001) und galt als „klarster Befund" der ganzen Analyse. Mit der korrigierten Ziel-Variable sind die drei Trägerarten-Mittelwerte praktisch **identisch** (0,0856 / 0,0857 / 0,0872) — die ANOVA findet **keinen** statistisch signifikanten Unterschied mehr. Das relativiert den auf den ersten Blick klaren Balkendiagramm-Unterschied in Grafik 3 erheblich: Dort wird die kontinuierliche Quote erst durch den Median-Split in zwei Gruppen geteilt, und schon kleine, nicht signifikante Unterschiede in der Quote können dabei zu sichtbar unterschiedlichen Prozentsätzen führen.

**Warum das wichtig ist:** Anders als vorher zeigt die ANOVA jetzt, dass der in Grafik 3 sichtbare Unterschied zwischen den Trägerarten **nicht** statistisch abgesichert ist — er könnte allein durch Stichprobenrauschen um den Median-Schnitt herum entstehen. Der in Grafik 10 gezeigte Störfaktor (Bettengröße je Trägerart) bleibt zwar weiterhin ein methodisch relevanter Punkt, ist hier aber zweitrangig geworden: Es gibt schon auf Ebene der kontinuierlichen Quote keinen Trägereffekt, der bereinigt werden müsste.

### 95 %-Konfidenzintervalle: Ärzte pro Bett

**Was ist ein Konfidenzintervall:** Ein Wertebereich, der den „wahren" Mittelwert einer Grundgesamtheit mit einer festgelegten Sicherheit (hier 95 %) einschließt — eine Ergänzung zum reinen Punktschätzwert (Mittelwert), die zeigt, wie präzise dieser Schätzwert ist.

**Befund:** Wenige Probleme: [0,389; 0,416], Viele Probleme: [0,484; 0,516].

> **⚠️ Richtung umgekehrt, Schlussfolgerung unverändert:** Die Zahlenwerte haben sich gedreht (vorher lag „wenige Probleme" mit [0,468; 0,497] höher), aber die Kernaussage bleibt: Die beiden Intervalle **überlappen sich weiterhin nicht**.

**Warum das wichtig ist:** Ein weiteres, anschauliches Indiz (neben dem p-Wert des T-Tests) dafür, dass der Unterschied zwischen den Gruppen real und nicht nur Stichprobenrauschen ist — jetzt mit „viele Probleme" als der Gruppe mit dem höheren Ärzte/Bett-Wert.

---

## 5. Pivot-Tabelle: Trägerschaft × Uni-Status

**Was:** Kreuztabelle der durchschnittlichen `auffaellig_quote`, aufgeschlüsselt nach Trägerart (Zeilen) und Uni-Status (Spalten), plus Gesamtspalte je Trägerart.

**Befund (tatsächlicher Notebook-Output):**

| Trägerart | Nicht-Uni | Uni-Klinik | Gesamt |
|---|---:|---:|---:|
| freigemeinnützig | 0,0864 | 0,0554 | 0,0857 |
| privat | 0,0860 | 0,0605 | 0,0856 |
| öffentlich | 0,0862 | 0,0957 | 0,0872 |

> **⚠️ Anderes Muster als in der ursprünglichen, fehlerhaften Auswertung:** Vorher hatten Uni-Kliniken in **allen drei** Trägerarten eine niedrigere oder gleiche Quote als Nicht-Uni-Häuser. Jetzt ist das Bild gemischt: Bei freigemeinnützig und privat haben Uni-Kliniken weiterhin eine **niedrigere** Quote (−0,031 bzw. −0,026), aber bei öffentlich jetzt eine **höhere** Quote (+0,0095) als Nicht-Uni-Häuser.

**Warum interessiert uns das:** Grafik 4 hatte „Uni-Kliniken vs. alle anderen" nur pauschal verglichen (dort: deutlicher Unterschied, 68,5 % vs. 48,7 %). Die Pivot-Tabelle prüft, ob dieser Effekt **innerhalb jeder Trägerart** gleich aussieht. Ergebnis: Nein — bei freigemeinnützigen und privaten Uni-Kliniken ist die Quote niedriger als bei vergleichbaren Nicht-Uni-Häusern, nur bei öffentlichen Uni-Kliniken ist sie höher. Der in Grafik 4 sichtbare Gesamtunterschied wird also nicht gleichmäßig von allen drei Trägerarten getragen.

---

## 6. Grafiken speichern & Gesamteinschätzung

**Was:** Das Notebook ruft per `subprocess.run()` ein externes Skript auf (`../scripts/Grafiken_Speichern.py`), das alle 12 Grafiken noch einmal (identisch zu den Kapiteln 2–3) erzeugt und als PNG in `grafiken/` speichert — diesmal ohne Anzeige im Notebook, nur zum Abspeichern für Dashboard und Präsentation.

> ⚠️ **Defekter Verweis (weiterhin offen):** Der im Notebook aufgerufene Pfad `scripts/Grafiken_Speichern.py` existiert im aktuellen `scripts/`-Ordner nicht mehr. Ein erneuter Lauf dieser Zelle schlägt daher mit `FileNotFoundError` fehl (wird von der Zelle selbst abgefangen und nur als Text ausgegeben, bricht die Notebook-Ausführung nicht ab). Die 12 PNGs in `grafiken/` sind davon nicht betroffen, zeigen aber weiterhin die **alte, unkorrigierte** Verteilung — sie müssten neu erzeugt werden, sobald das Skript wiederhergestellt oder diese Zelle anders implementiert ist.

**Gesamtfazit des Notebooks (korrigierte Version):** Anders als in der ursprünglichen, fehlerhaften Auswertung zeigen sich jetzt überwiegend **positive** Zusammenhänge: Größere Häuser mit mehr Personal (`aerzte_pro_bett`, `pflege_pro_bett`) und mehr bewerteten Indikatoren (`total_qi`) haben tendenziell **mehr**, nicht weniger, Qualitätsprobleme (alle T-Tests p < 0,0001). Uni-Kliniken zeigen jetzt einen deutlichen Unterschied (68,5 % vs. 48,7 %). Der zuvor als „klarster Befund" geltende Trägerschafts-Unterschied ist nach der Korrektur **nicht mehr statistisch signifikant** (ANOVA F=0,03, p=0,97) — er war vermutlich ein Artefakt des Median-Splits auf einer praktisch identischen Quote, kein echter Trägereffekt. `ist_konzern` und `fortbildungsquote` zeigen weiterhin klar **keinen** Zusammenhang.

> **Warum das kein Scheitern ist:** Das Projekt betont durchgehend (siehe `Text_Presentation.docx`, Folie 3–4): Ein Qualitätsbericht-„auffällig" ist kein automatisches Qualitätsurteil, und viele Faktoren, die wirklich zählen könnten (Patientenmix, Spezialisierung, Dokumentationsqualität), stehen gar nicht im Datensatz. **„Kein Zusammenhang ist ein valides Ergebnis"** — und auch eine **Richtungsumkehr durch eine Datenkorrektur** ist ein valides, dokumentiertes Ergebnis, kein Makel. Ob die Stärke der gefundenen Zusammenhänge praktisch bedeutsam ist, sollte in `03_Decision_Tree.ipynb` mit den ebenfalls korrigierten Daten neu geprüft werden.

---

*Zuletzt aktualisiert: 2026-08-14 — komplett gegen den korrigierten Stand von `Notebooks/02_Analyse.ipynb` (39 Zellen, echte Ausgaben nach Neuausführung gegen die korrigierte `Data/analysetabelle.csv`) abgeglichen. Grund der Korrektur: `QSErgBewStrukDialog` war in `01_Exploration.ipynb` invertiert interpretiert (R10 fälschlich als „auffällig" statt „nicht auffällig"), siehe `BI_Analyse`-Dokumentation. Alle Grafik-Befunde, T-Tests, Chi²-Test, ANOVA, Konfidenzintervalle und die Pivot-Tabelle neu berechnet und mit den tatsächlichen neuen Werten aktualisiert — mehrere Befunde (Bettenzahl, Ärzte/Bett, Pflege/Bett, Trägerschaft, alle Korrelationen) haben dabei die Richtung gewechselt.*
