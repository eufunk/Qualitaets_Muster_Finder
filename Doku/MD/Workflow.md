# 🗂️ Workflow — Qualitäts-Muster-Finder

> Dieses Dokument beschreibt zu jedem Baustein: was gemacht wurde, welche Entscheidungen getroffen wurden und warum.

**Projektfrage:** Welche Krankenhausmerkmale hängen damit zusammen, dass ein Haus überdurchschnittlich viele Qualitätsprobleme aufweist?

---

## <span style="color:#27ae60">📦 Baustein 1 — Daten vorbereiten</span>

<span style="background:#d4edda;color:#155724;padding:2px 8px;border-radius:4px;font-weight:bold">✅ Abgeschlossen</span> &nbsp; **Datum:** 2026-07-27 &nbsp; **Datei:** `01_Exploration.ipynb`

---

### 1.1 Setup

**Entscheidung:** Kein GitHub — das Projekt wird lokal geteilt (per USB / ZIP). Rohdaten bleiben im `Data/`-Ordner und werden nicht weitergegeben. Alle anderen Dateien (Notebooks, CSVs, Dokumentation) können direkt kopiert werden.

---

### 1.2 Datensatz erkunden

**Werkzeug:** Direkte Dateilese-Operationen (erste 3–5 Zeilen jeder CSV-Datei). CSV-Dateien sind Textdateien — Header + Beispieldaten reichen für die Strukturanalyse. Python wird erst für Berechnungen oder Dateien **>50 MB** benötigt.

**Vorgehen:**
1. Alle **86 CSV-Dateien** im `Data/`-Ordner aufgelistet
2. Von jeder Datei Header und 2–5 Beispielzeilen gelesen
3. Präfix-Logik: `SO.*` = Standort, `QS.*` = Qualitätssicherung, `FA.*` = Fachabteilung
4. Verknüpfung: **`SO.QBID`** taucht in fast allen Tabellen auf → universeller Join-Key

**Relevanz-Kriterium:**

| Kategorie | Kriterium |
|-----------|-----------|
| <span style="color:#27ae60">✅ Relevant</span> | Strukturmerkmal (Betten, Träger, Personal, Region, Uni, Fortbildung) ODER QI-Bewertungen |
| <span style="color:#e67e22">⚠️ Möglicherweise</span> | QS-relevante Infos, aber Bedeutung unklar oder nur für Teilgruppen |
| <span style="color:#e74c3c">❌ Nicht relevant</span> | Lookup-Tabellen, nicht-medizinische Angebote, Verwaltungsdaten |

**Ergebnis:** Vollständige Tabelle in `Daten_Inhaltsverzeichnis.md`

> 📄 **Weiterführende Dokumentation:** Die vollständige Analyse aller 86 Dateien mit Begründungen, Analysemethode und farbiger Klassifikationstabelle ist in **`Datensatz_Analyse_Bericht.docx`** dokumentiert.

**Schlüssel-Erkenntnisse:**
- Haupttabelle für Merkmale: **`SO.csv`** (Betten, Bundesland, Trägerart, Uni, Koordinaten)
- Ziel-Variable: **`QS.Qualitätsindikator.csv`** (>50 MB — nur per Python lesbar)
- Fortbildungsquote = `Erbracht / Pflichtige` aus `QS.Fortbildung.csv`

> ⚠️ **DSGVO-Hinweis: Personenbezogene Daten im Data/-Ordner**  
> Zwei Dateien enthalten echte Personendaten (Namen, E-Mail, Telefon von Krankenhauspersonal):
> - **`Personen.csv`** — Kontaktpersonen der Krankenhäuser (Vorname, Nachname, E-Mail, Telefon, Funktion)
> - **`FA.Personen.csv`** — Ärztliche Leitungen der Fachabteilungen (Vorname, Nachname, E-Mail, Telefon)
>
> Diese Dateien sind im `Data/`-Ordner, der per `.gitignore` **nicht** auf GitHub hochgeladen wird. Sie wurden **nicht** in die Analyse einbezogen und sind nicht in `analysetabelle.csv` enthalten. Die Daten stammen aus den öffentlich zugänglichen Qualitätsberichten 2023.

---

### 1.3 Ziel-Variable erstellen

**Quelle:** `QS.Qualitätsindikator.csv` — 29 Spalten, >50 MB

