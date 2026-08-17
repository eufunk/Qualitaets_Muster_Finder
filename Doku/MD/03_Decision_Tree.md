# 🤖 03_Decision_Tree.ipynb — Was wurde gemacht und warum?

> Dieses Dokument erklärt Schritt für Schritt, was im Notebook `Notebooks/03_Decision_Tree.ipynb` passiert — und warum jeweils so entschieden wurde. Ergebnis: ein trainierter und gespeicherter Decision-Tree-Klassifikator, drei Grafiken (`grafiken/`) und eine quantitative Aussage darüber, wie gut Strukturmerkmale von Krankenhäusern Qualitätsprobleme vorhersagen können.

> **⚠️ Korrektur (2026-08-14):** Die Ziel-Variable `hat_viele_Probleme` wurde in `01_Exploration.ipynb` korrigiert (`QSErgBewStrukDialog` war zuvor falsch interpretiert). Das Modell wurde mit der korrigierten `Data/analysetabelle.csv` neu trainiert — **alle Kennzahlen in diesem Dokument sind neu** und weichen teils deutlich von der ursprünglichen Version ab (Accuracy 63,6 %→57,0 %, R² auf `auffaellig_quote` sogar negativ statt +3,3 %, Feature-Importance-Rangfolge unverändert, aber Gewichte stark verschoben).

**Projektfrage:** Können Strukturmerkmale eines Krankenhauses (Größe, Träger, Personal, …) maschinell vorhersagen, ob es überdurchschnittlich viele Qualitätsprobleme hat?

**Themen:** Decision Tree, Metriken (Accuracy / Precision / Recall / F1 / Confusion Matrix), R², OOP (`KrankenhausModell`-Klasse), joblib

### Übergang von 02_Analyse.ipynb: Deskriptiv → Prädiktiv

`02_Analyse.ipynb` hat durch Histogramme, Boxplots und statistische Tests gezeigt, **welche** Merkmale mit Qualitätsproblemen zusammenhängen (Ärzte pro Bett, Pflege pro Bett, Trägerschaft) — und welche nicht (Fortbildungsquote, Uni-Status). Dieses Notebook geht einen Schritt weiter: Statt einzelne Merkmale isoliert zu testen, werden **alle sieben Merkmale gleichzeitig** in einem Machine-Learning-Modell kombiniert und gefragt: *Wie gut kann man damit ein Krankenhaus korrekt klassifizieren?*

---

## 0. Grundlagen — Warum Decision Tree, und was ist das für ein Lernverfahren?

### Supervised oder Unsupervised Learning?

Der Decision Tree in diesem Projekt ist **Supervised Learning** (überwachtes Lernen).

Der Unterschied:

| | Supervised Learning | Unsupervised Learning |
|---|---|---|
| **Trainingsdaten** | Jeder Datenpunkt hat ein bekanntes **Label** (= die richtige Antwort, die das Modell lernen soll — hier: ob ein Krankenhaus viele oder wenige Qualitätsprobleme hat) | Keine Labels — nur Merkmale |
| **Ziel** | Lerne aus Beispielen, um neue Fälle einzuordnen | Entdecke selbst Muster und Gruppen |
| **Beispiele** | Entscheidungsbaum, Lineare Regression, Random Forest | K-Means Clustering, PCA |

In diesem Projekt hat **jedes Krankenhaus ein bekanntes Label**: `hat_viele_Probleme = 0` oder `1` — berechnet aus den echten IQTIG-Bewertungen. Das Modell lernt aus diesen 1.821 beschrifteten Beispielen, dann klassifiziert es neue, unbekannte Häuser.

Es handelt sich konkret um **binäre Klassifikation** (zwei Klassen: 0 und 1).

---

### Warum Decision Tree — und nicht ein anderes Modell?

Es gibt viele ML-Modelle: Random Forest, Logistische Regression, Support Vector Machine (SVM), Neuronales Netz, k-Nearest Neighbors. Für dieses Projekt wurde der Decision Tree aus folgenden Gründen gewählt:

**1. Interpretierbarkeit — das wichtigste Argument**
Ein Decision Tree trifft Entscheidungen durch eine Kette von Wenn-Dann-Regeln, die man direkt ablesen kann:
> *„Wenn Ärzte pro Bett > 0,271 → in den meisten Teilästen wahrscheinlich viele Probleme"*

