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
    page_icon=":triangular_ruler:",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Deploy-Button und Hamburger-Menü ausblenden, Top-Padding reduzieren
st.markdown(
    "<style>"
    ".block-container{padding-top:1rem !important;}"
    ".stSelectbox>div>div{min-height:2rem !important;max-height:2rem !important;}"
    ".stSelectbox>div>div>div{padding-top:2px !important;padding-bottom:2px !important;}"
    "[data-baseweb='select']>div{min-height:2rem !important;padding:0 8px !important;}"
    "[data-baseweb='select'] [data-baseweb='select-control']{min-height:2rem !important;height:2rem !important;}"
    "[data-testid='stSidebar']{display:none !important;}"
    "[data-testid='collapsedControl']{display:none !important;}"
    "</style>",
    unsafe_allow_html=True,
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

def _reset_filters():
    st.session_state["filter_bl"]      = "Alle"
    st.session_state["filter_tr"]      = "Alle"
    st.session_state["filter_uni_key"] = "Alle"

SEITEN = ["Gesamtüberblick", "Einflussfaktoren", "Häuser vergleichen", "Qualitäts-Vorhersage"]

# Seite aus URL lesen (überlebt Browser-Reload)
_seite_aus_url = st.query_params.get("seite", SEITEN[0])
seite = _seite_aus_url if _seite_aus_url in SEITEN else SEITEN[0]

def _gehe_zu_seite(s):
    st.query_params["seite"] = s

# Header-Banner (Titel) ────────────────────────────────────────────
st.markdown(
    f"<div style='background:#1a4f72;padding:14px 28px;border-radius:6px;"
    f"margin-top:0;margin-bottom:10px;box-shadow:0 2px 6px rgba(0,0,0,.25);'>"
    f"<h1 style='color:#fff;font-size:1.8rem;margin:0 0 2px 0;line-height:1.2;'>"
    f"Dashboard für Qualitätsprobleme deutscher Krankenhäuser</h1>"
    f"<span style='color:#a8c8e8;font-size:0.82rem'>Datenbasis: Qualitätsberichte 2023 | IQTIG</span>"
    f"</div>",
    unsafe_allow_html=True,
)

# Navigation als echte Streamlit-Buttons (kein <a href> — öffnet nie einen neuen Browser-Tab) ─
_nav_cols = st.columns(len(SEITEN))
for _i, _s in enumerate(SEITEN):
    with _nav_cols[_i]:
        st.button(
            _s, key=f"nav_{_s}", on_click=_gehe_zu_seite, args=(_s,),
            type="primary" if _s == seite else "secondary",
            width="stretch",
        )

st.markdown("<div style='margin-bottom:4px'></div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════
# SEITE 1 — UEBERSICHT
# ═════════════════════════════════════════════════════════════════
if seite == "Gesamtüberblick":
    st.markdown(
        "**Projektfrage:** Welche Krankenhausmerkmale hängen damit zusammen, "
        "dass ein Haus überdurchschnittlich viele Qualitätsprobleme aufweist?"
    )

    # ── Filter direkt auf der Seite ──────────────────────────────
    _fc1, _fc2, _fc3, _fc4 = st.columns([2, 2, 2, 1], vertical_alignment="bottom")
    filter_bundesland = _fc1.selectbox("Bundesland", get_bundesland_optionen(df), key="filter_bl")
    filter_traeger    = _fc2.selectbox("Trägerschaft", get_traeger_optionen(df), key="filter_tr")
    filter_uni        = _fc3.selectbox("Klinik-Typ", ["Alle", "Normale Klinik", "Uni-Klinik"], key="filter_uni_key")
    _fc4.button("↺ Zurücksetzen", on_click=_reset_filters, use_container_width=True)

    df_gefiltert = df.copy()
    if filter_bundesland != "Alle":
        df_gefiltert = df_gefiltert[df_gefiltert["SO.Bundesland"] == filter_bundesland]
    if filter_traeger != "Alle":
        df_gefiltert = df_gefiltert[df_gefiltert[TRAEGER_COL] == filter_traeger]
    if filter_uni != "Alle":
        df_gefiltert = df_gefiltert[df_gefiltert["Uni_Label"] == filter_uni]

    _aktive_filter = [f for f in [filter_bundesland if filter_bundesland != "Alle" else None,
        filter_traeger if filter_traeger != "Alle" else None,
        filter_uni if filter_uni != "Alle" else None] if f]
    if _aktive_filter:
        st.info(f"**Aktiver Filter:** {' · '.join(_aktive_filter)} — {len(df_gefiltert):,} von {len(df):,} Häusern")

    kpis = berechne_kpis(df_gefiltert)

    st.markdown(
        "Die vier Kennzahlen geben einen schnellen Überblick über den aktuell angezeigten Datensatz. "
        "**Krankenhäuser** — Anzahl der Häuser nach aktiven Filtern. "
        "**Anteil 'Viele Probleme'** — wie viele Häuser als auffällig eingestuft wurden (Schwelle: Median ~6 %). "
        "**Ø auffällig-Quote** — von allen Qualitätsindikatoren, die für ein Haus bewertet wurden, "
        "wie viele davon vom IQTIG als rechnerisch auffällig eingestuft wurden (d. h. das Haus weicht "
        "statistisch negativ vom Bundesdurchschnitt ab). "
        "**Ø Ärzte pro Bett** — durchschnittliche Ärztedichte."
    )

    # KPI-Karten
    _diff_50  = kpis['pct_viele'] - 0.5
    _richt_50 = "über 50 %" if _diff_50 > 0 else "unter 50 %"
    _farbe_50 = "#c0392b" if _diff_50 > 0 else "#1a6b3a"
    st.markdown(f"""
<table style="width:100%;border-collapse:collapse;margin-bottom:12px;background:#f8f9fa;
              border-radius:8px;overflow:hidden;border:1px solid #dee2e6">
  <thead>
    <tr style="background:#1a4f72;color:#fff;font-size:0.82rem;font-weight:600;text-align:center">
      <th style="padding:8px 16px">Krankenhäuser gesamt</th>
      <th style="padding:8px 16px">Anteil mit vielen Qualitätsproblemen</th>
      <th style="padding:8px 16px">Ø auffällig-Quote pro Haus</th>
      <th style="padding:8px 16px">Ø Ärzte pro Bett</th>
    </tr>
  </thead>
  <tbody>
    <tr style="text-align:center;font-size:1.4rem;font-weight:700">
      <td style="padding:10px 16px;border-right:1px solid #dee2e6">{kpis['n_haeuser']:,}</td>
      <td style="padding:10px 16px;border-right:1px solid #dee2e6">
        {kpis['pct_viele']:.1%}
        <div style="font-size:0.8rem;font-weight:500;color:{_farbe_50}">{abs(_diff_50):.1%} {_richt_50}</div>
      </td>
      <td style="padding:10px 16px;border-right:1px solid #dee2e6">
        {kpis['avg_quote']:.1%}
        <div style="font-size:0.8rem;font-weight:400;color:#6c757d">Anteil auffälliger Indikatoren</div>
      </td>
      <td style="padding:10px 16px">
        {kpis['avg_aerzte']:.3f}
        <div style="font-size:0.8rem;font-weight:400;color:#6c757d">Vollzeitstellen / Bettenzahl</div>
      </td>
    </tr>
  </tbody>
</table>
""", unsafe_allow_html=True)

    st.markdown("---")

    _n_viele  = int(df_gefiltert["hat_viele_Probleme"].sum())
    _n_wenige = len(df_gefiltert) - _n_viele

    # Karte — volle Breite
    st.subheader("Regionale Verteilung")
    _c1, _c2 = st.columns(2)
    _c1.metric("Wenige Probleme", f"{_n_wenige/len(df_gefiltert):.1%}", help=f"{_n_wenige:,} Häuser")
    _c2.metric("Viele Probleme",  f"{_n_viele/len(df_gefiltert):.1%}",  help=f"{_n_viele:,} Häuser")
    _koord_ok = df_gefiltert[["SO.Latitude","SO.Longitude"]].dropna().shape[0]
    if _koord_ok == 0:
        st.warning("⚠️ Keine Koordinaten verfügbar — Karte kann nicht angezeigt werden.")
    else:
        st.plotly_chart(erstelle_karte(df_gefiltert), use_container_width=True)
    st.caption(
        "Jeder Punkt ist ein Krankenhaus. Farbe: grün = wenige Qualitätsprobleme, rot = viele. "
        "Punktgröße entspricht der Bettenzahl. Hover für Details."
    )

    # Histogramm — volle Breite darunter
    st.subheader("Verteilung der auff\u00e4llig-Quote")
    _h1, _h2 = st.columns(2)
    _h1.metric("Wenige Probleme", f"{_n_wenige/len(df_gefiltert):.1%}", help=f"{_n_wenige:,} H\u00e4user")
    _h2.metric("Viele Probleme",  f"{_n_viele/len(df_gefiltert):.1%}",  help=f"{_n_viele:,} H\u00e4user")
    st.plotly_chart(erstelle_quote_histogramm(df_gefiltert), use_container_width=True)
    st.caption(
        f"Trennlinie = Median {kpis['median_quote']:.1%}. Farbe zeigt die Gruppe jedes Krankenhauses (gr\u00fcn = wenige, rot = viele Probleme). "
        "Balken nahe dem Median erscheinen gemischt, weil ein Balken einen Quotenbereich abdeckt, in dem Krankenh\u00e4user aus beiden Gruppen liegen k\u00f6nnen."
    )

    st.markdown("---")
    if filter_bundesland == "Alle":
        st.subheader("Vergleich nach Bundesland")
        st.plotly_chart(erstelle_bundesland_balken(df_gefiltert), use_container_width=True)
        st.caption(
            "Anteil der Krankenhäuser mit überdurchschnittlich vielen Qualitätsproblemen je Bundesland. "
            "Werte über 50 % liegen über dem deutschlandweiten Durchschnitt. "
            "Die Zahl an jedem Balken (**n**) zeigt, wie viele Krankenhäuser in diesem Bundesland ausgewertet wurden — "
            "bei kleinem n (z. B. Bremen) kann schon ein einzelnes Haus den Prozentwert stark verschieben."
        )
    else:
        st.info(f"Bundesland-Vergleich ist ausgeblendet, da der Filter auf **{filter_bundesland}** gesetzt ist — ein Vergleich aller Bundesländer wäre nicht aussagekräftig.")


# ═════════════════════════════════════════════════════════════════
# SEITE 2 — VERGLEICHE
# ═════════════════════════════════════════════════════════════════
elif seite == "Einflussfaktoren":
    st.header("Einflussfaktoren — Welche Merkmale machen den Unterschied?")
    st.info(
        "**Wichtig:** Ein Zusammenhang in den Grafiken bedeutet **nicht** automatisch Kausalität. "
        "Kein Zusammenhang ist ebenfalls ein valides Ergebnis."
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "Trägerschaft", "Ärzte pro Bett", "Streudiagramm", "Pivot-Tabelle"
    ])

    with tab1:
        st.subheader("Trägerschaft vs. Anteil 'Viele Probleme'")
        st.plotly_chart(erstelle_traeger_vergleich(df), use_container_width=True)
        st.markdown(
            "**Befund:** Öffentliche Häuser haben mit **53,5 %** den höchsten Anteil an Häusern "
            "mit vielen Qualitätsproblemen — gegenüber 50,6 % (freigemeinnützig) und 43,8 % (privat). \n\n"
            "Der Unterschied wurde mit einer **ANOVA** (Varianzanalyse) getestet — allerdings direkt auf "
            "der stetigen Auffälligkeitsquote, nicht auf den hier gezeigten, in zwei Gruppen gesplitteten "
            "Prozentsätzen. Diese Methode prüft, ob sich die drei Trägergruppen in ihrer durchschnittlichen "
            "Auffälligkeitsquote statistisch bedeutsam unterscheiden — oder ob die Unterschiede "
            "nur zufällig sind. \n\n"
            "Der **p-Wert** ist das Kernstück jedes statistischen Tests: Er gibt an, wie wahrscheinlich es wäre, "
            "den beobachteten Unterschied zu sehen, *wenn es in Wirklichkeit gar keinen Unterschied gibt*. "
            "Wir nutzen ihn hier, weil wir nicht einfach auf die Prozentzahlen schauen können — "
            "bei 1.821 Krankenhäusern könnten Unterschiede auch rein durch Zufall entstehen. "
            "Der p-Wert sagt uns, ob wir dem Unterschied vertrauen dürfen. "
            "Liegt er unter 0,05 (5 %), gilt das Ergebnis als statistisch abgesichert. \n\n"
            "Hier beträgt der **p-Wert 0,969** — praktisch 1. Das Ergebnis ist damit **NICHT statistisch "
            "signifikant**: Die drei Trägerarten liegen im Mittelwert der stetigen Quote praktisch identisch "
            "(8,56 % / 8,57 % / 8,72 %). Der oben sichtbare Unterschied in den Prozentsätzen entsteht erst "
            "durch den Median-Split in zwei Gruppen — auf Ebene der eigentlichen Quote lässt sich kein "
            "Trägerschafts-Effekt nachweisen. \n\n"
            "⚠️ **Zusätzlicher Hinweis:** Private Häuser sind im Median deutlich kleiner "
            "(125 Betten gegenüber 218 bzw. 232 bei freigemeinnützigen und öffentlichen Häusern). "
            "Das bleibt methodisch relevant, ist hier aber zweitrangig — schon auf Ebene der stetigen "
            "Quote gibt es keinen Trägereffekt, der durch die Größe erklärt werden müsste."
        )

    with tab2:
        st.subheader("Ärzte pro Bett: MIT vs. OHNE viele Probleme")
        st.plotly_chart(erstelle_boxplot_aerzte(df), use_container_width=True)
        col_a, col_b = st.columns(2)
        col_a.metric("Wenige Probleme: Ø Ärzte/Bett",
                     f"{df[df['hat_viele_Probleme']==0]['aerzte_pro_bett'].median():.3f}")
        col_b.metric("Viele Probleme: Ø Ärzte/Bett",
                     f"{df[df['hat_viele_Probleme']==1]['aerzte_pro_bett'].median():.3f}")
        st.markdown(
            "**Was zeigt dieses Diagramm?** Jede Box zeigt die Verteilung der Ärztedichte "
            "(Vollzeit-Ärzte geteilt durch Bettenzahl) für Häuser *mit* und *ohne* viele Qualitätsprobleme. "
            "Der Strich in der Mitte der Box ist der Median — also der Wert, bei dem genau die Hälfte "
            "der Häuser darunter und die Hälfte darüber liegt. "
            "Die Box selbst zeigt, wo die mittleren 50 % aller Häuser liegen: "
            "Die unterste 25 % (sehr niedrige Ärztedichte) und die obersten 25 % (sehr hohe Ärztedichte) "
            "werden dabei weggelassen — sie würden das Bild verzerren. "
            "Was bleibt, ist der 'typische' Bereich: Hier liegen die meisten normalen Häuser. "
            "Eine schmale Box bedeutet, dass die Häuser ähnlich aufgestellt sind. "
            "Eine breite Box bedeutet große Unterschiede innerhalb der Gruppe. \n\n"
            f"**Befund:** Häuser mit wenigen Problemen haben im Median **{df[df['hat_viele_Probleme']==0]['aerzte_pro_bett'].median():.3f} Ärzte pro Bett**, "
            f"Häuser mit vielen Problemen **{df[df['hat_viele_Probleme']==1]['aerzte_pro_bett'].median():.3f}** — also mehr, nicht weniger. "
            "Das klingt nach einem kleinen Unterschied — macht aber bei einem Haus mit 300 Betten "
            "rund 20 Vollzeit-Ärzte mehr oder weniger aus. \n\n"
            "Ein **T-Test** hat geprüft, ob dieser Unterschied statistisch zuverlässig ist oder zufällig sein könnte. "
            "Der T-Test vergleicht die Mittelwerte zweier Gruppen und berechnet daraus einen p-Wert. "
            "Ergebnis: t = −9,13, **p < 0,0001** — die Wahrscheinlichkeit, dass dieser Unterschied "
            "zufällig ist, liegt weit unter 0,1 %. Der Zusammenhang ist damit statistisch gesichert. \n\n"
            f"Die gestrichelte Linie bei **{DT_SPLIT} Ärzte/Bett** ist der Trennwert, den der Decision Tree "
            "automatisch gefunden hat: Häuser oberhalb dieser Grenze werden vom Modell tendenziell als "
            "Risikokandidat für viele Qualitätsprobleme eingestuft. \n\n"
            "**Schlussfolgerung:** Mehr Ärzte pro Bett geht mit mehr, nicht weniger, Qualitätsproblemen einher — "
            "vermutlich weil Häuser mit mehr Personal auch mehr Indikatoren bewertet bekommen und damit mehr "
            "Gelegenheiten für eine Auffälligkeit haben (derselbe Effekt wie bei `total_qi`, siehe Streudiagramm-Tab). "
            "Personalintensität ist trotzdem der stärkste erklärende Faktor im gesamten Datensatz. "
            "Das zeigt die sogenannte **Feature Importance** des Decision Trees: "
            "Das Modell hat beim Training selbst bewertet, welche Merkmale am stärksten dazu beitragen, "
            "ein Haus als 'viele Probleme' oder 'wenige Probleme' einzustufen. "
            "Bei **Ärzte pro Bett** liegt dieser Wert bei **72,8 %** — das bedeutet, "
            "fast drei Viertel aller Entscheidungen im Modell hängen allein an diesem einen Merkmal. "
            "Alle anderen Merkmale (Bettenzahl, Pflegekräfte, Träger usw.) teilen sich die restlichen 27,2 % auf."
        )

    with tab3:
        st.subheader("Streudiagramm")
        _merkmal_labels = {
            "aerzte_pro_bett":   "aerzte_pro_bett (Ärzte je Bett — Personalintensität)",
            "SO.Betten":         "SO.Betten (Bettenzahl — Hausgröße)",
            "fortbildungsquote": "fortbildungsquote (Anteil Ärzte mit erfüllter Fortbildungspflicht)",
            "total_qi":          "total_qi (Anzahl bewerteter Qualitätsindikatoren pro Haus)",
        }
        _merkmal_auswahl = st.selectbox(
            "Merkmal für X-Achse",
            list(_merkmal_labels.values()),
        )
        merkmal = [k for k, v in _merkmal_labels.items() if v == _merkmal_auswahl][0]
        st.plotly_chart(erstelle_streudiagramm(df, merkmal), use_container_width=True)

        _erklaerung_basis = (
            "**Was zeigt dieses Diagramm?** Jeder Punkt ist ein Krankenhaus. "
            "Die Farbe zeigt, ob das Haus viele (rot) oder wenige (grün) Qualitätsprobleme hat. "
            "Die X-Achse zeigt **{}** — die Y-Achse immer die Auffälligkeitsquote "
            "(Anteil der Indikatoren im roten Bereich). "
            "Es gibt zwei Regressionslinien — eine grüne (wenige Probleme) und eine rote (viele Probleme). "
            "Jede zeigt den Trend innerhalb ihrer Gruppe.\n\n"
        )

        _erklaerungen = {
            "aerzte_pro_bett": (
                "**Was die Linien zeigen:** Die beiden Trendlinien verlaufen uneinheitlich: Bei Häusern "
                "mit vielen Problemen sinkt die Quote mit steigender Ärztedichte leicht, bei Häusern mit "
                "wenigen Problemen bleibt sie nahezu gleich. Die Punktwolken beider Gruppen überlappen stark. \n\n"
                "**Wichtig — zwei verschiedene Blickwinkel:** Die klare Ärzte-Wirkung aus dem Boxplot-Tab "
                "(Median 0,382 vs. 0,470 Ärzte/Bett) und der hohen Feature Importance (72,8 %) bezieht sich "
                "auf den Vergleich zwischen den beiden GRUPPEN. Dieses Streudiagramm zeigt dagegen den "
                "Zusammenhang mit der STETIGEN Quote innerhalb jeder Gruppe — der ist hier deutlich schwächer "
                "und uneinheitlich. Beides sind gültige, aber unterschiedliche Perspektiven auf dieselben Daten. \n\n"
                "**Schlussfolgerung:** Ärztedichte bleibt laut Decision Tree das mit Abstand wichtigste Merkmal — "
                "aber nicht, weil sie die stetige Quote linear vorhersagt, wie dieses Diagramm zeigt."
            ),
            "SO.Betten": (
                "**Was die Linien zeigen:** Beide Linien verlaufen nahezu horizontal — die Bettenzahl hat "
                "innerhalb keiner der beiden Gruppen einen erkennbaren linearen Einfluss auf die stetige Quote. "
                "Die Punktwolken beider Gruppen überlappen stark. \n\n"
                "**Hinweis:** Bezogen auf die Gruppenzugehörigkeit (viele vs. wenige Probleme) gibt es einen "
                "schwachen, aber messbaren Zusammenhang (r = +0,14): größere Häuser gehören etwas häufiger zur "
                "Gruppe 'viele Probleme'. Auf der hier gezeigten stetigen Quote ist davon praktisch nichts zu sehen "
                "(r = −0,03). \n\n"
                "**Schlussfolgerung:** Bettenzahl allein trennt die beiden Gruppen kaum."
            ),
            "fortbildungsquote": (
                "**Warum sind die Linien fast horizontal?** Horizontale Regressionslinien bedeuten: "
                "Egal wie hoch oder niedrig die Fortbildungsquote eines Hauses ist — "
                "die Auffälligkeitsquote bleibt ungefähr gleich. "
                "Es gibt keinen erkennbaren Zusammenhang zwischen diesen beiden Merkmalen. \n\n"
                "**Schlussfolgerung:** Fortbildungsquote ist kein Qualitätsprädiktor (r ≈ 0,03, praktisch null). "
                "Ob Ärzte ihre Fortbildungspflicht erfüllen, hängt in diesem Datensatz nicht damit zusammen, "
                "wie hoch die Auffälligkeitsquote eines Hauses ist."
            ),
            "total_qi": (
                "**Was die Linien zeigen:** Beide Linien verlaufen nahezu flach, mit einem leicht fallenden "
                "Trend bei Häusern mit vielen Problemen. \n\n"
                "**Ein wichtiger Unterschied:** Bezogen auf die Gruppenzugehörigkeit (viele vs. wenige Probleme) "
                "ist total_qi das stärkste Einzelmerkmal im gesamten Datensatz (r = +0,24) — Häuser mit mehr "
                "bewerteten Indikatoren gehören häufiger zur Gruppe 'viele Probleme'. Auf der hier gezeigten "
                "STETIGEN Quote ist der Zusammenhang dagegen schwach und sogar leicht negativ (r = −0,09). "
                "Das ist kein Widerspruch: Der Median-Split, mit dem die beiden Gruppen gebildet werden, kann "
                "Zusammenhänge sichtbar machen, die auf der stetigen Skala so nicht bestehen. \n\n"
                "**Was ist total_qi?** Die Gesamtzahl der bewerteten Qualitätsindikatoren pro Haus "
                "(nach Filterung von N*-Codes und Nicht-QI-Typen). Kleine Häuser haben typischerweise weniger Fälle "
                "je Indikator und werden daher seltener bewertet — ihr total_qi ist entsprechend niedriger. \n\n"
                "**Schlussfolgerung:** total_qi ist ein Strukturmerkmal, kein Qualitätsmerkmal — ob es "
                "'positiv' oder 'negativ' wirkt, hängt davon ab, ob man die Gruppenzugehörigkeit oder die "
                "stetige Quote betrachtet."
            ),
        }

        st.markdown(
            _erklaerung_basis.format(merkmal) +
            _erklaerungen.get(merkmal, "") +
            "\n\n**Tipp:** Wechsle das Merkmal oben und vergleiche — bei allen vier Merkmalen überlappen "
            "sich die Punktwolken beider Gruppen stark, ein einzelnes Merkmal trennt hier keine klare Grenze."
        )

    with tab4:
        st.subheader("Pivot-Tabelle: Ø auffällig-Quote nach Träger × Uni-Status")
        st.markdown(
            "**Was ist eine Pivot-Tabelle?** Eine Pivot-Tabelle fasst viele Einzelwerte in einer kompakten "
            "Übersicht zusammen. Hier wird für jede Kombination aus Trägerart (Zeilen) und Uni-Status (Spalten) "
            "der **Durchschnitt der auffaellig_quote** aller Häuser in dieser Gruppe angezeigt. "
            "Ein Wert von z. B. 0,09 bedeutet: Häuser in dieser Gruppe haben im Schnitt 9 % ihrer "
            "Qualitätsindikatoren im roten Bereich. \n\n"
            "**Wofür ist das nützlich?** Sie zeigt auf einen Blick, ob sich Trägerart und Uni-Status "
            "*gemeinsam* auf die Qualität auswirken — also ob z. B. private Uni-Kliniken anders abschneiden "
            "als private Nicht-Uni-Kliniken. Das geht über die einzelnen Balkendiagramme hinaus, "
            "weil dort immer nur ein Merkmal auf einmal betrachtet wird. \n\n"
            "**Wie lesen?** Die Farbskala geht von **grün** (niedrige Auffälligkeit = besser) "
            "bis **rot** (hohe Auffälligkeit = schlechter). "
            "Die Spalte **Gesamt** zeigt den Durchschnitt über alle Häuser dieser Trägerart, unabhängig vom Uni-Status."
        )
        pivot = erstelle_pivot_traeger_uni(df)
        st.dataframe(
            pivot.style.format("{:.3f}").background_gradient(cmap="RdYlGn_r"),
            use_container_width=True,
        )
        st.markdown(
            "**Befund:** Das Bild ist gemischt: Bei freigemeinnützigen und privaten Häusern haben "
            "Uni-Kliniken eine niedrigere Auffälligkeitsquote als Nicht-Uni-Häuser (z. B. freigemeinnützig: "
            "5,5 % vs. 8,6 %). Bei öffentlichen Häusern ist es umgekehrt — dort liegt die Uni-Klinik-Quote "
            "höher (9,6 % vs. 8,6 %). Der Uni-Status wirkt sich also nicht einheitlich aus, sondern hängt "
            "mit der Trägerart zusammen — ein Beispiel dafür, warum Merkmale gemeinsam statt isoliert "
            "betrachtet werden sollten."
        )


# ═════════════════════════════════════════════════════════════════
# SEITE 3 — AEHNLICHE KRANKENHAEUSER
# ═════════════════════════════════════════════════════════════════
elif seite == "Häuser vergleichen":
    st.header("Häuser vergleichen")
    st.markdown(
        "Diese Seite hat zwei unabhängige Werkzeuge:\n\n"
        "**① Ähnliche Häuser suchen** — Gib Bettenzahl, Bundesland und Trägerschaft ein "
        "und erhalte eine Liste von Krankenhäusern mit ähnlichen Strukturmerkmalen. "
        "Nützlich, um ein bestimmtes Haus in seinen Kontext einzuordnen: "
        "Wie schlägt es sich im Vergleich zu strukturell ähnlichen Häusern? "
        "Die Toleranz bei der Bettenzahl ist einstellbar (±10 % bis ±50 %).\n\n"
        "**② Einzelhaus-Steckbrief** — Suche direkt nach einem Krankenhaus und sieh alle "
        "relevanten Kennzahlen auf einen Blick, inkl. Abstand zum Gesamtmedian."
    )
    st.markdown("---")

    col_filter, col_ergebnis = st.columns([1, 2])

    with col_filter:
        st.subheader("⚙️ Filter")
        toleranz = st.select_slider(
            "Bettenzahl-Toleranz",
            options=[0.1, 0.2, 0.3, 0.5],
            value=0.3,
            format_func=lambda x: f"\u00b1{int(x*100)} %",
        )
        eingabe_betten = st.number_input(
            f"Bettenzahl (\u00b1{int(toleranz*100)} % Toleranz)", min_value=0, max_value=2000, value=300, step=50
        )
        eingabe_bundesland = st.selectbox(
            "Bundesland", get_bundesland_optionen(df), index=0
        )
        eingabe_traeger = st.selectbox(
            "Trägerschaft", get_traeger_optionen(df), index=0
        )
        n_ergebnisse = st.slider("Max. Ergebnisse", 5, 30, 10)

        suchen = st.button("\u21aa Suchen", use_container_width=True)

    with col_ergebnis:
        if suchen:
            aehnliche = finde_aehnliche(
                df, eingabe_betten, eingabe_bundesland, eingabe_traeger, n_ergebnisse, toleranz
            )
            if aehnliche.empty:
                st.warning("Keine Häuser mit diesen Kriterien gefunden. Filter lockern.")
            else:
                st.subheader(f"{len(aehnliche)} ähnliche Häuser gefunden")
                st.dataframe(
                    aehnliche.style
                    .format({"auffaellig_quote": "{:.1%}", "aerzte_pro_bett": "{:.3f}",
                             "fortbildungsquote": "{:.1%}"})
                    .map(
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
                _diff = avg_quote - MEDIAN_QUOTE
                _richtung = "über Median" if _diff > 0 else "unter Median"
                _farbe = "#e74c3c" if _diff > 0 else "#27ae60"
                col_c1.markdown(
                    f"<div style='font-size:0.85rem;color:#6c757d;margin-bottom:4px'>Ø auffällig-Quote (Gruppe)</div>"
                    f"<div style='font-size:1.6rem;font-weight:700'>{avg_quote:.1%}</div>"
                    f"<div style='font-size:0.85rem;color:{_farbe};font-weight:600'>{abs(_diff):.1%} {_richtung}</div>",
                    unsafe_allow_html=True
                )
                col_c2.metric("Ø Ärzte/Bett (Gruppe)", f"{avg_aerzte:.3f}")
        else:
            st.info("Filter setzen und 'Suchen' klicken.")
            st.markdown(
                "**Wie funktioniert die Suche?** Das Ergebnis zeigt alle Häuser, "
                "die gleichzeitig zur gewählten Trägerart, zum gewählten Bundesland "
                "und zur Bettenzahl (±Toleranz laut Schieberegler, einstellbar von ±10 % bis ±50 %) passen. "
                "Die Tabelle ist nach Auffälligkeitsquote sortiert — "
                "Häuser mit rotem Hintergrund in der Kategorie-Spalte haben viele Qualitätsprobleme. "
                "Die zwei Kennzahlen unten zeigen den Gruppen-Durchschnitt im Vergleich zum Gesamtmedian aller ~1.821 Häuser."
            )

    st.markdown("---")

    # Einzelhaus-Steckbrief
    st.subheader("🪪 Einzelhaus-Steckbrief")
    st.markdown(
        "Wähle ein Krankenhaus aus der Liste und sieh alle Kennzahlen auf einen Blick. "
        "Der Abstandswert bei der auffällig-Quote zeigt die **Abweichung in Prozentpunkten** vom Gesamtmedian (~6 %): "
        "z. B. bedeutet **5 % über Median**: das Haus hat eine um 5 Prozentpunkte höhere Auffälligkeitsquote als der Durchschnitt — also mehr Indikatoren im roten Bereich → **rot**. "
        "**Unter Median** bedeutet weniger auffällige Indikatoren als der Durchschnitt → **grün**."
    )
    haus_auswahl = st.selectbox(
        "Krankenhaus wählen",
        options=df["SO.QBID"].tolist(),
        format_func=lambda x: df[df["SO.QBID"] == x]["SO.Name"].values[0],
    )
    if haus_auswahl:
        sb = haus_steckbrief(df, haus_auswahl)

        delta_color = "#e74c3c" if sb["delta_median"] > 0 else "#27ae60"
        richtung    = "über" if sb["delta_median"] > 0 else "unter"
        delta_label = f"{abs(sb['delta_median']):.1%} {richtung} Median"
        kategorie_color = "#e74c3c" if sb["hat_viele"] else "#27ae60"
        kategorie_label = "⚠️ Viele Probleme" if sb["hat_viele"] else "🟢 Wenige Probleme"
        aerzte_str = f"{sb['aerzte_pro_bett']:.3f}" if pd.notna(sb["aerzte_pro_bett"]) else "k.A."
        fortb_str  = f"{sb['fortbildungsquote']:.1%}" if pd.notna(sb["fortbildungsquote"]) else "k.A."

        st.markdown(f"""
<style>
.sb-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-top: 8px;
}}
.sb-card {{
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 14px 16px;
    min-width: 0;
}}
.sb-label {{
    font-size: 0.78rem;
    color: #6c757d;
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}
.sb-value {{
    font-size: 1.15rem;
    font-weight: 600;
    color: #212529;
    white-space: normal;
    word-break: break-word;
    line-height: 1.3;
}}
.sb-delta {{
    font-size: 0.82rem;
    margin-top: 3px;
    font-weight: 500;
}}
</style>
<div class="sb-grid">
  <div class="sb-card">
    <div class="sb-label">Betten</div>
    <div class="sb-value">{sb["betten"]}</div>
  </div>
  <div class="sb-card">
    <div class="sb-label">Träger</div>
    <div class="sb-value">{sb["traeger"]}</div>
  </div>
  <div class="sb-card">
    <div class="sb-label">Bundesland</div>
    <div class="sb-value">{sb["bundesland"]}</div>
  </div>
  <div class="sb-card">
    <div class="sb-label">Uni-Klinik</div>
    <div class="sb-value">{sb["uni"]}</div>
  </div>
  <div class="sb-card">
    <div class="sb-label">auffällig-Quote</div>
    <div class="sb-value">{sb["auffaellig_quote"]:.1%}</div>
    <div class="sb-delta" style="color:{delta_color}">{delta_label}</div>
  </div>
  <div class="sb-card">
    <div class="sb-label">Kategorie</div>
    <div class="sb-value" style="color:{kategorie_color}">{kategorie_label}</div>
  </div>
  <div class="sb-card">
    <div class="sb-label">Ärzte / Bett</div>
    <div class="sb-value">{aerzte_str}</div>
  </div>
  <div class="sb-card">
    <div class="sb-label">Fortbildungsquote</div>
    <div class="sb-value">{fortb_str}</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════
# SEITE 4 — RISIKO-RECHNER
# ═════════════════════════════════════════════════════════════════
elif seite == "Qualitäts-Vorhersage":
    st.header("Qualitäts-Vorhersage — Decision Tree")
    st.markdown(
        "Gib die Merkmale eines Krankenhauses ein und das Modell schätzt, "
        "ob dieses Haus wahrscheinlich **viele oder wenige Qualitätsprobleme** haben wird. "
        "Grundlage ist ein Decision Tree — ein Entscheidungsbaum, der aus den Daten von "
        "1.821 deutschen Krankenhäusern trainiert wurde. "
        "Das Modell lernt dabei selbst, welche Merkmalskombinationen typisch für Häuser "
        "mit vielen Qualitätsproblemen sind."
    )
    st.warning(
        "**Wie gut ist dieses Modell?** "
        "Das Modell trifft in **57,0 %** der Fälle die richtige Vorhersage. "
        "Zum Vergleich: Würde man einfach immer die häufigste Kategorie raten, käme man auf 50,4 % — "
        "das Modell ist also nur wenig besser als reines Raten. \n\n"
        "Die Strukturmerkmale (Betten, Träger, Personal usw.) erklären nur einen kleinen Teil davon, "
        "warum ein Haus viele Qualitätsprobleme hat. Andere Faktoren — z. B. Patientenstruktur oder "
        "Dokumentationsqualität — spielen eine größere Rolle, sind aber im Datensatz nicht enthalten. \n\n"
        "⚠️ Die Vorhersage ist daher ein **Hinweis**, keine gesicherte Diagnose."
    )

    if modell is None:
        st.error("Modell-Datei 'modell_krankenhaus.pkl' nicht gefunden. Bitte 03_Decision_Tree.ipynb ausführen.")
        st.stop()

    st.subheader(" Merkmale eingeben")
    r1, r2 = st.columns(2)

    with r1:
        ein_betten      = st.number_input("Bettenzahl", 0, 2000, 300, 50)
        ein_uni         = st.selectbox("Uni-Klinik?", ["Nein", "Ja"])
        ein_fortb       = st.slider("Fortbildungsquote", 0.0, 1.0, 0.7, 0.05,
                                    format="%.0f%%")
        ein_konzern     = st.selectbox("Konzernhaus?", ["Nein", "Ja"])
        st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
        berechnen = st.button("Ergebnis anzeigen", type="primary")

    with r2:
        ein_aerzte      = st.number_input("Ärzte pro Bett", 0.0, 5.0, 0.45, 0.05,
                                          format="%.3f")
        ein_pflege      = st.number_input("Pflegekräfte pro Bett", 0.0, 5.0, 1.0, 0.05,
                                          format="%.3f")
        ein_traeger_opt = st.selectbox("Trägerschaft",
                                       ["freigemeinnützig", "öffentlich", "privat"])
        traeger_enc_map = {"freigemeinnützig": 0, "öffentlich": 1, "privat": 2}

    st.markdown("---")

    if berechnen:
        ergebnis = berechne_risiko(
            modell,
            betten      = ein_betten,
            uni         = 1 if ein_uni == "Ja" else 0,
            fortbildung = ein_fortb,
            aerzte      = ein_aerzte,
            pflege      = ein_pflege,
            konzern     = 1 if ein_konzern == "Ja" else 0,
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

        st.markdown("---")
        st.subheader("🧩 Wie kam das Modell zu dieser Einschätzung?")
        _seite = "über" if ein_aerzte > DT_SPLIT else "unter"
        _bewertung = "erhöhtes Risiko" if ein_aerzte > DT_SPLIT else "geringeres Risiko"
        st.markdown(
            f"Das Modell trifft seine Entscheidung hauptsächlich anhand eines einzigen Merkmals: "
            f"**Ärzte pro Bett**. Dieses Merkmal erklärt fast drei Viertel der Vorhersageleistung (72,8 %). \n\n"
            f"Der wichtigste Schwellenwert liegt bei **{DT_SPLIT} Ärzte pro Bett**: \n\n"
            f"- Liegt der Wert **darüber** → das Modell stuft das Haus tendenziell als Kandidat ein, "
            f"der **überdurchschnittlich viele auffällige Qualitätsindikatoren** haben wird\n"
            f"- Liegt der Wert **darunter** → die Vorhersage hängt zusätzlich von Pflegepersonal und "
            f"Bettenzahl ab, tendenziell aber **wenige Qualitätsprobleme**\n\n"
            f"Der eingegebene Wert beträgt **{ein_aerzte:.3f}** — das ist {_seite} dem Schwellenwert "
            f"({DT_SPLIT}). Das Modell sieht daher tendenziell **{_bewertung}** für dieses Haus "
            f"(die tatsächliche Vorhersage oben berücksichtigt zusätzlich Pflegepersonal und Bettenzahl)."
        )

    st.markdown("---")
    st.subheader("⚗️ Feature Importance")
    import plotly.graph_objects as go
    fig_fi = go.Figure(go.Bar(
        x=[0.7277, 0.1648, 0.1075, 0, 0, 0, 0],
        y=[
            "Ärzte pro Bett",
            "Bettenzahl",
            "Pflegekräfte pro Bett",
            "Trägerschaft",
            "Fortbildungsquote",
            "Uni-Klinik (ja/nein)",
            "Konzernhaus (ja/nein)",
        ],
        orientation="h",
        marker_color=["#2E74B5", "#5FA0D6", "#7DC3E8", "#D9D9D9", "#D9D9D9", "#D9D9D9", "#D9D9D9"],
    ))
    fig_fi.update_layout(
        title="Welche Merkmale nutzt das Modell für seine Vorhersage?",
        xaxis_title="Anteil an der Vorhersageleistung", height=320,
        xaxis=dict(tickformat=".0%"),
    )
    st.plotly_chart(fig_fi, use_container_width=True)
    st.caption(
        "Ärzte pro Bett ist mit 72,8 % das mit Abstand wichtigste Merkmal — fast drei Viertel aller "
        "Modellentscheidungen hängen daran. Bettenzahl (16,5 %) und Pflegekräfte pro Bett (10,8 %) folgen. "
        "Trägerschaft, Fortbildungsquote, Uni-Status und Konzernzugehörigkeit tragen 0 % bei — "
        "das Modell ignoriert sie vollständig."
    )
