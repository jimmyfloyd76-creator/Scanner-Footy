import math
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Scanner-Footy Pro - Book Killer Engine",
    page_icon="🎯",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title { font-size: 2.2rem; font-weight: 800; color: #f43f5e; text-align: center; }
    .sub-title { text-align: center; color: #9ca3af; margin-bottom: 20px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-title">🎯 BOOK KILLER ENGINE (Analisi Varianti & Edge)'
    "</div>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">Sganciare il calcolo dai database e attaccare le'
    " inefficienze di quota</div>",
    unsafe_allow_html=True,
)

# --- SIDEBAR: INPUT MANUALE DI PRECISIONE & QUOTE BOOK ---
st.sidebar.header("🕹️ Setup Partita & Metriche Tuoi Studi")

match_nome = st.sidebar.text_input("Match (es. Squadra A vs Squadra B)", "Match #1")

st.sidebar.subheader("📊 Valori Analitici (I Tuoi Studi)")
xg_c = st.sidebar.number_input("xG Prodotti Casa", 0.0, 5.0, 1.55, 0.05)
xga_c = st.sidebar.number_input("xG Concessi Casa", 0.0, 5.0, 1.10, 0.05)
xg_o = st.sidebar.number_input("xG Prodotti Ospite", 0.0, 5.0, 1.25, 0.05)
xga_o = st.sidebar.number_input("xG Concessi Ospite", 0.0, 5.0, 1.30, 0.05)

st.sidebar.markdown("---")
st.sidebar.subheader("💰 Quote Reali del Bookmaker")
q_1 = st.sidebar.number_input(
    "Quota 1", min_value=1.01, max_value=20.0, value=2.10, step=0.05
)
q_x = st.sidebar.number_input(
    "Quota X", min_value=1.01, max_value=20.0, value=3.40, step=0.05
)
q_2 = st.sidebar.number_input(
    "Quota 2", min_value=1.01, max_value=20.0, value=3.60, step=0.05
)

q_over = st.sidebar.number_input(
    "Quota Over 2.5", min_value=1.01, max_value=10.0, value=2.00, step=0.05
)
q_under = st.sidebar.number_input(
    "Quota Under 2.5", min_value=1.01, max_value=10.0, value=1.80, step=0.05
)


# --- MOTORE DI CALCOLO SCENARI E DISINNERVO BOOK ---
# 1. Calcolo Overround (Lavagna del book) e pulizia della probabilità implicita
somma_inversa_1x2 = (1 / q_1) + (1 / q_x) + (1 / q_2)
overround_1x2 = (somma_inversa_1x2 - 1) * 100

# Probabilità reali implicite ripulite dall'aggio del book
prob_imp_1 = (1 / q_1) / somma_inversa_1x2
prob_imp_x = (1 / q_x) / somma_inversa_1x2
prob_imp_2 = (1 / q_2) / somma_inversa_1x2

# 2. Modello Poisson Corretto per le varianti del match
lambda_c = (xg_c + xga_o) / 2
lambda_o = (xg_o + xga_c) / 2


def poisson(lmbda, k):
  return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)


# Generazione matrice 6x6 per calcolare le varianti esatte
p_1, p_x, p_2 = 0.0, 0.0, 0.0
p_over25 = 0.0

for i in range(6):
  for j in range(6):
    prob_punteggio = poisson(lambda_c, i) * poisson(lambda_o, j)
    if i > j:
      p_1 += prob_punteggio
    elif i == j:
      p_x += prob_punteggio
    else:
      p_2 += prob_punteggio
    if i + j > 2:
      p_over25 += prob_punteggio

# 3. Calcolo Edge / Scarto contro il Bookmaker
edge_1 = ((p_1 * q_1) - 1) * 100
edge_x = ((p_x * q_x) - 1) * 100
edge_2 = ((p_2 * q_2) - 1) * 100

edge_over = ((p_over25 * q_over) - 1) * 100
edge_under = (((1 - p_over25) * q_under) - 1) * 100

# --- DASHBOARD VISIVO DI ATTACCO AL BOOK ---
st.subheader(f"⚔️ Analisi di Scostamento: {match_nome}")

col1, col2, col3 = st.columns(3)
col1.metric("Lavagna Book (Overround)", f"{round(overround_1x2, 2)}%", delta_color="inverse")
col2.metric("Lambda Casa (xG Modello)", round(lambda_c, 2))
col3.metric("Lambda Ospite (xG Modello)", round(lambda_o, 2))

st.markdown("---")
st.markdown("### 📊 Tabella Comparativa: Modello (Tuoi Studi) vs Bookmaker")

df_comparativa = pd.DataFrame({
    "Mercato / Segno": ["1 (Casa)", "X (Pareggio)", "2 (Ospite)", "Over 2.5", "Under 2.5"],
    "Quota Book": [q_1, q_x, q_2, q_over, q_under],
    "Prob. Reale Modello": [
        f"{round(p_1*100, 1)}%",
        f"{round(p_x*100, 1)}%",
        f"{round(p_2*100, 1)}%",
        f"{round(p_over25*100, 1)}%",
        f"{round((1-p_over25)*100, 1)}%",
    ],
    "Quota Equa Reale": [
        round(1 / p_1, 2) if p_1 > 0 else 0,
        round(1 / p_x, 2) if p_x > 0 else 0,
        round(1 / p_2, 2) if p_2 > 0 else 0,
        round(1 / p_over25, 2) if p_over25 > 0 else 0,
        round(1 / (1 - p_over25), 2) if (1 - p_over25) > 0 else 0,
    ],
    "Edge (Valore %)": [
        f"+{round(edge_1, 1)}%" if edge_1 > 0 else f"{round(edge_1, 1)}%",
        f"+{round(edge_x, 1)}%" if edge_x > 0 else f"{round(edge_x, 1)}%",
        f"+{round(edge_2, 1)}%" if edge_2 > 0 else f"{round(edge_2, 1)}%",
        f"+{round(edge_over, 1)}%" if edge_over > 0 else f"{round(edge_over, 1)}%",
        f"+{round(edge_under, 1)}%" if edge_under > 0 else f"{round(edge_under, 1)}%",
    ],
})

st.dataframe(df_comparativa, use_container_width=True)

st.markdown("---")
st.markdown("### 🎯 Segnali di Inefficienza Rilevati (Value Finder)")

valori_trovati = False
edges = {
    "Segno 1": edge_1,
    "Segno X": edge_x,
    "Segno 2": edge_2,
    "Over 2.5": edge_over,
    "Under 2.5": edge_under,
}

for mercato, val in edges.items():
  if val >= 3.5:
    valori_trovati = True
    st.success(
        f"🔥 **POSSIBILE VALUE BET SU [{mercato}]**: Il tuo modello calcola un"
        f" vantaggio stimato del **+{round(val, 1)}%** rispetto alla quota"
        f" proposta dal banco."
    )

if not valori_trovati:
  st.info(
      "🛡️ **NESSUN VARco EVIDENTE**: Le quote del bookmaker sono strettamente"
      " allineate al rischio stimato dal modello matematico. Meglio passare"
      " oltre o cercare varianti live."
  )