Jede Verzweigung ist in einfacher Sprache erklärbar — ideal für Präsentationen und Berichte an nicht-technische Zielgruppen. Ein Random Forest oder neuronales Netz liefert zwar eine bessere Accuracy, aber man kann nicht nachvollziehen, warum das Modell eine bestimmte Entscheidung getroffen hat (sog. „Black Box").

**2. Passend zum Datensatz und zum R²**
R² (Bestimmtheitsmaß) ist eine Kennzahl, die angibt, wie viel Prozent der Unterschiede zwischen den Häusern durch die Merkmale im Modell erklärt werden können. Ein R² von 1,0 würde bedeuten: das Modell erklärt alles perfekt. Ein R² von 0 bedeutet: das Modell erklärt gar nichts — genauso gut könnte man den Durchschnittswert für alle Häuser vorhersagen. Das R² von **−0,007** zeigt hier: Die lineare Regression auf der Auffälligkeitsquote erklärt **gar nichts** — sie ist sogar minimal schlechter als einfach den Durchschnittswert für alle Häuser vorherzusagen. Die Zusammenhänge im Datensatz sind also für ein lineares Modell nicht nutzbar. Ein komplexes Modell würde diese Schwäche nicht lösen, sondern nur den Trainingsdatensatz auswendig lernen (Overfitting). Ein flacher Baum mit `max_depth=3` ist ehrlich: Er lernt, was lernbar ist, und macht das Limit sichtbar.

**3. Keine Vorverarbeitung der Merkmale nötig**
SVM (Support Vector Machine — ein Algorithmus, der Datenpunkte durch möglichst breite Trennlinien in Klassen aufteilt) und neuronale Netze benötigen skalierte Features (z. B. alle Werte zwischen 0 und 1). Der Decision Tree arbeitet direkt mit den Originalwerten — kein zusätzlicher Schritt, keine Verzerrung durch Skalierung.

**4. Vollständige Bewertbarkeit des Modells**
Der Decision Tree liefert alle relevanten Metriken auf einen Blick: Accuracy, Precision, Recall, F1-Score, Confusion Matrix und Feature Importance. Besonders die Feature Importance ist ein einzigartiger Vorteil — sie zeigt direkt, welche Merkmale das Modell tatsächlich für seine Entscheidungen nutzt und wie stark. Das ermöglicht eine direkte Rückkopplung zur inhaltlichen Analyse aus Baustein 2.

**5. Ergänzung durch Lineare Regression**
Parallel wird eine Lineare Regression eingesetzt, um mit R² eine zweite, unabhängige Perspektive auf die Erklärungskraft der Merkmale zu gewinnen — und um den Vergleich zwischen einem Klassifikationsmodell (Decision Tree) und einem Regressionsmodell (Lineare Regression) auf demselben Datensatz zu ermöglichen.

| Modell | Vorteile | Nachteile | Verwendung hier |
|---|---|---|---|
| **Decision Tree** | Interpretierbar, kein Scaling nötig, Feature Importance | Overfitting-anfällig ohne max_depth | ✅ Hauptmodell |
| Lineare Regression | R²-Metrik, Koeffizienten zeigen Richtung | Nur lineare Zusammenhänge | ✅ Ergänzung |
| Random Forest | Bessere Accuracy, robust | Black Box, kein klares Regelwerk | ❌ Nicht gewählt |
| SVM / Neuronales Netz | Sehr flexibel | Black Box, benötigt Skalierung, komplex | ❌ Nicht gewählt |

---

## 1. Setup & Daten laden

**Was:** Imports, Arbeitsverzeichnis auf Projekt-Root setzen (das Notebook liegt in `/Notebooks/`, alle Pfade sind relativ zur Root), `analysetabelle.csv` laden.

**Bibliotheken:**
- `scikit-learn` — Decision Tree, Metriken, Train-Test-Split, Cross-Validation, Lineare Regression
- `joblib` — Modell serialisieren (Speichern/Laden)
- `matplotlib` — Baumvisualisierung und Confusion Matrix

**Ergebnis:** 1.821 Zeilen × 18 Spalten, dieselbe Datei wie in Baustein 2.

---

## 2. OOP — Modell-Pipeline als Klasse (`KrankenhausModell`)

**Was:** Die gesamte ML-Pipeline ist als Python-Klasse in `model/modell_klasse.py` ausgelagert. Das Notebook importiert sie mit:

```python
from modell_klasse import KrankenhausModell
```

**Warum eine Klasse statt einzelner Funktionen?**
Die Klasse hat einen klaren praktischen Nutzen: Dieselbe `KrankenhausModell`-Klasse wird sowohl hier beim Training als auch im Streamlit-Dashboard (`dashboard_utils.py`) zum Laden und Vorhersagen verwendet — eine einzige Definition, zwei Verwendungsorte, kein doppelter Code.

**Was macht die Klasse?**

| Methode | Aufgabe |
|---|---|
| `__init__(max_depth, random_state)` | Initialisiert `DecisionTreeClassifier` + `LabelEncoder` |
| `prepare(df)` | Features aufbereiten: `KH.Träger.Art` label-encoden → `traeger_enc`, fehlende Werte mit Median auffüllen |
| `fit(X_train, y_train)` | Modell trainieren |
| `evaluate(X_test, y_test)` | Accuracy, Precision, Recall, F1, Confusion Matrix berechnen |
| `save(path)` | Modell mit `joblib.dump()` speichern |
| `load(path)` | Modell mit `joblib.load()` laden (statische Methode) |

**Features (7 Merkmale):**

| Feature | Quelle | Bedeutung |
|---|---|---|
| `SO.Betten` | SO.csv | Krankenhausgröße |
| `SO.Uni` | SO.csv | Uni-Klinik (0/1) |
| `fortbildungsquote` | AM.csv | Anteil fortgebildeter Ärzte |
| `aerzte_pro_bett` | FA.csv | Ärzte-Personalstärke relativ zur Größe |
| `pflege_pro_bett` | AQ.Pflege.csv | Pflege-Personalstärke relativ zur Größe |
| `ist_konzern` | Konzern.csv | Teil eines Krankenhauskonzerns (0/1) |
| `traeger_enc` | SO.csv | Trägerart codiert (freigemeinnützig=0, öffentlich=1, privat=2) |

**Ziel-Variable:** `hat_viele_Probleme` (0 = wenige, 1 = viele) — binäre Klassifikation.

---

## 3. Train-Test-Split & Basislinie

**Was:** Datensatz 80/20 aufgeteilt, stratifiziert nach der Ziel-Variable.

| | Häuser | Anteil |
|---|---|---|
| Training | 1.456 | 80 % |
| Test | 365 | 20 % |

**Warum stratifiziert?** Stratifizieren bedeutet: beim Aufteilen des Datensatzes in Training und Test wird darauf geachtet, dass beide Teile die gleiche **Klassenverteilung** (= das Verhältnis zwischen den zwei Gruppen — hier: wie viel Prozent der Häuser „Viele Probleme" haben und wie viel „Wenige Probleme") haben wie der Gesamtdatensatz. Ohne `stratify=y` könnte der Zufall dafür sorgen, dass Trainings- und Testset unterschiedliche Anteile dieser Gruppen enthalten — z. B. 55 % „Viele Probleme" im Training aber nur 45 % im Test. Mit `stratify=y` wird garantiert, dass beide Sets dieselbe Gruppenverteilung wie der Gesamtdatensatz aufweisen — das macht die Testergebnisse stabiler und vergleichbarer.

**Warum `random_state=42`?** Reproduzierbarkeit: Jeder, der das Notebook erneut ausführt, erhält exakt dieselbe Aufteilung.

**Basislinie (Naiver Vergleichswert):** 50,4 % — stell dir vor, jemand kennt das Modell gar nicht und tippt für jedes Krankenhaus einfach immer „Wenige Probleme". Keine Analyse, kein Rechnen — nur dieser eine Tipp für alle. Da etwas mehr als die Hälfte der Häuser (916 von 1.821 = 50,4 %) tatsächlich zur Gruppe „Wenige Probleme" gehört, wäre dieser blinde Tipp bei 50,4 % der Häuser zufällig richtig. Das ist der Vergleichswert: Unser Modell muss besser sein als dieses blinde Raten, sonst wäre es nutzlos.

---

## 4. Decision Tree trainieren & bewerten

**Hyperparameter:** `max_depth=3` — der Baum darf maximal 3 Ebenen tief verzweigen.

**Warum `max_depth=3` und nicht 4 oder 5?** Mit jeder zusätzlichen Ebene lernt der Baum feinere Unterschiede aus dem Trainingsdatensatz — bis er ihn irgendwann fast auswendig kennt, aber auf neuen, unbekannten Daten schlechter wird (Overfitting). Das Ziel ist ein Modell, das verallgemeinert und nicht nur die 1.456 Trainingshäuser memoriert.

Konkret: Bei `max_depth=3` hat der Baum maximal 8 Endknoten (Blätter). Jede Entscheidungsregel ist im Baumdiagramm direkt ablesbar und erklärbar. Bei `max_depth=5` wären es bis zu 32 Blätter — der Baum würde zwar auf den Trainingsdaten besser abschneiden, aber die 5-Fold Cross-Validation (61,6 %) zeigt, dass die generelle Vorhersagekraft der Daten begrenzt ist. Ein tieferer Baum würde dieses Limit nicht verbessern, sondern nur schwerer interpretierbar und weniger zuverlässig auf neuen Daten.

![Entscheidungsbaum](../../grafiken/decision_tree.png)

**Wie liest man dieses Diagramm?**
Man startet oben am **Wurzelknoten** (erster Kasten ganz oben) und folgt für ein konkretes Krankenhaus dem Pfad nach unten:
- Ist die Bedingung im Kasten **erfüllt** → weiter nach **links**
- Ist die Bedingung **nicht erfüllt** → weiter nach **rechts**

Das wiederholt sich über maximal 3 Ebenen, bis man ein **Blatt** (unterster Kasten ohne weitere Verzweigung) erreicht. Die Farbe des Blattes zeigt die Vorhersage: **orange = Viele Probleme**, **blau = Wenige Probleme**.

Jeder Kasten zeigt außerdem:
- `gini` — wie „gemischt" die Häuser in diesem Knoten noch sind (0 = alle in einer Gruppe, 0,5 = fifty-fifty)
- `samples` — wie viele der 1.456 Trainingshäuser diesen Knoten durchlaufen haben
- `value` — wie viele davon zu jeder Gruppe gehören [Wenige Probleme, Viele Probleme]

**Beispiel** — ein Krankenhaus mit 0,20 Ärzten pro Bett:
1. Wurzel: `aerzte_pro_bett ≤ 0,271` → **ja** (0,20 ≤ 0,271) → nach links
2. Nächste Ebene: weitere Bedingung prüfen → links oder rechts folgen
3. Blatt erreicht: Farbe und `value` zeigen die Vorhersage

### Metriken auf den Testdaten (365 Häuser):

> Die 365 Häuser sind die **20 % des Gesamtdatensatzes**, die beim Train-Test-Split zurückgehalten wurden (1.821 × 0,2 = 364,2 ≈ 365). Das Modell hat diese Häuser während des Trainings nie gesehen — sie dienen als neutrale Prüfung, wie gut das Modell auf unbekannte Daten verallgemeinert.

| Metrik | Wert | Interpretation |
|---|---|---|
| **Accuracy** | **57,0 %** | 57,0 % der Häuser korrekt klassifiziert |
| **Precision** | **55,2 %** | Von allen als "viele Probleme" vorhergesagten Häusern stimmen 55,2 % |
| **Recall** | **70,2 %** | Von allen echten "Viele Probleme"-Häusern wurden 70,2 % erkannt |
| **F1-Score** | **61,8 %** | Harmonisches Mittel aus Precision & Recall |
| Basislinie | 50,4 % | Naiver Classifier: immer die Mehrheitsklasse vorhersagen |
| **Verbesserung** | **+6,6 %** | Mehrwert gegenüber dem naiven Ansatz |

**5-Fold Cross-Validation — was ist das und wozu?**
Bei einem einfachen Train-Test-Split könnte man Glück haben: Vielleicht landen gerade die „leichten" Häuser im Testset, und das Modell sieht besonders gut aus. Um das auszuschließen, wird Cross-Validation eingesetzt: Der gesamte Datensatz wird in 5 gleich große Teile (Faltungen) aufgeteilt. Das Modell wird 5 Mal trainiert und getestet — jedes Mal mit einer anderen Faltung als Testset und den übrigen vier als Training. Am Ende wird der Durchschnitt der 5 Accuracy-Werte berechnet.

Ergebnis hier: **61,6 % ± 3,7 %** — das Modell erreicht im Durchschnitt 61,6 %, mit einer Schwankung von ±3,7 % zwischen den 5 Durchläufen. Der leichte Anstieg gegenüber den 57,0 % auf dem festen Testset ist normal — beide Werte liegen im selben Bereich. Die geringe Streuung von ±3,7 % zeigt, dass das Modell **stabil** ist und nicht von einer günstigen Zufallsaufteilung profitiert hat.

---

**Was bedeuten die einzelnen Metriken konkret?**

**Accuracy — 57,0 %:**
Anteil der Vorhersagen, die das Modell richtig getroffen hat — egal ob „Viele Probleme" oder „Wenige Probleme". Bei 365 Testhäusern hat das Modell bei 208 Häusern die richtige Gruppe vorhergesagt und bei 157 die falsche.

**Precision — 55,2 %:**
Von allen Häusern, bei denen das Modell „Viele Probleme" vorhersagt, hat es in 55,2 % der Fälle recht. Die restlichen 44,8 % sind falsche Alarme — das Modell hat „Viele Probleme" gesagt, aber das Haus hatte in Wirklichkeit wenige.

**Recall — 70,2 %:**
Von allen Häusern, die tatsächlich viele Probleme haben, findet das Modell 70,2 % davon. Die anderen 29,8 % werden übersehen — das Modell sagt „Wenige Probleme", obwohl in Wirklichkeit viele vorliegen.

**Warum ist Recall hier höher als Precision?**
Das Modell ist „großzügig": Es sagt eher „Viele Probleme", auch wenn es sich nicht ganz sicher ist. Dadurch findet es die meisten echten Problemfälle (hoher Recall) — aber es schlägt dafür auch relativ viele falsche Alarme (niedrigere Precision).

**F1-Score — 61,8 %:**
Ein einziger Wert, der Precision und Recall zusammenfasst. Er bestraft Ungleichgewichte: Ein Modell, das Precision auf 100 % treibt, indem es so gut wie nie „Viele Probleme" sagt, bekommt trotzdem einen niedrigen F1-Score, weil der Recall entsprechend tief ist. Der F1-Score von 61,8 % zeigt: das Modell ist mäßig gut, aber kein Ausreißer in eine Richtung.

**Verbesserung +6,6 %:**
Gegenüber dem blinden Tipp (50,4 %) liegt das Modell 6,6 Prozentpunkte höher. Das ist ein kleiner, aber messbarer Mehrwert — was mit dem negativen R² auf der stetigen Auffälligkeitsquote übereinstimmt (siehe Kapitel 7): Die Strukturmerkmale erklären die Qualitätsunterschiede nur sehr schwach.

### Confusion Matrix

**Was ist eine Confusion Matrix und warum interessiert sie uns?**
Accuracy allein sagt nur, wie viele Vorhersagen insgesamt richtig waren — aber nicht, bei welcher Art von Fehlern das Modell danebenliegt: Hat es mehr Häuser übersehen, die eigentlich Probleme haben? Oder hat es zu viele falsche Alarme geschlagen? Die Confusion Matrix zeigt genau das: Sie schlüsselt auf, welche Häuser das Modell richtig erkannt hat und — wichtiger noch — wo es sich geirrt hat und in welche Richtung.

In unserem Fall gibt es zwei mögliche Irrtümer:
- Das Modell sagt „Wenige Probleme", obwohl das Haus tatsächlich viele hat → verpasster Fall
- Das Modell sagt „Viele Probleme", obwohl das Haus tatsächlich wenige hat → falscher Alarm

Diese beiden Fehlertypen haben unterschiedliche Konsequenzen, daher ist es wichtig, sie getrennt zu betrachten.

![Confusion Matrix](../../grafiken/confusion_matrix.png)

> Im Diagramm steht auf der **X-Achse „Predicted label"** (= was das Modell vorhergesagt hat) und auf der **Y-Achse „True label"** (= was tatsächlich der Fall ist, also die echte Gruppe des Krankenhauses laut IQTIG-Daten).

Die Matrix zeigt die vier möglichen Vorhersageergebnisse auf den 365 Testhäusern:

|  | Vorhergesagt: Wenige Qualitätsprobleme | Vorhergesagt: Viele Qualitätsprobleme |
|---|---|---|
| **Tatsächlich: Wenige Qualitätsprobleme** | True Negative (TN) | False Positive (FP) |
| **Tatsächlich: Viele Qualitätsprobleme** | False Negative (FN) | True Positive (TP) |

- **TP** (True Positive): Korrekt als "Viele Probleme" erkannt
- **TN** (True Negative): Korrekt als "Wenige Probleme" erkannt
- **FP** (False Positive, falsche Alarme): Als "Viele" vorhergesagt, tatsächlich "Wenige"
- **FN** (False Negative, verpasste Fälle): Als "Wenige" vorhergesagt, tatsächlich "Viele"

**Wie liest man die Matrix?**
Die Matrix im Diagramm hat 2 Zeilen und 2 Spalten. Die **Zeilen** zeigen, was tatsächlich stimmt (die Realität). Die **Spalten** zeigen, was das Modell vorhergesagt hat.
- Obere linke Zahl → Modell sagt „Wenige", tatsächlich „Wenige" ✅ (TN, korrekt)
- Obere rechte Zahl → Modell sagt „Viele", tatsächlich „Wenige" ❌ (FP, falscher Alarm)
- Untere linke Zahl → Modell sagt „Wenige", tatsächlich „Viele" ❌ (FN, verpasster Fall)
- Untere rechte Zahl → Modell sagt „Viele", tatsächlich „Viele" ✅ (TP, korrekt)

Die Zahlen auf der **Diagonale** (oben links + unten rechts) sind die richtigen Vorhersagen — je größer, desto besser. Die Zahlen **außerhalb der Diagonale** sind die Fehler.

Konkret auf den 365 Testhäusern: TN = 81, FP = 103, FN = 54, TP = 127. Der vergleichsweise niedrige FN-Wert (54) spiegelt den Recall von 70,2 % wider — die meisten echten Problemhäuser werden erkannt. Der hohe FP-Wert (103) spiegelt die niedrigere Precision von 55,2 % wider — dafür schlägt das Modell relativ viele falsche Alarme.

---

## 5. Feature Importance

**Was ist Feature Importance?**
Nach dem Training berechnet der Decision Tree automatisch, wie wichtig jedes Merkmal für seine Entscheidungen war. Das Ergebnis ist eine Prozentzahl pro Merkmal — sie gibt an, wie viel dieses Merkmal zur Gesamtvorhersageleistung beigetragen hat. Alle Werte zusammen ergeben 100 %.

**Warum ist das nützlich?**
Feature Importance beantwortet die Frage: *Welche Merkmale hat das Modell tatsächlich genutzt — und welche haben keine Rolle gespielt?* Das ist eine Rückkopplung zur inhaltlichen Analyse: Wenn das Modell dieselben Merkmale als wichtig einstuft, die auch in den statistischen Tests aus Baustein 2 herausgestochen sind, stärkt das die Glaubwürdigkeit des Ergebnisses.

![Feature Importance](../../grafiken/feature_importance.png)

> **X-Achse „Wichtigkeit"** = Anteil dieses Merkmals an der gesamten Vorhersageleistung des Modells (in %). Ein Wert von 72,8 % bedeutet: fast drei Viertel aller Entscheidungen im Baum basieren allein auf diesem Merkmal, wie stark jedes Merkmal zur Reduktion der Gini-Unreinheit beiträgt — je höher, desto öfter und weiter oben im Baum wird das Merkmal für Verzweigungen genutzt.

| Feature | Importance | Bedeutung |
|---|---|---|
| `aerzte_pro_bett` | **72,77 %** | Wichtigstes Merkmal — bestätigt Befund aus Baustein 2 |
| `SO.Betten` | 16,48 % | Krankenhausgröße |
| `pflege_pro_bett` | 10,75 % | Zweites Personalstärke-Merkmal |
| `traeger_enc` | 0,00 % | Trägerschaft — bei `max_depth=3` nicht genutzt |
| Fortbildungsquote | 0,00 % | Kein Einfluss — bestätigt die statistische Analyse: Fortbildung hängt nicht mit Qualitätsproblemen zusammen |
| Uni-Klinik (ja/nein) | 0,00 % | Kein Einfluss — Uni- und Nicht-Uni-Kliniken unterscheiden sich nicht in ihrer Auffälligkeitsquote |
| `ist_konzern` | 0,00 % | Kein Einfluss auf die 3 Baumebenen |

**Warum `traeger_enc` = 0?** In der korrigierten Auswertung zeigt die ANOVA in `02_Analyse.ipynb` für Trägerschaft **keinen** statistisch signifikanten Zusammenhang mehr (F = 0,031, p = 0,969) — passend dazu spielt `traeger_enc` auch im Decision Tree keine Rolle. Das ist einer der Punkte, an denen sich die Korrektur der Ziel-Variable besonders deutlich auswirkt: In der ursprünglichen, fehlerhaften Berechnung galt Trägerschaft noch als klarster Befund des ganzen Projekts — nach der Korrektur ist dieser Zusammenhang komplett verschwunden.

---

## 7. R²-Metrik — Lineare Regression zum Vergleich

**Was:** Parallel zum Decision Tree wurde eine lineare Regression auf dieselben sieben Features trainiert — einmal auf die binäre Ziel-Variable (0/1), einmal auf die kontinuierliche `auffaellig_quote`.

**Warum zusätzlich R²?** R² ist primär für Regression definiert (Anteil erklärter Varianz) und ergänzt die Klassifikationsmetriken sinnvoll: Er gibt auf der kontinuierlichen Skala an, wie viel von der Variabilität der Auffälligkeitsquote die sieben Strukturmerkmale gemeinsam erklären können.

| Modell | Ziel-Variable | R²-Wert |
|---|---|---|
| Lineare Regression | `hat_viele_Probleme` (0/1) | 0,024 |
| Lineare Regression | `auffaellig_quote` (0–1, stetig) | **−0,007** |

**Interpretation:** R² = −0,007 bedeutet: Die lineare Regression auf der stetigen Auffälligkeitsquote ist **schlechter als der einfachste denkbare Vergleichswert** — nämlich einfach für jedes Haus den Durchschnittswert aller Häuser vorherzusagen. Ein negatives R² ist möglich (anders als bei Accuracy o. Ä. gibt es hier keine Untergrenze bei 0) und bedeutet konkret: Die sieben Strukturmerkmale liefern in einem linearen Modell **keinen brauchbaren Erklärungsbeitrag** für die Höhe der Auffälligkeitsquote — der lineare Zusammenhang ist praktisch nicht vorhanden.

**Lineare Regressionskoeffizienten (`auffaellig_quote`):**

| Feature | Koeffizient | Richtung |
|---|---|---|
| `aerzte_pro_bett` | −0,0487 | Mehr Ärzte → tendenziell niedrigere Quote |
| `pflege_pro_bett` | +0,0178 | Mehr Pflegekräfte → tendenziell höhere Quote |
| `SO.Uni` | +0,0126 | Uni-Klinik → minimal höhere Quote |
| `fortbildungsquote` | +0,0111 | Mehr Fortbildung → minimal höhere Quote |
| `ist_konzern` | +0,0053 | Konzernzugehörigkeit: praktisch kein Effekt |
| `traeger_enc` | +0,0028 | Träger-Codierung: praktisch kein Effekt |
| `SO.Betten` | −0,00001 | Größe: praktisch kein Effekt |

**Richtung ist uneinheitlich:** Nur `aerzte_pro_bett` zeigt noch den erwarteten negativen Zusammenhang (mehr Ärzte pro Bett → tendenziell niedrigere Quote). Bei `pflege_pro_bett` hat sich das Vorzeichen gegenüber der ursprünglichen, fehlerhaften Berechnung umgedreht (jetzt leicht positiv statt negativ) — bei einem R² nahe 0 sind solche Vorzeichen aber ohnehin nicht verlässlich interpretierbar, da das Modell insgesamt keinen belastbaren linearen Zusammenhang gefunden hat.

> ⚠️ **Kein Zusammenhang ist ein valides Ergebnis.** Ein negatives R² bedeutet nicht, dass die Analyse gescheitert ist — es bedeutet, dass die **verfügbaren Strukturdaten** die Höhe der Auffälligkeitsquote linear nicht vorhersagen können. Das ist eine substanzielle inhaltliche Aussage: Die Ursachen für eine hohe oder niedrige Auffälligkeitsquote liegen offenbar überwiegend außerhalb der hier erfassten Strukturmerkmale.

---

## 8. Modell speichern & laden (joblib)

**Was:** Das trainierte `KrankenhausModell`-Objekt wird mit `joblib.dump()` als Pickle-Datei gespeichert:

```
Data/modell_krankenhaus.pkl
```

`joblib` ist gegenüber `pickle` vorzuziehen für NumPy-Arrays und sklearn-Objekte, da es effizienter mit großen Arrays umgeht.

**Probe-Vorhersage (Beispiel-Krankenhaus):**

```python
beispiel = {
    'SO.Betten': 300, 'SO.Uni': 0,
    'fortbildungsquote': 0.8, 'aerzte_pro_bett': 0.4,
    'pflege_pro_bett': 1.0, 'ist_konzern': 0,
    'traeger_enc': 0  # privat
}
```

Für dieses Beispiel-Krankenhaus sagt das Modell **„Viele Probleme"** vorher, mit einer Wahrscheinlichkeit von 60,09 % (gegenüber 39,91 % für „Wenige Probleme").

