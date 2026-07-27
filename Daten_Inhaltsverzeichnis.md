---
noteId: "74e3e610898e11f1aab5fd6c420404f8"
tags: []

---

# 📂 Inhaltsverzeichnis — Datensatz Qualitäts-Muster-Finder

> Erstellt: 2026-07-27 | Basis: Manuelles Sichten aller CSV-Dateien (Header + Beispielzeilen)

---

## 🔑 Schlüssel-Spalte: `SO.QBID`

Fast alle Tabellen sind über **`SO.QBID`** verknüpft.  
`SO.QBID` = eindeutige ID eines Krankenhaus-**Standorts**.

---

## ✅ Für das Projekt relevante Tabellen

| Datei | Inhalt | Wichtige Spalten | Rolle im Projekt |
|-------|--------|-----------------|-----------------|
| **SO.csv** | Stammdaten aller Krankenhäuser **(Haupttabelle)** | `SO.QBID`, `SO.Name`, `SO.Betten`, `SO.Bundesland`, `SO.Uni`, `KH.Träger`, `KH.Träger.Art`, `SO.Latitude`, `SO.Longitude`, `SO.Standortnummer` | 🎯 **Kern-Merkmale** (Betten, Region, Träger, Uni) |
| **QS.Qualitätsindikator.csv** | Qualitätsindikatoren mit Bewertungen (>50 MB!) | Spalten noch zu explorieren | 🎯 **Ziel-Variable** (auffällig / nicht auffällig) |
| **QS.csv** | QS-Berichtsbasis pro Standort | `QS.ID`, `QS.IKNummer`, `QS.Land`, `QS.Standortnummer`, `SO.QBID`, `QS.Typ` (bund/land) | 🔗 Verknüpfungstabelle |
| **QS.Fortbildung.csv** | Fortbildungsnachweise der Ärzte pro Haus | `QS.Fortbildungspflichtige`, `QS.Fortbildungsnachweis_Erbracht_Habende`, `QS.Nachweispflichtige`, `SO.QBID` | 🎯 **Merkmal:** Fortbildungsquote |
| **FA.csv** | Fachabteilungen der Krankenhäuser | `ABTID`, `FA.Key301`, `FA.Name`, `FA.FZ.Voll`, `FA.FZ.Teil`, `FA.QBID` | 🎯 **Merkmal:** Ärzte/Pflegekräfte pro Bett |
| **QS.Leistungsbereich.csv** | Leistungsbereiche je Haus mit Fallzahlen | `QSLB.Leistungsbereich`, `QSLB.Dokumentationsrate`, `QSLB.Fallzahl`, `QSLB.AnzDatensätzeStandort`, `SO.QBID` | 📊 Ergänzung (Dokumentationsqualität) |
| **Konzern.csv** | Konzernzugehörigkeit der Häuser | noch nicht gesichtet | 🎯 **Merkmal:** Träger-Info (Konzern vs. unabhängig) |

---

## ⚠️ Möglicherweise relevant (noch prüfen)

| Datei | Inhalt | Wichtige Spalten | Notiz |
|-------|--------|-----------------|-------|
| **QS.Extern.Sonstige.csv** | Externe QS-Ergebnisse (Zahlenwerte) | `Externe.QS.Leistungsbereich`, `Externe.QS.Ergebnis`, `Externe.QS.Qualitätsindikator`, `SO.QBID` | Könnte Ziel-Variable ergänzen |
| **MM.csv** | Mindestmengen-Erfüllung je Eingriff | `MM.Erbracht`, `MM.Mindestmenge`, `MM.Differenz`, `MM.LB.Kurz`, `MM.Key` | Strukturmerkmal: erfüllt Mindestmengen? |
| **FA.Personalliste.csv** | Personaldaten der Fachabteilungen | noch nicht gesichtet | Quelle für Pflegekräfte-Daten |
| **FA.Personen.csv** | Einzelpersonen in Fachabteilungen | noch nicht gesichtet | Detailebene — ggf. zu granular |
| **AMTS.csv** | Arzneimitteltherapiesicherheit | noch nicht gesichtet | Qualitätsmerkmal |
| **BF.csv** | Behandlungsfelder | `BF`, `BF.Erläuterung`, `BF.Key`, `SO.QBID` | Bedeutung von BF.Key unklar |
| **CQ.csv** | Strukturqualitätsvereinbarungen | `CQ.Key`, `SO.QBID` | Welche Zertifizierungen hat das Haus? |
| **GIQI.csv** | Geriatrische Indikatoren | noch nicht gesichtet | Unklar |
| **HB.csv / HD.csv / HM.csv** | Hygiene-Daten | noch nicht gesichtet | Möglicherweise relevant |
| **RM.csv** | Risikomanagement | noch nicht gesichtet | Strukturmerkmal |
| **QS.Pso.csv** | Personalstunden Psychiatrie | `QS.Pso.Berufsgruppen`, `QS.Pso.Stunden`, `QS.Einrichtung.ID` | Nur für Psychiatrie-Häuser |
| **QS.Struktur.Station.csv** | Stationsstruktur Psychiatrie | `QS.Station.Planbetten`, `QS.Station.Typ`, `QS.Einrichtung.ID` | Nur für Psychiatrie-Häuser |