**Bewertungsspalte:** **`QSErgBewStrukDialog`**
- <span style="color:#e74c3c">`R*` (R10, R20, ...) = **rechnerisch auffällig**</span>
- `N99` = nicht bewertet → **ausgeschlossen** (nicht bewertet ≠ unauffällig!)
- <span style="color:#27ae60">`N01/N02` = nicht auffällig</span>

> ⚠️ **Wichtige Entscheidung:** `QSQI.AEKey` ist eine Haus-ID, kein Indikator-Schlüssel! Deduplizierung über `(SO.QBID, QSQI.Indikator)` — ein Fehler hier hätte zu 1 Zeile pro Haus geführt statt ~55 Zeilen.

**Berechnungsschritte:**

| Schritt | Code | Erklärung |
|---------|------|-----------|
| 1 | `QSQI.ArtDesWertes == 'QI'` | Nur echte QI, keine Zählkennzahlen |
| 2 | `QSErgBewStrukDialog != 'N99'` | Nur bewertete Indikatoren |
| 3 | `drop_duplicates(['SO.QBID','QSQI.Indikator'])` | Je Haus+Indikator eine Zeile |
| 4 | `str.startswith('R')` | Auffällig-Flag setzen |
| 5 | `groupby('SO.QBID').agg(count, sum)` | Pro Haus aggregieren |
| 6 | `auffaellig_n / total_qi` | Quote berechnen |
| 7 | `quote > Median → 1` | Binäre Ziel-Variable |

**Ergebnis:** Median-Quote = **76,92 %** | **1.824 Häuser** | ausgewogene Verteilung (899 vs. 925)

---

### 1.4 Merkmale auswählen & Analysetabelle zusammenführen

**Merkmale:**

| Merkmal | Quelle | Berechnung |
|---------|--------|-----------|
| `SO.Betten` | SO.csv | Direkt |
| `KH.Träger.Art` | SO.csv | Direkt |
| `SO.Bundesland` | SO.csv | Direkt |
| `SO.Uni` | SO.csv | Direkt |
| `SO.Latitude / SO.Longitude` | SO.csv | Direkt (für Karte) |
| `fortbildungsquote` | QS.Fortbildung.csv | `Erbracht / Pflichtige` |
| `aerzte_pro_bett` | FA.Personalliste.csv | `Σ Ärzte / SO.Betten` |
| `pflege_pro_bett` *(2026-07-29)* | SO.Personalliste.csv | `Σ Pflegekräfte / SO.Betten` |
| `ist_konzern` *(2026-07-29)* | Konzern.csv | `SO.Standortnummer` in Konzern.csv? → 0/1 |

**Entscheidung:** Zusammenführung vollständig per Skript reproduzierbar — kein manuelles Klicken.

**Analysetabelle (`Data/analysetabelle.csv`):**

| Kennzahl | Wert |
|----------|------|
| Zeilen (Krankenhäuser) | **1.824** |
| Spalten | 18 |
| Ziel-Variable = 1 (viele Probleme) | 899 (49,3 %) |
| Ziel-Variable = 0 (wenige Probleme) | 925 (50,7 %) |
| Fehlende Werte KH.Träger.Art | 28 (1,5 %) |
| Fehlende Werte fortbildungsquote | 33 (1,8 %) |
| Fehlende Werte aerzte_pro_bett | 5 (0,3 %) |
| Fehlende Werte pflege_pro_bett | 4 (0,2 %) |
| Konzernhäuser (ist_konzern=1) | 358 (19,6 %) |

**Wozu wird die Analysetabelle genutzt?** → Rohdaten → Analysetabelle → **alles andere.**

| Baustein | Nutzung |
|----------|---------|
| Baustein 2 | Grafiken direkt aus Tabelle erzeugen |
| Baustein 3 Seite 1 | `hat_viele_Probleme` + Koordinaten → Karte |
| Baustein 3 Seite 2 | Merkmale gruppiert → Vergleichsdiagramme |
| Baustein 3 Seite 3 | Filter → ähnliche Häuser |
| Baustein 4 | `X` = Merkmale, `y` = `hat_viele_Probleme` |

---

### 1.5 Ärzte pro Bett (Ergänzung)

**Quelle:** `FA.Personalliste.csv` × `FA.csv` über `ABTID`

