"""
dashboard_utils.py
==================
Hilfsfunktionen fuer das Streamlit Dashboard — Qualitaets-Muster-Finder

Trennprinzip:
    - Datenlogik, Berechnungen und Plot-Erstellung: HIER
    - UI-Layout und Widgets:                        in streamlit_dashboard.py

Aufruf-Beispiel:
    from dashboard_utils import lade_daten, berechne_kpis, erstelle_karte
"""

import sys
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
from pathlib import Path

# ── Projekt-Root (eine Ebene über /Dashboard) ─────────────────────
PROJEKT_ROOT = Path(__file__).resolve().parent.parent

# modell_klasse.py liegt in model/, nicht neben dieser Datei
sys.path.insert(0, str(PROJEKT_ROOT / "model"))
from modell_klasse import KrankenhausModell  # noqa: E402, F401 – wird fuer joblib benoetigt

# ── Konstanten ────────────────────────────────────────────────────
DATA_PATH    = PROJEKT_ROOT / "Data" / "analysetabelle.csv"
MODEL_PATH   = PROJEKT_ROOT / "Data" / "modell_krankenhaus.pkl"

FARBE_VIELE  = "#e74c3c"   # rot   = viele Probleme
FARBE_WENIGE = "#2ecc71"   # gruen = wenige Probleme
FARBE_MAP    = {0: FARBE_WENIGE, 1: FARBE_VIELE}
LABEL_MAP    = {0: "Wenige Probleme", 1: "Viele Probleme"}

MEDIAN_QUOTE = 0.0588      # aus Python-Analyse berechnet (Korrektur 2026-08-14) — nicht veraendern!
DT_SPLIT     = 0.271       # Decision Tree Split-Wert fuer aerzte_pro_bett
TRAEGER_COL  = "KH.Träger.Art"

# ═════════════════════════════════════════════════════════════════
# 1. DATEN LADEN & VALIDIEREN
# ═════════════════════════════════════════════════════════════════

def lade_daten(pfad: Path = DATA_PATH) -> pd.DataFrame:
    """
    Laedt analysetabelle.csv und bereitet sie fuer das Dashboard vor.

    Transformationen:
      - Latitude/Longitude: Komma -> Punkt (falls noetig)
      - Neue Hilfsspalten: Problemkategorie, Uni_Label, Groessenklasse

    Returns:
        pd.DataFrame mit 1.821 Zeilen und erweiterten Spalten
    """
    df = pd.read_csv(pfad, low_memory=False)

    # Koordinaten reparieren — bedingungslos, da dtype-Check auf manchen Servern fehlschlägt
    for col in ["SO.Latitude", "SO.Longitude"]:
        df[col] = (
            df[col].astype(str)
            .str.replace(",", ".", regex=False)
            .pipe(pd.to_numeric, errors="coerce")
        )

    # Hilfsspalten fuer Dashboard-Anzeige
    df["Problemkategorie"] = df["hat_viele_Probleme"].map(LABEL_MAP)
    df["Uni_Label"]        = df["SO.Uni"].map({0: "Normale Klinik", 1: "Uni-Klinik"})
    df["Groessenklasse"]   = df["SO.Betten"].apply(_groesse_kategorie)
    df["Aerzte_Kategorie"] = df["aerzte_pro_bett"].apply(_aerzte_risikoklasse)

    # Traeger-Fehlwerte auffuellen
    df[TRAEGER_COL] = df[TRAEGER_COL].fillna("Unbekannt")

    return df


def _groesse_kategorie(betten: float) -> str:
    if betten == 0:
        return "Tagesklinik"
    elif betten <= 100:
        return "Klein (≤ 100)"
    elif betten <= 400:
        return "Mittel (101–400)"
    else:
        return "Groß (> 400)"


def _aerzte_risikoklasse(aerzte: float) -> str:
    if pd.isna(aerzte):
        return "Unbekannt"
    return "Risiko hoch" if aerzte > DT_SPLIT else "Risiko gering"


def validiere_daten(df: pd.DataFrame) -> dict:
    """
    Prueft die Datenqualitaet und gibt eine Zusammenfassung zurueck.

    Returns:
        dict mit Warnungen und Statistiken
    """
    return {
        "n_haeuser":       len(df),
        "n_fehlend_aerzte": df["aerzte_pro_bett"].isna().sum(),
        "n_fehlend_fortb":  df["fortbildungsquote"].isna().sum(),
        "n_fehlend_traeger": (df[TRAEGER_COL] == "Unbekannt").sum(),
        "koordinaten_ok":   df["SO.Latitude"].notna().sum(),
    }