Das geladene Modell gibt sowohl eine binäre Vorhersage (0/1) als auch Wahrscheinlichkeiten für beide Klassen zurück — Grundlage für die Einzelvorhersage im Streamlit-Dashboard (Tab „Einzelvorhersage").

---

## 9. Zusammenfassung Baustein 4

| Metrik | Wert | Einordnung |
|---|---|---|
| **Accuracy** | **57,0 %** | +6,6 Prozentpunkte über Basislinie (50,4 %) |
| **Precision** | **55,2 %** | Vorhersage "viele Probleme" stimmt etwas öfter als der Zufall |
| **Recall** | **70,2 %** | Die meisten echten Fälle werden erkannt |
| **F1-Score** | **61,8 %** | Ausgewogener Gesamtwert |
| **CV-Accuracy** | **61,6 % ± 3,7 %** | Stabil, kein Overfitting |
| **R²** | **−0,7 %** | Strukturmerkmale erklären die Auffälligkeitsquote linear nicht |
| **Wichtigstes Merkmal** | `aerzte_pro_bett` | 72,8 % Feature Importance |

### Wichtigste Erkenntnisse

1. **Der Baum übertrifft die Basislinie nur knapp** — mit 57,0 % vs. 50,4 % ist das Modell etwas besser als zufälliges Raten, aber weit entfernt von einer zuverlässigen Vorhersage.

2. **`aerzte_pro_bett` ist mit großem Abstand das wichtigste Merkmal** (72,8 %) — konsistent mit Baustein 2 (T-Test: p < 0,0001, deutlicher Unterschied im Boxplot).

3. **Trägerschaft spielt weder im Baum noch in der ANOVA aus Baustein 2 eine Rolle** — nach der Korrektur der Ziel-Variable ist der zuvor „klarste" Trägerschaftseffekt vollständig verschwunden (ANOVA: F = 0,031, p = 0,969).

4. **Negatives R² ist das zentrale Ergebnis:** Krankenhausstruktur allein kann die Höhe der Auffälligkeitsquote linear nicht vorhersagen — das Modell schneidet schlechter ab als die simple Durchschnittsvorhersage. Kein Zusammenhang ist ein valides Ergebnis — und eine relevante, eher ernüchternde Aussage für die Projektfrage.

5. **Modell ist einsatzbereit:** `Data/modell_krankenhaus.pkl` wird direkt vom Streamlit-Dashboard geladen für Live-Einzelvorhersagen.