**Vorgehen:**
- Filter: `FA.Personal.Bereich == "Ärzte"`
- `FA.Personal.Anzahl` = Komma-Dezimal → `.str.replace(",", ".")` → float
- Aggregation: Summe pro `ABTID` → pro `FA.QBID` → `aerzte_gesamt / SO.Betten`
- SO.Betten = 0 (Tageskliniken) → NaN — wird nicht aufgefüllt (kein echtes Verhältnis)

**Ergebnisse:** Ø **0,451** Ärzte/Bett | 5 fehlende Werte (4 Tageskliniken)

---

### 1.6 Pflegekräfte pro Bett (Ergänzung, 2026-07-29)

**Hintergrund:** Explizit in `Fragestellung.docx` gefordertes Merkmal — stand lange als offener Punkt in `ToDo.md`. Kollegen im BI-Tool-Vergleich (`BI_Datenanalyse.docx`) empfahlen dafür `AQ.Pflege.csv` oder `FA.Personalliste.csv` mit Pflege-Filter.

**Quelle:** `SO.Personalliste.csv` (direkt, kein Umweg über `FA.csv` nötig)

**Vorgehen:**
- Filter: `SO.Personal.Bereich == "Pflege"`
- Aggregation: Summe pro `SO.QBID` → `pflege_gesamt / SO.Betten`
- **Warum `SO.Personalliste.csv` statt `AQ.Pflege.csv`?** `AQ.Pflege.csv` enthält nur Qualifikationsnachweise, keine Personal-Anzahlen. `SO.Personalliste.csv` hat direkt `SO.QBID` + `SO.Personal.Anzahl`.

**Ergebnisse:** Ø **1,01** Pflegekräfte/Bett | 4 fehlende Werte | Feature Importance im Decision Tree: **23,8 %** (2. wichtigstes Merkmal)

---

### 1.7 Konzernzugehörigkeit (Ergänzung, 2026-07-29)

**Hintergrund:** Von den Kollegen im BI-Tool-Vergleich als „interessante Ergänzung" identifiziert (Konzernhäuser könnten durch zentrale Qualitätssicherung andere QI-Profile haben).

**Quelle:** `Konzern.csv`

> ⚠️ **Bug gefunden und behoben:** `Konzern.csv` nutzt `SO.Standortnummer` als Schlüssel — **nicht** `SO.QBID`. Der erste Join-Versuch verglich versehentlich `Konzern.csv`s `SO.Standortnummer` gegen `SO.csv`s `SO.QBID` → **0 Treffer**, `ist_konzern` war für alle 1.824 Häuser 0. `SO.csv` hat aber selbst eine `SO.Standortnummer`-Spalte, die im ersten Anlauf nicht mit ausgewählt wurde. Nach Korrektur (Vergleich `SO.Standortnummer` gegen `SO.Standortnummer`): **358 von 1.824 Häusern (19,6 %)** sind Konzernhäuser.

**Ergebnis:** Chi²-Test zeigt **keinen** signifikanten Zusammenhang zwischen `ist_konzern` und `hat_viele_Probleme` (χ²=0,015, p=0,90). Der Decision Tree bestätigt das mit **0 % Feature Importance**. Bewusst trotzdem im Modell gelassen — das Modell soll selbst entscheiden, kein Zusammenhang ist ein valider Befund.

---

## <span style="color:#2980b9">📊 Baustein 2 — Deskriptive Analyse</span>

<span style="background:#d4edda;color:#155724;padding:2px 8px;border-radius:4px;font-weight:bold">✅ Abgeschlossen</span> &nbsp; **Datum:** 2026-07-27 &nbsp; **Datei:** `02_Analyse.ipynb`

---

### 2.1 Vorgehen

12 Grafiken aus `Data/analysetabelle.csv`. Jede Grafik mit automatisch berechnetem Befundsatz. Farbschema: 🟢 grün = wenige Probleme, 🔴 rot = viele Probleme. Grafiken gespeichert in `grafiken/`. Grafik 11 (Pflegekräfte/Bett) und Grafik 12 (Konzernvergleich) am 2026-07-29 ergänzt.

---

### 2.2 Befunde