# ═════════════════════════════════════════════════════════════════
# 2. KPIs (fuer alle Seiten)
# ═════════════════════════════════════════════════════════════════

def berechne_kpis(df: pd.DataFrame) -> dict:
    """
    Berechnet die Kern-Kennzahlen fuer die KPI-Karten.

    Returns:
        dict mit Kennzahlen
    """
    n        = len(df)
    n_viele  = df["hat_viele_Probleme"].sum()
    return {
        "n_haeuser":          n,
        "pct_viele":          n_viele / n,
        "avg_quote":          df["auffaellig_quote"].mean(),
        "median_quote":       df["auffaellig_quote"].median(),
        "gesamt_quote":       df["auffaellig_n"].sum() / df["total_qi"].sum(),
        "avg_aerzte":         df["aerzte_pro_bett"].mean(),
        "avg_fortbildung":    df["fortbildungsquote"].mean(),
        "n_uni":              df["SO.Uni"].sum(),
        "n_privat":           (df[TRAEGER_COL] == "privat").sum(),
    }


# ═════════════════════════════════════════════════════════════════
# 3. SEITE 1 — UEBERSICHT
# ═════════════════════════════════════════════════════════════════

def erstelle_karte(df: pd.DataFrame) -> go.Figure:
    """
    Erstellt die Deutschland-Karte mit Krankenhaus-Standorten.
    Farbe = Problemkategorie, Groesse = Bettenzahl.
    """
    df_karte = df.dropna(subset=["SO.Latitude", "SO.Longitude"]).copy()

    fig = px.scatter_mapbox(
        df_karte,
        lat="SO.Latitude",
        lon="SO.Longitude",
        color="Problemkategorie",
        color_discrete_map={
            "Wenige Probleme": FARBE_WENIGE,
            "Viele Probleme":  FARBE_VIELE,
        },
        hover_name="SO.Name",
        hover_data={
            "SO.Betten":        True,
            "SO.Bundesland":    True,
            TRAEGER_COL:        True,
            "auffaellig_quote": ":.1%",
            "SO.Latitude":      False,
            "SO.Longitude":     False,
            "Problemkategorie": False,
        },
        zoom=5,
        center={"lat": 51.2, "lon": 10.4},
        mapbox_style="open-street-map",
    )
    fig.update_traces(marker={"size": 8, "opacity": 0.7})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=620)
    return fig


def erstelle_quote_histogramm(df: pd.DataFrame) -> go.Figure:
    """Histogramm der auffaellig-Quote — Bins explizit berechnet, Linie passt exakt."""
    # Bins einmal berechnen, dann für Balken UND Linie nutzen (wie im Notebook)
    data_all   = df["auffaellig_quote"].dropna().values
    data_wenig = df[df["hat_viele_Probleme"] == 0]["auffaellig_quote"].dropna().values
    data_viel  = df[df["hat_viele_Probleme"] == 1]["auffaellig_quote"].dropna().values

    counts_all,   bin_edges = np.histogram(data_all,   bins=30)
    counts_wenig, _         = np.histogram(data_wenig, bins=bin_edges)
    counts_viel,  _         = np.histogram(data_viel,  bins=bin_edges)

    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_width   = (bin_edges[1] - bin_edges[0]) * 0.92  # 8% Lücke

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=bin_centers, y=counts_wenig, name="Wenige Probleme",
        marker_color=FARBE_WENIGE, width=bin_width,
    ))
    fig.add_trace(go.Bar(
        x=bin_centers, y=counts_viel, name="Viele Probleme",
        marker_color=FARBE_VIELE, width=bin_width,
    ))
    # Linie auf exakter Balkenhöhe (passt garantiert, gleiche Bins)
    fig.add_trace(go.Scatter(
        x=bin_centers, y=counts_all,
        mode="lines+markers",
        line=dict(color="#2c3e50", width=1.5),
        marker=dict(size=3),
        name="Verlauf",
        showlegend=False,
    ))
    fig.add_vline(
        x=MEDIAN_QUOTE, line_dash="dash", line_color="#888888",
        annotation_text=f"Median {MEDIAN_QUOTE:.0%}",
        annotation_position="top right",
    )
    fig.update_layout(
        barmode="stack",
        xaxis=dict(tickformat=".0%", title="Anteil auffälliger QI"),
        yaxis=dict(title="Anzahl Krankenhäuser"),
        title="Verteilung der auffällig-Quote",
        legend=dict(orientation="h", y=1.1),
    )
    return fig


