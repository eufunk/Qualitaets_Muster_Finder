"""
streamlit_dashboard.py
=======================
Streamlit Dashboard — Qualitaets-Muster-Finder

Start:  streamlit run Dashboard/streamlit_dashboard.py

Seiten:
  1. Uebersicht      — KPIs, Deutschland-Karte, Verteilung
  2. Vergleiche      — Traeger, Bundesland, Ärzte/Bett
  3. Aehnliche KH    — Filtersuche + Steckbrief
  4. Risiko-Rechner  — Decision Tree Vorhersage (Bonus)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard_utils import (
    lade_daten, validiere_daten, berechne_kpis,
    erstelle_karte, erstelle_quote_histogramm, erstelle_bundesland_balken,
    erstelle_traeger_vergleich, erstelle_boxplot_aerzte,
    erstelle_streudiagramm, erstelle_pivot_traeger_uni,
    finde_aehnliche, haus_steckbrief,
    lade_modell, berechne_risiko,
    get_traeger_optionen, get_bundesland_optionen,
    FARBE_VIELE, FARBE_WENIGE, MEDIAN_QUOTE, DT_SPLIT, TRAEGER_COL,
)

# ── Seitenkonfiguration ───────────────────────────────────────────
st.set_page_config(
    page_title="Qualitaets-Muster-Finder",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Daten laden (gecacht) ─────────────────────────────────────────
@st.cache_data
def get_daten():
    return lade_daten()

@st.cache_resource
def get_modell():
    return lade_modell()

df     = get_daten()
modell = get_modell()

# ── Sidebar Navigation ────────────────────────────────────────────
st.sidebar.title("🏥 Qualitäts-Muster-Finder")
st.sidebar.markdown("---")
seite = st.sidebar.radio(
    "Navigation",
    ["📊 Übersicht", "🔍 Vergleiche", "🏨 Ähnliche Häuser", "⚠️ Risiko-Rechner"],
)
st.sidebar.markdown("---")

# Globale Filter (wirken auf alle Seiten)
st.sidebar.subheader("🔧 Globale Filter")
filter_bundesland = st.sidebar.selectbox(
    "Bundesland", get_bundesland_optionen(df), index=0
)
filter_traeger = st.sidebar.selectbox(
    "Trägerschaft", get_traeger_optionen(df), index=0
)
filter_uni = st.sidebar.selectbox(
    "Klinik-Typ", ["Alle", "Normale Klinik", "Uni-Klinik"], index=0
)

# Filter anwenden
df_gefiltert = df.copy()
if filter_bundesland != "Alle":
    df_gefiltert = df_gefiltert[df_gefiltert["SO.Bundesland"] == filter_bundesland]
if filter_traeger != "Alle":
    df_gefiltert = df_gefiltert[df_gefiltert[TRAEGER_COL] == filter_traeger]
if filter_uni != "Alle":
    df_gefiltert = df_gefiltert[df_gefiltert["Uni_Label"] == filter_uni]

st.sidebar.caption(f"Haeuser im Filter: **{len(df_gefiltert):,}** von {len(df):,}")
st.sidebar.markdown("---")
st.sidebar.caption("Datenbasis: Qualitaetsberichte 2023 | IQTIG")

# ═════════════════════════════════════════════════════════════════
# SEITE 1 — UEBERSICHT
# ═════════════════════════════════════════════════════════════════
if seite == "📊 Übersicht":
    st.title("📊 Übersicht — Qualitätsprobleme deutscher Krankenhäuser")
    st.markdown(
        "**Projektfrage:** Welche Krankenhausmerkmale hängen damit zusammen, "
        "dass ein Haus überdurchschnittlich viele Qualitätsprobleme aufweist?"
    )

    kpis = berechne_kpis(df_gefiltert)

    # KPI-Karten
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🏥 Krankenhäuser", f"{kpis['n_haeuser']:,}")
    k2.metric(
        "⚠️ Anteil 'Viele Probleme'",
        f"{kpis['pct_viele']:.1%}",
        delta=f"{kpis['pct_viele'] - 0.5:+.1%} vs. 50%",
        delta_color="inverse",
    )
    k3.metric("📈 Ø auffällig-Quote", f"{kpis['avg_quote']:.1%}")
    k4.metric("👨‍⚕️ Ø Ärzte pro Bett", f"{kpis['avg_aerzte']:.3f}")

    st.markdown("---")

    # Karte + Histogramm
    col_karte, col_hist = st.columns([2, 1])
    with col_karte:
        st.subheader("🗺️ Regionale Verteilung")
        st.plotly_chart(erstelle_karte(df_gefiltert), use_container_width=True)

    with col_hist:
        st.subheader("📊 Verteilung der auffällig-Quote")
        st.plotly_chart(erstelle_quote_histogramm(df_gefiltert), use_container_width=True)
        st.caption(
            f"Median: **{kpis['median_quote']:.1%}** — "
            "Häuser über dem Median gelten als 'viele Probleme'."
        )

    st.markdown("---")
    st.subheader("📍 Vergleich nach Bundesland")
    st.plotly_chart(erstelle_bundesland_balken(df_gefiltert), use_container_width=True)


# ═════════════════════════════════════════════════════════════════
# SEITE 2 — VERGLEICHE
# ═════════════════════════════════════════════════════════════════
elif seite == "🔍 Vergleiche":
    st.title("🔍 Vergleiche — Welche Merkmale machen den Unterschied?")
    st.info(
        "**Wichtig:** Ein Zusammenhang in den Grafiken bedeutet **nicht** automatisch Kausalität. "
        "Kein Zusammenhang ist ebenfalls ein valides Ergebnis."
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "Trägerschaft", "Ärzte pro Bett", "Streudiagramm", "Pivot-Tabelle"
    ])

    with tab1:
        st.subheader("Trägerschaft vs. Anteil 'Viele Probleme'")
        st.plotly_chart(erstelle_traeger_vergleich(df_gefiltert), use_container_width=True)
        st.markdown(
            "**Befund:** Private Häuser haben mit **56,5 %** den höchsten Anteil "
            "(freigemeinnützig: 46,4 % | öffentlich: 46,7 %). "
            "ANOVA p<0,001 statistisch signifikant. "
            "⚠️ Störfaktor: Private Häuser sind im Median kleiner (125 Betten)."
        )

    with tab2:
        st.subheader("Ärzte pro Bett: MIT vs. OHNE viele Probleme")
        st.plotly_chart(erstelle_boxplot_aerzte(df_gefiltert), use_container_width=True)
        col_a, col_b = st.columns(2)
        col_a.metric("Wenige Probleme: Ø Ärzte/Bett",
                     f"{df_gefiltert[df_gefiltert['hat_viele_Probleme']==0]['aerzte_pro_bett'].median():.3f}")
        col_b.metric("Viele Probleme: Ø Ärzte/Bett",
                     f"{df_gefiltert[df_gefiltert['hat_viele_Probleme']==1]['aerzte_pro_bett'].median():.3f}")
        st.markdown(
            f"**Befund:** T-Test t=6,002, **p<0,001 signifikant**. "
            f"Trennwert aus Decision Tree: **{DT_SPLIT} Ärzte/Bett** (gestrichelte Linie)."
        )

    with tab3:
        st.subheader("Streudiagramm")
        merkmal = st.selectbox(
            "Merkmal für X-Achse",
            ["aerzte_pro_bett", "SO.Betten", "fortbildungsquote", "total_qi"],
        )
        st.plotly_chart(erstelle_streudiagramm(df_gefiltert, merkmal), use_container_width=True)
        st.caption(f"Regressionslinie zeigt den linearen Trend (r² aus Plotly OLS).")

    with tab4:
        st.subheader("Pivot-Tabelle: Ø auffällig-Quote nach Träger × Uni-Status")
        pivot = erstelle_pivot_traeger_uni(df_gefiltert)
        st.dataframe(
            pivot.style.format("{:.3f}").background_gradient(cmap="RdYlGn_r"),
            use_container_width=True,
        )
        st.caption("Uni-Kliniken haben je nach Träger leicht niedrigere Auffälligkeitsquoten.")


# ═════════════════════════════════════════════════════════════════
# SEITE 3 — AEHNLICHE KRANKENHAEUSER
# ═════════════════════════════════════════════════════════════════
elif seite == "🏨 Ähnliche Häuser":
    st.title("🏨 Ähnliche Krankenhäuser finden")

    col_filter, col_ergebnis = st.columns([1, 2])

    with col_filter:
        st.subheader("🔧 Filter")
        eingabe_betten = st.number_input(
            "Bettenzahl (±50% Toleranz)", min_value=0, max_value=2000, value=300, step=50
        )
        eingabe_bundesland = st.selectbox(
            "Bundesland", get_bundesland_optionen(df), index=0
        )
        eingabe_traeger = st.selectbox(
            "Trägerschaft", get_traeger_optionen(df), index=0
        )
        n_ergebnisse = st.slider("Max. Ergebnisse", 5, 30, 10)

        suchen = st.button("🔍 Suchen", use_container_width=True)

    with col_ergebnis:
        if suchen:
            aehnliche = finde_aehnliche(
                df, eingabe_betten, eingabe_bundesland, eingabe_traeger, n_ergebnisse
            )
            if aehnliche.empty:
                st.warning("Keine Häuser mit diesen Kriterien gefunden. Filter lockern.")
            else:
                st.subheader(f"🏥 {len(aehnliche)} ähnliche Häuser gefunden")
                st.dataframe(
                    aehnliche.style
                    .format({"auffaellig_quote": "{:.1%}", "aerzte_pro_bett": "{:.3f}",
                             "fortbildungsquote": "{:.1%}"})
                    .applymap(
                        lambda v: f"background-color: {FARBE_VIELE}22" if v == "Viele Probleme"
                        else f"background-color: {FARBE_WENIGE}22",
                        subset=["Problemkategorie"]
                    ),
                    use_container_width=True,
                )

                # Vergleichsbalken
                avg_quote  = aehnliche["auffaellig_quote"].mean()
                avg_aerzte = aehnliche["aerzte_pro_bett"].mean()
                col_c1, col_c2 = st.columns(2)
                col_c1.metric(
                    "Ø auffällig-Quote (Gruppe)",
                    f"{avg_quote:.1%}",
                    delta=f"{avg_quote - MEDIAN_QUOTE:+.1%} vs. Median",
                    delta_color="inverse",
                )
                col_c2.metric("Ø Ärzte/Bett (Gruppe)", f"{avg_aerzte:.3f}")
        else:
            st.info("Filter setzen und 'Suchen' klicken.")

    st.markdown("---")

    # Einzelhaus-Steckbrief
    st.subheader("📋 Einzelhaus-Steckbrief")
    haus_auswahl = st.selectbox(
        "Krankenhaus wählen",
        options=df["SO.QBID"].tolist(),
        format_func=lambda x: df[df["SO.QBID"] == x]["SO.Name"].values[0],
    )
    if haus_auswahl:
        sb = haus_steckbrief(df, haus_auswahl)
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Betten",        sb["betten"])
        s2.metric("Träger",        sb["traeger"])
        s3.metric("Bundesland",    sb["bundesland"])
        s4.metric("Uni-Klinik",    sb["uni"])
        s5, s6, s7, s8 = st.columns(4)
        s5.metric("auffällig-Quote", f"{sb['auffaellig_quote']:.1%}",
                  delta=f"{sb['delta_median']:+.1%} vs. Median", delta_color="inverse")
        s6.metric("Kategorie",      sb["hat_viele"] and "⚠️ Viele Probleme" or "✅ Wenige Probleme")
        s7.metric("Ärzte/Bett",     f"{sb['aerzte_pro_bett']:.3f}" if pd.notna(sb["aerzte_pro_bett"]) else "k.A.")
        s8.metric("Fortbildungsquote", f"{sb['fortbildungsquote']:.1%}" if pd.notna(sb["fortbildungsquote"]) else "k.A.")


# ═════════════════════════════════════════════════════════════════
# SEITE 4 — RISIKO-RECHNER
# ═════════════════════════════════════════════════════════════════
elif seite == "⚠️ Risiko-Rechner":
    st.title("⚠️ Risiko-Rechner — Decision Tree Vorhersage")
    st.warning(
        f"**Modell-Genauigkeit: 64,9 %** (Basislinie: 50,7 %) | "
        f"R² = 0,023 — Strukturmerkmale erklären nur **2,3 % der Varianz**. "
        "Vorhersagen sind Hinweise, keine Diagnosen!"
    )

    if modell is None:
        st.error("Modell-Datei 'modell_krankenhaus.pkl' nicht gefunden. Bitte 03_Decision_Tree.ipynb ausführen.")
        st.stop()

    st.subheader("📝 Merkmale eingeben")
    r1, r2 = st.columns(2)

    with r1:
        ein_betten      = st.number_input("Bettenzahl", 0, 2000, 300, 50)
        ein_uni         = st.selectbox("Uni-Klinik?", ["Nein", "Ja"])
        ein_fortb       = st.slider("Fortbildungsquote", 0.0, 1.0, 0.7, 0.05,
                                    format="%.0f%%")

    with r2:
        ein_aerzte      = st.number_input("Ärzte pro Bett", 0.0, 5.0, 0.45, 0.05,
                                          format="%.3f")
        ein_traeger_opt = st.selectbox("Trägerschaft",
                                       ["freigemeinnützig", "öffentlich", "privat"])
        traeger_enc_map = {"freigemeinnützig": 0, "öffentlich": 1, "privat": 2}

    st.markdown("---")

    if st.button("🔮 Risiko berechnen", use_container_width=True, type="primary"):
        ergebnis = berechne_risiko(
            modell,
            betten      = ein_betten,
            uni         = 1 if ein_uni == "Ja" else 0,
            fortbildung = ein_fortb,
            aerzte      = ein_aerzte,
            traeger_enc = traeger_enc_map[ein_traeger_opt],
        )

        # Ergebnis anzeigen
        farbe = FARBE_VIELE if ergebnis["vorhersage"] == 1 else FARBE_WENIGE
        st.markdown(
            f"<div style='background:{farbe}22;border-left:5px solid {farbe};"
            f"padding:15px;border-radius:5px;'>"
            f"<h3 style='color:{farbe}'>Vorhersage: {ergebnis['risiko_text']}</h3>"
            f"<p>{ergebnis['erklaerung']}</p>"
            f"<p>Unsicherheit: <b>{ergebnis['unsicherheit']}</b></p>"
            f"</div>",
            unsafe_allow_html=True,
        )

        st.markdown("")
        p1, p2 = st.columns(2)
        p1.metric("P(Wenige Probleme)", f"{ergebnis['prob_wenige']:.1%}")
        p2.metric("P(Viele Probleme)",  f"{ergebnis['prob_viele']:.1%}")

        # Wichtigster Faktor visuell
        st.markdown("---")
        st.subheader("🔑 Entscheidungsgrundlage")
        st.markdown(
            f"Der Decision Tree entscheidet primär anhand von **Ärzte pro Bett** "
            f"(71,3 % Feature Importance):\n\n"
            f"- Ärzte/Bett **≤ {DT_SPLIT}** → Risiko **hoch**\n"
            f"- Ärzte/Bett **> {DT_SPLIT}** → Risiko **gering**\n\n"
            f"Ihr eingegebener Wert: **{ein_aerzte:.3f}** "
            f"({'≤' if ein_aerzte <= DT_SPLIT else '>'} {DT_SPLIT})"
        )

    st.markdown("---")
    st.subheader("📊 Feature Importance")
    import plotly.graph_objects as go
    fig_fi = go.Figure(go.Bar(
        x=[0.7133, 0.2867, 0, 0, 0],
        y=["aerzte_pro_bett", "SO.Betten", "fortbildungsquote", "traeger_enc", "SO.Uni"],
        orientation="h",
        marker_color=["#2E74B5", "#7DC3E8", "#D9D9D9", "#D9D9D9", "#D9D9D9"],
    ))
    fig_fi.update_layout(
        title="Feature Importance des Decision Tree",
        xaxis_title="Wichtigkeit", height=300,
        xaxis=dict(tickformat=".0%"),
    )
    st.plotly_chart(fig_fi, use_container_width=True)
    st.caption("Werte aus 03_Decision_Tree.ipynb. aerzte_pro_bett dominiert mit 71,3 %.")