| Grafik | Merkmal | Befund |
|--------|---------|--------|
| 1 | auffällig-Quote | Median **77 %**, linkssteil — meisten Häuser zwischen 60–90 % |
| 2 | Bettenzahl | Median: wenige=214, viele=170 — kein klarer Größenunterschied |
| 3 | Trägerschaft | Privat **56,5 %** vs. freigemeinnützig 46,4 % vs. öffentlich 46,7 % |
| 4 | Uni-Klinik | Uni 47,3 % vs. Normal 49,4 % — kaum Unterschied |
| 5+6 | Fortbildung & Ärzte/Bett | Fortbildung: kein Unterschied; Ärzte/Bett: wenige=0,468, viele=0,390 |
| 7 | Bundesland | Saarland höchster Anteil **(63,2 %)**, Berlin niedrigster (33,3 %) |
| 8 | Korrelation | Stärkste Korrelation: `total_qi` **(r=−0,28)**, `aerzte_pro_bett` (r=−0,14) |
| 9 | Scatter | Kein klares Trennmuster — starke Überlappung |
| 10 | Störfaktor | Private Häuser kleiner (Md=125 Betten) — Trägereffekt mit Vorsicht |
| 11 *(2026-07-29)* | Pflegekräfte/Bett | Wenige=1,041, Viele=0,892 — ähnliches Muster wie Ärzte/Bett |
| 12 *(2026-07-29)* | Konzernvergleich | Konzern 49,7 % vs. unabhängig 49,2 % viele Probleme — praktisch kein Unterschied |

### 2.3 Inferenzstatistik (ergänzt)

| Test | Ergebnis | Befund |
|------|----------|--------|
| **T-Test** Ärzte/Bett (Wenige vs. Viele) | t=6,002, **p<0,001** | Unterschied statistisch **signifikant** |
| **T-Test** Pflegekräfte/Bett (Wenige vs. Viele) *(2026-07-29)* | t=5,846, **p<0,001** | Unterschied statistisch **signifikant** |
| **Chi²-Test** Konzernzugehörigkeit vs. viele Probleme *(2026-07-29)* | χ²=0,015, **p=0,90** | **Kein** signifikanter Zusammenhang |
| **ANOVA** auffällig-Quote nach Träger | F=11,323, **p<0,001** | Mind. eine Gruppe unterscheidet sich signifikant |
| **95%-KI** Ärzte/Bett Wenige | [0,468–0,497] | Kein Überlappung mit Viele-Gruppe |
| **95%-KI** Ärzte/Bett Viele | [0,402–0,433] | Bestätigt signifikanten Unterschied |
| **pivot_table** Träger × Uni | Uni-Kliniken leicht niedrigere Quote | Kein starker Effekt |

### 2.4 Gesamteinschätzung

Keine starken, eindeutigen Zusammenhänge. Stärkster Prädiktor `total_qi` ist ein **Strukturmerkmal**, kein Qualitätsmerkmal. Einziger klarer Befund: private Häuser höherer Anteil — aber Störfaktor Größe möglich.

> 💡 **Kein Zusammenhang ist ein valides Ergebnis.** *(Quelle: Text_Presentation.docx, Folie 7)*

---

## <span style="color:#8e44ad">🖥️ Baustein 3 — Dashboard bauen</span>

<span style="background:#d4edda;color:#155724;padding:2px 8px;border-radius:4px;font-weight:bold">✅ Live</span> &nbsp; **Werkzeug:** Streamlit &nbsp; **Dateien:** `Dashboard/streamlit_dashboard.py`, `Dashboard/dashboard_utils.py`

**Umgesetzt:**
- Seite 1 „Übersicht": Kennzahlen + Deutschland-Karte + Verteilung
- Seite 2 „Vergleiche": Dropdown → Verteilung MIT vs. OHNE viele Probleme, Pivot-Tabelle
- Seite 3 „Ähnliche Häuser": Filter nach Betten / Region / Träger + Einzelhaus-Steckbrief
- Seite 4 „Risiko-Rechner" *(Bonus)*: Decision Tree Vorhersage — seit 2026-07-29 inkl. Eingabefelder für Pflegekräfte/Bett und Konzernstatus