def erstelle_bundesland_balken(df: pd.DataFrame) -> go.Figure:
    """Horizontalbalken: Anteil 'Viele Probleme' je Bundesland."""
    stats = (
        df.groupby("SO.Bundesland")
        .agg(pct=("hat_viele_Probleme", "mean"), n=("hat_viele_Probleme", "count"))
        .reset_index()
        .sort_values("pct")
    )
    farben = [FARBE_VIELE if p > 0.5 else FARBE_WENIGE for p in stats["pct"]]

    fig = px.bar(
        stats, x="pct", y="SO.Bundesland", orientation="h",
        text=stats["n"].apply(lambda x: f"n={x} Häuser"),
        custom_data=["n"],
        labels={"pct": "Anteil 'Viele Probleme'", "SO.Bundesland": ""},
        title="Anteil Haeuser mit vielen Problemen je Bundesland",
    )
    fig.update_traces(
        marker_color=farben, textposition="outside",
        hovertemplate="<b>%{y}</b><br>Anteil 'Viele Probleme': %{x:.1%}<br>Anzahl Häuser (n): %{customdata[0]}<extra></extra>",
    )
    fig.add_vline(x=0.5, line_dash="dash", line_color="gray")
    fig.update_xaxes(tickformat=".0%")
    return fig


# ═════════════════════════════════════════════════════════════════
# 4. SEITE 2 — VERGLEICHE
# ═════════════════════════════════════════════════════════════════

def erstelle_traeger_vergleich(df: pd.DataFrame) -> go.Figure:
    """Balkendiagramm: Anteil 'Viele Probleme' nach Traegerschaft."""
    stats = (
        df.groupby(TRAEGER_COL)
        .agg(pct=("hat_viele_Probleme", "mean"), n=("hat_viele_Probleme", "count"))
        .reset_index()
        .sort_values("pct", ascending=False)
    )
    fig = px.bar(
        stats, x=TRAEGER_COL, y="pct",
        text=stats.apply(lambda r: f"{r['pct']:.1%} (n={r['n']})", axis=1),
        color="pct",
        color_continuous_scale=["#2ecc71", "#e74c3c"],
        labels={"pct": "Anteil 'Viele Probleme'", TRAEGER_COL: "Traegerschaft"},
        title="Traeger-Vergleich (ANOVA p=0,969 NICHT signifikant)",
    )
    fig.add_hline(y=0.5, line_dash="dash", line_color="gray",
                  annotation_text="50%-Linie")
    fig.update_traces(textposition="outside")
    fig.update_yaxes(tickformat=".0%", range=[0, 0.7])
    fig.update_coloraxes(showscale=False)
    return fig


def erstelle_boxplot_aerzte(df: pd.DataFrame) -> go.Figure:
    """Box-Plot: aerzte_pro_bett nach Problemkategorie (T-Test p<0,0001)."""
    fig = px.box(
        df.dropna(subset=["aerzte_pro_bett"]),
        x="Problemkategorie", y="aerzte_pro_bett",
        color="Problemkategorie",
        color_discrete_map={
            "Wenige Probleme": FARBE_WENIGE,
            "Viele Probleme":  FARBE_VIELE,
        },
        points=False,
        labels={"aerzte_pro_bett": "Aerzte pro Bett"},
        title="Aerzte pro Bett: MIT vs. OHNE viele Probleme (T-Test p<0,0001)",
    )
    fig.add_hline(y=DT_SPLIT, line_dash="dot", line_color="black",
                  annotation_text=f"Decision Tree Grenzwert: {DT_SPLIT}")
    return fig


def erstelle_streudiagramm(df: pd.DataFrame, merkmal_x: str = "aerzte_pro_bett") -> go.Figure:
    """Streudiagramm: Merkmal vs. auffaellig_quote, eingefaerbt nach Problemkategorie."""
    df_plot = df.dropna(subset=[merkmal_x, "auffaellig_quote"])
    fig = px.scatter(
        df_plot,
        x=merkmal_x, y="auffaellig_quote",
        color="Problemkategorie",
        color_discrete_map={
            "Wenige Probleme": FARBE_WENIGE,
            "Viele Probleme":  FARBE_VIELE,
        },
        opacity=0.5,
        hover_name="SO.Name",
        trendline="ols",
        labels={"auffaellig_quote": "Auffaellig-Quote", merkmal_x: merkmal_x},
        title=f"Zusammenhang: {merkmal_x} vs. Auffaellig-Quote",
    )
    fig.update_yaxes(tickformat=".0%")
    return fig


