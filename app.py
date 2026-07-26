import math
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Scanner-Footy Pro - Global Engine", page_icon="⚽", layout="wide"
)

st.markdown(
    """
    <style>
    .main-title { font-size: 2.3rem; font-weight: 800; color: #38bdf8; text-align: center; }
    .sub-title { text-align: center; color: #9ca3af; margin-bottom: 25px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-title">⚽ SCANNER-FOOTY PRO (Global Database Engine)</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">Copertura Globale Campionati & Matrice xG</div>',
    unsafe_allow_html=True,
)

# --- DATABASE GLOBALE ESTESO PER AREE ---
db_globale = {
    "🌍 EUROPA - Top Leagues": {
        "Premier League (Inghilterra)": {
            "Manchester City": {
                "xG_fatti": 2.20,
                "xGA_subiti": 0.80,
                "tiri_porta": 7.0,
            },
            "Arsenal": {
                "xG_fatti": 2.10,
                "xGA_subiti": 0.75,
                "tiri_porta": 6.8,
            },
            "Liverpool": {
                "xG_fatti": 2.15,
                "xGA_subiti": 0.90,
                "tiri_porta": 6.9,
            },
        },
        "Serie A (Italia)": {
            "Inter": {"xG_fatti": 2.05, "xGA_subiti": 0.70, "tiri_porta": 6.5},
            "Atalanta": {
                "xG_fatti": 1.90,
                "xGA_subiti": 1.00,
                "tiri_porta": 6.2,
            },
            "Juventus": {
                "xG_fatti": 1.60,
                "xGA_subiti": 0.85,
                "tiri_porta": 5.2,
            },
        },
        "La Liga (Spagna)": {
            "Real Madrid": {
                "xG_fatti": 2.10,
                "xGA_subiti": 0.85,
                "tiri_porta": 6.7,
            },
            "Barcelona": {
                "xG_fatti": 2.25,
                "xGA_subiti": 0.95,
                "tiri_porta": 7.1,
            },
            "Atlético Madrid": {
                "xG_fatti": 1.70,
                "xGA_subiti": 0.80,
                "tiri_porta": 5.5,
            },
        },
    },
    "🌎 AMERICA - Sud & Nord": {
        "Brasileirão Série A": {
            "Flamengo": {
                "xG_fatti": 1.80,
                "xGA_subiti": 0.90,
                "tiri_porta": 5.9,
            },
            "Palmeiras": {
                "xG_fatti": 1.75,
                "xGA_subiti": 0.85,
                "tiri_porta": 5.7,
            },
            "Botafogo": {"xG_fatti": 1.85, "xGA_subiti": 0.95, "tiri_porta": 6.0},
        },
        "Argentina - Liga Profesional": {
            "River Plate": {
                "xG_fatti": 1.70,
                "xGA_subiti": 0.85,
                "tiri_porta": 5.6,
            },
            "Boca Juniors": {
                "xG_fatti": 1.55,
                "xGA_subiti": 0.90,
                "tiri_porta": 5.1,
            },
        },
    },
    "🌏 ASIA & RESTO DEL MONDO": {
        "Giappone - J1 League": {
            "Vissel Kobe": {
                "xG_fatti": 1.65,
                "xGA_subiti": 0.95,
                "tiri_porta": 5.4,
            },
            "Sanfrecce Hiroshima": {
                "xG_fatti": 1.70,
                "xGA_subiti": 0.90,
                "tiri_porta": 5.6,
            },
        },
        "Australia - A-League": {
            "Melbourne City": {
                "xG_fatti": 1.80,
                "xGA_subiti": 1.10,
                "tiri_porta": 5.8,
            },
            "Sydney FC": {"xG_fatti": 1.75, "xGA_subiti": 1.15, "tiri_porta": 5.7},
        },
    },
}

# --- SIDEBAR DI NAVIGAZIONE GLOBALE ---
st.sidebar.header("🌍 Selettore Globale")
area_scelta = st.sidebar.selectbox("Area Geografica", list(db_globale.keys()))

campionato_scelto = st.sidebar.selectbox(
    "Campionato", list(db_globale[area_scelta].keys())
)

squadre_disponibili = list(db_globale[area_scelta][campionato_scelto].keys())

st.sidebar.markdown("---")
casa_nome = st.sidebar.selectbox(
    "Squadra in Casa", squadre_disponibili, index=0
)
ospite_nome = st.sidebar.selectbox(
    "Squadra Ospite",
    squadre_disponibili,
    index=1 if len(squadre_disponibili) > 1 else 0,
)

dati_c = db_globale[area_scelta][campionato_scelto][casa_nome]
dati_o = db_globale[area_scelta][campionato_scelto][ospite_nome]

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Parametri Match")
xg_fatti_c = st.sidebar.number_input(
    "xG Fatti Casa", 0.0, 5.0, float(dati_c["xG_fatti"]), 0.05
)
xga_subiti_c = st.sidebar.number_input(
    "xG Subiti Casa", 0.0, 5.0, float(dati_c["xGA_subiti"]), 0.05
)
tiri_porta_c = st.sidebar.number_input(
    "Tiri in Porta Casa", 0.0, 20.0, float(dati_c["tiri_porta"]), 0.1
)

xg_fatti_o = st.sidebar.number_input(
    "xG Fatti Ospite", 0.0, 5.0, float(dati_o["xG_fatti"]), 0.05
)
xga_subiti_o = st.sidebar.number_input(
    "xG Subiti Ospite", 0.0, 5.0, float(dati_o["xGA_subiti"]), 0.05
)
tiri_porta_o = st.sidebar.number_input(
    "Tiri in Porta Ospite", 0.0, 20.0, float(dati_o["tiri_porta"]), 0.1
)

quota_over25 = st.sidebar.number_input(
    "Quota Over 2.5", min_value=1.01, max_value=10.0, value=1.95, step=0.05
)


# --- MOTORE MATEMATICO ---
def poisson_prob(lmbda, k):
  return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)


media_gol_campionato = 2.6
forza_attacco_casa = xg_fatti_c / (media_gol_campionato / 2)
forza_difesa_ospite = xga_subiti_o / (media_gol_campionato / 2)
forza_attacco_ospite = xg_fatti_o / (media_gol_campionato / 2)
forza_difesa_casa = xga_subiti_c / (media_gol_campionato / 2)

fattore_tiri_casa = tiri_porta_c / 4.8
fattore_tiri_ospite = tiri_porta_o / 4.8

lambda_casa = (
    forza_attacco_casa * forza_difesa_ospite * (media_gol_campionato / 2)
) * (0.8 + 0.2 * fattore_tiri_casa)
lambda_ospite = (
    forza_attacco_ospite * forza_difesa_casa * (media_gol_campionato / 2)
) * (0.8 + 0.2 * fattore_tiri_ospite)

prob_over25 = sum(
    poisson_prob(lambda_casa, i) * poisson_prob(lambda_ospite, j)
    for i in range(7)
    for j in range(7)
    if i + j > 2
)
prob_over25_pct = prob_over25 * 100
quota_equa_over = round(100 / prob_over25_pct, 2) if prob_over25_pct > 0 else 99.0
edge_over = round(((prob_over25_pct / 100) * quota_over25 - 1) * 100, 1)

# --- UI PRINCIPALE ---
st.subheader(f"⚔️ [{campionato_scelto}] {casa_nome} vs {ospite_nome}")

c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "Expected Goals", f"{round(lambda_casa, 2)} - {round(lambda_ospite, 2)}"
)
c2.metric("Probabilità Over 2.5", f"{round(prob_over25_pct, 1)}%")
c3.metric("Quota Equa", quota_equa_over)
c4.metric(
    "Edge Over",
    f"+{edge_over}%" if edge_over > 0 else f"{edge_over}%",
    delta="Value Bet" if edge_over > 4 else "No Value",
)