**Deployment:** Streamlit Community Cloud — live unter [Qualitäts-Muster-Finder Dashboard](https://appdashboardpy-dkgplgkkzczyvnwpfjjcsp.streamlit.app/)

**Technischer Hinweis:** `streamlit_dashboard.py` und `dashboard_utils.py` wurden am 2026-07-29 von `scripts/` in einen eigenen `Dashboard/`-Ordner verschoben. `modell_klasse.py` wiederum wurde am 2026-07-30 von `scripts/` in einen eigenen `model/`-Ordner verschoben. Alle drei Ordner sind getrennt — der Import von `modell_klasse` läuft über eine `sys.path`-Ergänzung zur Laufzeit. Der Main-File-Pfad in den Streamlit-Cloud-Einstellungen muss entsprechend aktualisiert werden.

---

## <span style="color:#e67e22">🤖 Baustein 4 — Entscheidungsbaum</span> *(Bonus)*

<span style="background:#d4edda;color:#155724;padding:2px 8px;border-radius:4px;font-weight:bold">✅ Abgeschlossen</span> &nbsp; **Datum:** 2026-07-27, neu trainiert 2026-07-29 &nbsp; **Datei:** `03_Decision_Tree.ipynb`

- **OOP:** Klasse `KrankenhausModell` mit `prepare()`, `fit()`, `evaluate()`, `save()`, `load()` — Notebook importiert die Klasse jetzt aus `model/modell_klasse.py`, statt sie inline zu duplizieren *(behebt einen `__main__`-Pickle-Bug, der das Dashboard beim Laden des Modells crashen ließ)*
- **Train-Test-Split:** 80/20, stratifiziert | Basislinie: 50,7 %
- **Metriken:** Accuracy=0,636 | Precision=0,682 | Recall=0,489 | F1=0,570 | CV=0,597±0,042
- **R²=0,033** — Strukturmerkmale erklären nur 3,3 % der Varianz → bestätigt Baustein 2
- **Feature Importance:** `aerzte_pro_bett` 53,6 %, `pflege_pro_bett` 23,8 %, `SO.Betten` 22,6 % — alle anderen (inkl. `ist_konzern`) 0 %
- **Wichtigster Split:** `aerzte_pro_bett ≤ 0,271`
- **`joblib`:** Modell gespeichert als `Data/modell_krankenhaus.pkl`

---

## <span style="color:#c0392b">🏁 Baustein 5 — Abschluss & Präsentation</span>

<span style="background:#fff3cd;color:#856404;padding:2px 8px;border-radius:4px;font-weight:bold">🟡 Teilweise erledigt</span>

**Erledigt:** Startanleitung (`README.md`), Entscheidungen dokumentiert (`README.md`, `ProjektDetails.md`, dieses Dokument), Komplett-Durchlauf getestet (Rohdaten → alle 3 Notebooks → Dashboard, fehlerfrei)

**Noch offen:** Randfälle im Dashboard testen, Code aufräumen, Entscheidungsbegründungen für Präsentation ausformulieren, Präsentation mit Live-Demo + Generalprobe

---

*Zuletzt aktualisiert: 2026-07-29*

---

## 📁 Erstellte Projektdateien

> Übersicht aller Dateien, die im Laufe des Projekts erstellt wurden — mit Zweck und Baustein-Zuordnung.

### 📒 Notebooks

| Datei | Baustein | Zweck |
|-------|----------|-------|
| `01_Exploration.ipynb` | Baustein 1 | Datenaufbereitung: Ziel-Variable, Merkmale, Analysetabelle, Ärzte/Pflege pro Bett, Konzernzugehörigkeit |
| `02_Analyse.ipynb` | Baustein 2 | Deskriptive Analyse: 12 Grafiken, T-Test, Chi²-Test, ANOVA, Konfidenzintervalle, pivot_table |
| `03_Decision_Tree.ipynb` | Baustein 4 | Decision Tree, OOP (importiert aus model/modell_klasse.py), Metriken, R², Feature Importance, joblib |

### 🖥️ Dashboard

| Datei | Baustein | Zweck |
|-------|----------|-------|
| `Dashboard/streamlit_dashboard.py` | Baustein 3 | Haupt-App: 4 Seiten (Übersicht, Vergleiche, Ähnliche Häuser, Risiko-Rechner) |
| `Dashboard/dashboard_utils.py` | Baustein 3 | Hilfsfunktionen: Daten laden, KPIs, Plots, Modell-Vorhersage |

### 🧠 Modell-Logik (`model/`) *(NEU 2026-07-30, vorher in `scripts/`)*

| Datei | Baustein | Zweck |
|-------|----------|-------|
| `modell_klasse.py` | Baustein 4 | OOP-Wrapper `KrankenhausModell` — einzige Quelle der Wahrheit für Features & Modell-Logik |

### 🐍 Python-Module (`scripts/`)

| Datei | Baustein | Zweck |
|-------|----------|-------|
| `bi_datenanalyse.py` | Baustein 1 | Generiert Word-Dokument: BI-Tool-Vergleich mit Kollegen |
| `datei_uebersicht.py` | Baustein 1 | Generiert Word-Dokument: Datei-Klassifikation (A4) |
| `word_dokumentation.py` | Baustein 1 | Generiert Hauptdokumentation als Word-Datei |
| `analysetabelle_zusammenfassung.py` | Baustein 1 | **NEU (2026-07-30)** Generiert Word-Dokument: Merkmale, Ziel-Variable, Quelltabellen, Merge-Kriterien, Endgröße |
| `grafiken_speichern.py`, `datensatz_bericht.py`, `powerbi_anleitung.py` | — | Interne Hilfsskripte (per `.gitignore` ausgeschlossen) |

### 📊 Datendateien

| Datei | Baustein | Zweck |
|-------|----------|-------|
| `Data/analysetabelle.csv` | Baustein 1 | Finale Analysetabelle: 1.824 Häuser × 18 Spalten — Basis für alles weitere |
| `Data/modell_krankenhaus.pkl` | Baustein 4 | Trainiertes Decision-Tree-Modell (joblib) — bereit für Dashboard |

### 📄 Dokumentation (Word)

| Datei | Inhalt |
|-------|--------|
| `Dokumentation_Qualitaets_Muster_Finder.docx` | Hauptdokumentation: Projektübersicht, Baustein 1+2 komplett mit Ergebnissen und Grafiken |
| `Datensatz_Analyse_Bericht.docx` | Spezialdokumentation Datensatz: Analyse aller 86 CSV-Dateien, Klassifikation, Analysemethode, Datenmodell |

###  Markdown-Dateien

| Datei | Zweck |
|-------|-------|
| `Workflow.md` | Dieses Dokument: Vorgehen, Entscheidungen, Verweise |
| `ToDo.md` | Aufgabenliste nach Baustein-Struktur mit Haken |
| `01_Exploration.md` | Schritt-für-Schritt-Erklärung von `01_Exploration.ipynb` — was gemacht wurde und warum |
| `02_Analyse.md` | **NEU (2026-07-30)** Schritt-für-Schritt-Erklärung von `02_Analyse.ipynb` — was gemacht wurde und warum |
| `Daten_Inhaltsverzeichnis.md` | Tabellarische Übersicht aller 86 CSV-Dateien mit Relevanz-Einstufung |

### 🖼️ Grafiken

| Ordner/Datei | Inhalt |
|-------------|--------|
| `grafiken/g1_auffaellig_quote.png` | Verteilung der auffällig-Quote |
| `grafiken/g2_bettenzahl.png` | Bettenzahl MIT vs. OHNE Probleme |
| `grafiken/g3_traegerschaft.png` | Trägerschaft-Vergleich |
| `grafiken/g4_uni.png` | Uni-Kliniken vs. normale Häuser |
| `grafiken/g5_6_fortbildung_aerzte.png` | Fortbildungsquote & Ärzte/Bett |
| `grafiken/g7_bundesland.png` | Anteil je Bundesland |
| `grafiken/g8_korrelation.png` | Korrelationsmatrix |
| `grafiken/g9_scatter_betten_aerzte.png` | Scatter Bettenzahl vs. Ärzte/Bett |
| `grafiken/g10_stoerfaktor_traeger.png` | Störfaktor Träger × Bettengröße |
| `grafiken/g11_pflege_pro_bett.png` | Pflegekräfte pro Bett MIT vs. OHNE viele Probleme *(2026-07-29)* |
| `grafiken/g12_konzern_vergleich.png` | Konzernhaus vs. unabhängiges Haus *(2026-07-29)* |
| `grafiken/confusion_matrix.png` | Confusion Matrix Decision Tree |
| `grafiken/decision_tree.png` | Visualisierung Entscheidungsbaum |
| `grafiken/feature_importance.png` | Feature Importance Balkendiagramm |