---

## ❌ Nicht relevant für unser Projekt

| Datei | Inhalt | Warum nicht? |
|-------|--------|-------------|
| **NM.csv** | Nicht-medizinische Angebote (Parkplatz, Telefon, Ernährung) | Kein Bezug zu Qualität oder Struktur |
| **ICD.Code.csv** | ICD-Diagnoseschlüssel (Lookup-Tabelle) | Zu spezifisch / Lookup |
| **OPS.csv / OPS.Code.csv** | Operationsschlüssel | Zu spezifisch / Lookup |
| **QS.Nachweis.csv** | Nachweiszeiträume (Meta-Daten) | Nur technische Meta-Info |
| **Link.csv / LinkVersorgunggebieteSO.csv** | URL-Links | Keine Analysedaten |
| **Weiterführender_Link.csv** | Weitere Links | Keine Analysedaten |
| **QS.Einrichtungstypen.csv** | Einrichtungstypen-Lookup | Nur Lookup |
| **QS.Berufsgruppen.csv** | Berufsgruppen-Lookup | Nur Lookup |
| **Akademische_Lehre.csv** | Akademische Lehre | Eher Metadaten |
| **ErfPersVorgaben.csv** | Erforderliche Personalvorgaben | Verwaltungsdaten |
| **Pflegepersonalregelung.csv** | Pflegepersonalregelung | Verwaltungsdaten |
| **Neuartige_Therapien.csv** | Neuartige Therapien | Zu spezifisch |
| **Schutzkonzept.csv** | Schutzkonzepte | Zu spezifisch |
| **Praevention_Missbrauch_und_Gewalt.csv** | Prävention | Zu spezifisch |
| **Sicherstellungszuschlaege.csv** | Sicherstellungszuschläge | Verwaltungsdaten |

---

## 🗺️ Datenmodell — Beziehungen

```
SO.csv  ──────────────────────────────────────────── Haupttabelle
  │ SO.QBID
  ├──► QS.csv                  (QS-Berichtsbasis)
  │      │ QS.ID
  │      └──► QS.Qualitätsindikator.csv   ← ZIEL-VARIABLE
  │
  ├──► QS.Fortbildung.csv      (Fortbildungsquote)
  ├──► QS.Leistungsbereich.csv (Dokumentationsraten)
  ├──► QS.Extern.Sonstige.csv  (Externe QS-Ergebnisse)
  ├──► FA.csv                  (Fachabteilungen → Ärzte)
  │      └──► FA.Personalliste.csv
  ├──► MM.csv                  (Mindestmengen)
  ├──► BF.csv                  (Behandlungsfelder)
  └──► CQ.csv                  (Strukturqualitätsvereinbarungen)
```

---

## 📌 Wichtige Erkenntnisse

1. **`SO.QBID` ist der universelle Schlüssel** — alle Tabellen über diese ID verknüpfbar.
2. **`QS.Qualitätsindikator.csv` ist >50 MB** — muss mit `pd.read_csv()` in Python geladen werden, nicht direkt in VS Code lesbar.
3. **Fortbildungsquote berechnen:** `QS.Fortbildungsnachweis_Erbracht_Habende / QS.Fortbildungspflichtige`
4. **Ärzte pro Bett berechnen:** `FA.csv` aggregieren (`FA.FZ.Voll` summieren pro `FA.QBID`) ÷ `SO.Betten` aus `SO.csv`
5. **Träger-Kategorien** in `SO.csv` Spalte `KH.Träger.Art`: `privat` | `freigemeinnützig` | `öffentlich`

---

*Zuletzt aktualisiert: 2026-07-27*
