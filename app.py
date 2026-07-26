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
    '<div class="main-title">🎯 BOOK KILLER ENGINE (xG + SoT In/Out Variant'
    ' Matrix)</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">Analisi Avanzata delle Inefficienze di Quota basata'
    ' su xG, Tiri in Porta e Tiri Fuori</div>',
    unsafe_allow_html=True,
)

# --- SIDEBAR: INPUT MANUALE DI PRECISIONE & METRICHE ---
st.sidebar.header("🕹️ Setup Partita & Metriche Studi")

match_nome = st.sidebar.text_input("Match (es. Squadra A vs Squadra B)", "Match #1")

st.sidebar.subheader("🏠 Squadra di Casa (Metriche)")
xg_c = st.sidebar.number_input("xG Prodotti Casa", 0.0, 5.0, 1.55, 0.05)
xga_c = st.sidebar.number_input("xG Concessi Casa", 0.0, 5.0, 1.10, 0.05)
sot_f_c = st.sidebar.number_input(
    "Shots on Target (In Porta) Fatti Casa", 0.0, 15.0, 5.2, 0.1
)
sot_a_c = st.sidebar.number_input(
    "Shots on Target (In Porta) Subiti Casa", 0.0, 15.0, 3.8, 0.1
)
sot_out_f_c = st.sidebar.number_input(
    "Shots Off Target (Fuori) Fatti Casa", 0.0, 20.0, 6.5, 0.1
)
sot_out_a_c = st.sidebar.number_input(
    "Shots Off Target (Fuori) Subiti Casa", 0.0, 20.0, 5.0, 0.1
)

st.sidebar.subheader("✈️ Squadra Ospite (Metriche)")
xg_o = st.sidebar.number_input("xG Prodotti Ospite", 0.0, 5.0, 1.25, 0.05)
xga_o = st.sidebar.number_input("xG Concessi Ospite", 0.0, 5.0, 1.30, 0.05)
sot_f_o = st.sidebar.number_input(
    "Shots on Target (In Porta) Fatti Ospite", 0.0, 15.0, 4.4, 0.1
)
sot_a_o = st.sidebar.number_input(
    "Shots on Target (In Porta) Subiti Ospite", 0.0, 15.0, 4.9, 0.1
)
sot_out_f_o = st.sidebar.number_input(
    "Shots Off Target (Fuori) Fatti Ospite", 0.0, 20.0, 5.5, 0.1
)
sot_out_a_o = st.sidebar.number_input(
    "Shots Off Target (Fuori) Subiti Ospite", 0.0, 20.0, 6.0, 0.1
)

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


# --- MOTORE DI CALCOLO SCENARI (xG + SoT In + SoT Out CORRECTION) ---
# 1. Calcolo Overround (Lavagna del book)
somma_inversa_1x2 = (1 / q_1) + (1 / q_x) + (1 / q_2)
overround_1x2 = (somma_inversa_1x2 - 1) * 100

# 2. Modello di incrocio avanzato comprensivo di tiri fuori (volume offensivo totale)
fattore_sot_casa = (sot_f_c + sot_a_o) / 9.0
fattore_sot_ospite = (sot_f_o + sot_a_c) / 9.0

# Ponderazione dei tiri fuori (impatto minore rispetto a quelli in porta, stimato al 10%)
fattore_out_casa = (sot_out_f_c + sot_out_a_o) / 11.0
fattore_out_ospite = (sot_out_f_o + sot_out_a_c) / 11.0

base_lambda_c = (xg_c + xga_o) / 2
base_lambda_o = (xg_o + xga_c) / 2

lambda_c = base_lambda_c * (0.65 + 0.25 * fattore_sot_casa + 0.10 * fattore_out_casa)
lambda_o = base_lambda_o * (0.65 + 0.25 * fattore_sot_ospite + 0.10 * fattore_out_ospite)


def poisson(lmbda, k):
  return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)


# Generazione matrice 6x6 per le varianti esatte
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
col2.metric("Lambda Casa Corretto (xG+SoT+Out)", round(lambda_c, 2))
col3.metric("Lambda Ospite Corretto (xG+SoT+Out)", round(lambda_o, 2))

st.markdown("---")
st.markdown("### 📊 Tabella Comparativa: Modello Integrato vs Bookmaker")

df_comparativa = pd.DataFrame({
    "Mercato / Segno": [
        "1 (Casa)",
        "X (Pareggio)",
        "2 (Ospite)",
        "Over 2.5",
        "Under 2.5",
    ],
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
        f"+{round(edge_under, 1)}%"
        if edge_under > 0
        else f"{round(edge_under, 1)}%",
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
        f"🔥 **POSSIBILE VALUE BET SU [{mercato}]**: Il tuo modello completo"
        f" (xG + tiri in porta + tiri fuori) rileva un vantaggio stimato del"
        f" **+{round(val, 1)}%** rispetto al banco."
    )

if not valori_trovati:
  st.info(
      "🛡️ **NESSUN VARCO EVIDENTE**: Le quote del bookmaker riflettono"
      " accuratamente il volume complessivo dei tiri registrati."
  )