def erstelle_pivot_traeger_uni(df: pd.DataFrame) -> pd.DataFrame:
    """
    pivot_table: Ø auffaellig_quote nach Traeger x Uni-Status.
    """
    pivot = df.pivot_table(
        values="auffaellig_quote",
        index=TRAEGER_COL,
        columns="Uni_Label",
        aggfunc="mean",
    ).round(3)
    pivot["Gesamt"] = df.groupby(TRAEGER_COL)["auffaellig_quote"].mean().round(3)
    return pivot


# ═════════════════════════════════════════════════════════════════
# 5. SEITE 3 — AEHNLICHE KRANKENHAEUSER
# ═════════════════════════════════════════════════════════════════

def finde_aehnliche(
    df: pd.DataFrame,
    betten: int,
    bundesland: str,
    traeger: str,
    n: int = 10,
    toleranz_pct: float = 0.3,
) -> pd.DataFrame:
    """
    Findet aehnliche Krankenhaeuser anhand von Filtern.

    Args:
        betten:     Ziel-Bettenzahl (±50% Toleranz)
        bundesland: Bundesland-Filter ("Alle" = kein Filter)
        traeger:    Traeger-Filter ("Alle" = kein Filter)
        n:          Max. Anzahl Ergebnis-Haeuser

    Returns:
        DataFrame mit aehnlichen Haeusern, sortiert nach auffaellig_quote
    """
    mask = pd.Series([True] * len(df), index=df.index)

    # Bettenzahl: konfigurierbare Toleranz
    if betten > 0:
        toleranz = max(betten * toleranz_pct, 30)
        mask &= df["SO.Betten"].between(betten - toleranz, betten + toleranz)

    if bundesland != "Alle":
        mask &= df["SO.Bundesland"] == bundesland

    if traeger != "Alle":
        mask &= df[TRAEGER_COL] == traeger

    ergebnis = df[mask].copy()

    # Ausgabe-Spalten
    cols = [
        "SO.Name", "SO.Betten", "SO.Bundesland", TRAEGER_COL,
        "Uni_Label", "auffaellig_quote", "Problemkategorie",
        "aerzte_pro_bett", "fortbildungsquote",
    ]
    return ergebnis[cols].sort_values("auffaellig_quote").head(n)


def haus_steckbrief(df: pd.DataFrame, so_qbid: int) -> dict:
    """
    Gibt alle Merkmale eines einzelnen Krankenhauses zurueck.

    Returns:
        dict mit Merkmal -> Wert, inkl. Vergleich zum Durchschnitt
    """
    haus = df[df["SO.QBID"] == so_qbid].iloc[0]
    return {
        "name":              haus["SO.Name"],
        "betten":            haus["SO.Betten"],
        "bundesland":        haus["SO.Bundesland"],
        "traeger":           haus[TRAEGER_COL],
        "uni":               haus["Uni_Label"],
        "auffaellig_quote":  haus["auffaellig_quote"],
        "delta_median":      haus["auffaellig_quote"] - MEDIAN_QUOTE,
        "hat_viele":         haus["hat_viele_Probleme"],
        "aerzte_pro_bett":   haus["aerzte_pro_bett"],
        "fortbildungsquote": haus["fortbildungsquote"],
        "aerzte_kategorie":  haus["Aerzte_Kategorie"],
        # Vergleich mit Gesamt-Durchschnitt
        "avg_quote_gesamt":  df["auffaellig_quote"].mean(),
        "avg_aerzte_gesamt": df["aerzte_pro_bett"].mean(),
    }


# ═════════════════════════════════════════════════════════════════
# 6. SEITE 4 — RISIKO-RECHNER (DECISION TREE)
# ═════════════════════════════════════════════════════════════════

def lade_modell(pfad: Path = MODEL_PATH):
    """
    Laedt das trainierte KrankenhausModell aus modell_krankenhaus.pkl.

    Returns:
        KrankenhausModell-Instanz oder None bei Fehler
    """
    try:
        return joblib.load(pfad)
    except FileNotFoundError:
        return None


def berechne_risiko(
    modell,
    betten: int,
    uni: int,
    fortbildung: float,
    aerzte: float,
    traeger_enc: int,
    pflege: float = 1.0,
    konzern: int = 0,
) -> dict:
    """
    Berechnet die Risiko-Vorhersage fuer ein Krankenhaus.

    Args:
        modell:       Geladenes KrankenhausModell
        betten:       Bettenzahl
        uni:          0=Normal, 1=Uni-Klinik
        fortbildung:  Fortbildungsquote (0.0 - 1.0)
        aerzte:       Aerzte pro Bett
        traeger_enc:  Encoded Traeger (0=freigemeinnuetzig, 1=oeffentlich, 2=privat)
        pflege:       Pflegekraefte pro Bett
        konzern:      0=unabhaengig, 1=Konzernhaus

    Returns:
        dict mit Vorhersage, Wahrscheinlichkeiten und Erklaerung
    """
    import pandas as pd

    eingabe = pd.DataFrame([{
        "SO.Betten":        betten,
        "SO.Uni":           uni,
        "fortbildungsquote": fortbildung,
        "aerzte_pro_bett":  aerzte,
        "pflege_pro_bett":  pflege,
        "ist_konzern":      konzern,
        "traeger_enc":      traeger_enc,
    }])

    vorhersage = modell.model.predict(eingabe)[0]
    proba      = modell.model.predict_proba(eingabe)[0]

    # Einfaerben nach Risiko
    risiko_text = "Viele Probleme" if vorhersage == 1 else "Wenige Probleme"
    risiko_farbe = FARBE_VIELE if vorhersage == 1 else FARBE_WENIGE

    # Decision Tree Erklaerung (wichtigster Split) — Korrektur 2026-08-14:
    # mehr Aerzte pro Bett haengt jetzt mit MEHR, nicht weniger, Qualitaetsproblemen zusammen
    _seite  = "darüber" if aerzte > DT_SPLIT else "darunter"
    _folge  = "viele Qualitätsprobleme wahrscheinlicher" if aerzte > DT_SPLIT else "wenige Qualitätsprobleme wahrscheinlicher (hängt zusätzlich von Pflegepersonal/Bettenzahl ab)"
    erklaerung = (
        f"Ausschlaggebend: Ärzte pro Bett = {aerzte:.3f} "
        f"(Schwellenwert {DT_SPLIT} — eingegebener Wert liegt {_seite} → {_folge})"
    )

    return {
        "vorhersage":    vorhersage,
        "risiko_text":   risiko_text,
        "risiko_farbe":  risiko_farbe,
        "prob_wenige":   proba[0],
        "prob_viele":    proba[1],
        "erklaerung":    erklaerung,
        "unsicherheit":  "hoch" if max(proba) < 0.7 else "mittel" if max(proba) < 0.85 else "gering",
    }


def get_traeger_optionen(df: pd.DataFrame) -> list:
    """Gibt sortierte Liste der Traeger-Optionen zurueck (fuer Dropdown)."""
    return ["Alle"] + sorted(df[TRAEGER_COL].unique().tolist())


def get_bundesland_optionen(df: pd.DataFrame) -> list:
    """Gibt sortierte Liste der Bundeslaender zurueck (fuer Dropdown)."""
    return ["Alle"] + sorted(df["SO.Bundesland"].unique().tolist())


# ═════════════════════════════════════════════════════════════════
# 7. TEST (direkt ausfuehren zum Pruefen)
# ═════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Lade Daten...")
    df = lade_daten()
    print(f"  Geladen: {df.shape}")

    info = validiere_daten(df)
    print(f"  Validierung: {info}")

    kpis = berechne_kpis(df)
    print(f"\nKPIs:")
    for k, v in kpis.items():
        print(f"  {k:25s}: {v:.3f}" if isinstance(v, float) else f"  {k:25s}: {v}")

    aehnliche = finde_aehnliche(df, betten=300, bundesland="Bayern", traeger="Alle", n=5)
    print(f"\nAehnliche Haeuser (Bayern, ~300 Betten):\n{aehnliche[['SO.Name','SO.Betten','auffaellig_quote']].to_string()}")

    modell = lade_modell()
    if modell:
        risiko = berechne_risiko(modell, betten=200, uni=0, fortbildung=0.7, aerzte=0.25,
                                  traeger_enc=1, pflege=1.0, konzern=0)
        print(f"\nRisiko-Vorhersage: {risiko['risiko_text']} (P={risiko['prob_viele']:.1%})")
        print(f"  {risiko['erklaerung']}")
    else:
        print("\nKein Modell gefunden (modell_krankenhaus.pkl fehlt)")
