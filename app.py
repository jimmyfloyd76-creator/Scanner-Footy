import math
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Scanner-Footy Pro - Book Killer Engine",
    page_icon="🎯",
    layout="wide",
)

# --- PERSONALIZZAZIONE GRAFICA & SFONDO ---
st.markdown(
    """
    <style>
    .main-title { font-size: 2.2rem; font-weight: 800; color: #f43f5e; text-align: center; }
    .sub-title { text-align: center; color: #9ca3af; margin-bottom: 20px; }
    /* Esempio per personalizzare lo sfondo dell'app */
    .stApp {
        background-color: #0e1117;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-title">🎯 BOOK KILLER ENGINE (xG + SoT Variant Matrix)'
    "</div>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">Analisi Avanzata delle Inefficienze di Quota (1X2,'
    " Over/Under 2.5, Over 1.5 Casa/Ospite)</div>",
    unsafe_allow_html=True,
)

# --- INIZIALIZZAZIONE MEMORIA STORICO (SESSION STATE) ---
if "storico_partite" not in st.session_state:
  st.session_state.storico_partite = {}

# --- SIDEBAR: INPUT METRICHE ---
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

st.sidebar.subheader("✈️ Squadra Ospite (Metriche)")
xg_o = st.sidebar.number_input("xG Prodotti Ospite", 0.0, 5.0, 1.25, 0.05)
xga_o = st.sidebar.number_input("xG Concessi Ospite", 0.0, 5.0, 1.30, 0.05)
sot_f_o = st.sidebar.number_input(
    "Shots on Target (In Porta) Fatti Ospite", 0.0, 15.0, 4.4, 0.1
)
sot_a_o = st.sidebar.number_input(
    "Shots on Target (In Porta) Subiti Ospite", 0.0, 15.0, 4.9, 0.1
)

st.sidebar.markdown("---")
st.sidebar.subheader("💰 Quote Reali del Bookmaker (1X2 & Totali)")
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

st.sidebar.markdown("---")
st.sidebar.subheader("💰 Quote Over 1.5 Squadra")
q_over15_c = st.sidebar.number_input(
    "Quota Over 1.5 Casa", min_value=1.01, max_value=10.0, value=2.20, step=0.05
)
q_over15_o = st.sidebar.number_input(
    "Quota Over 1.5 Ospite", min_value=1.01, max_value=10.0, value=2.60, step=0.05
)

st.sidebar.markdown("---")
st.sidebar.subheader("💾 Gestione Archivio Partite")

# Pulsante per salvare il match corrente
if st.sidebar.button("📥 Salva Partita Corrente"):
  st.session_state.storico_partite[match_nome] = {
      "xg_c": xg_c,
      "xga_c": xga_c,
      "sot_f_c": sot_f_c,
      "sot_a_c": sot_a_c,
      "xg_o": xg_o,
      "xga_o": xga_o,
      "sot_f_o": sot_f_o,
      "sot_a_o": sot_a_o,
      "q_1": q_1,
      "q_x": q_x,
      "q_2": q_2,
      "q_over": q_over,
      "q_under": q_under,
      "q_over15_c": q_over15_c,
      "q_over15_o": q_over15_o,
  }
  st.sidebar.success(f"Partita '{match_nome}' salvata con successo!")

# Selezione per richiamare o eliminare una partita salvata
if st.session_state.storico_partite:
  st.sidebar.markdown("### 📂 Partite Salvate")
  match_selezionato = st.sidebar.selectbox(
      "Seleziona match da richiamare",
      list(st.session_state.storico_partite.keys()),
  )

  col_carica, col_elimina = st.sidebar.columns(2)
  if col_carica.button("📂 Carica"):
    dati = st.session_state.storico_partite[match_selezionato]
    st.rerun()

  if col_elimina.button("🗑️ Elimina"):
    del st.session_state.storico_partite[match_selezionato]
    st.rerun()

# --- MOTORE DI CALCOLO ---
somma_inversa_1x2 = (1 / q_1) + (1 / q_x) + (1 / q_2)
overround_1x2 = (somma_inversa_1x2 - 1) * 100

fattore_sot_casa = (sot_f_c + sot_a_o) / 9.0
fattore_sot_ospite = (sot_f_o + sot_a_c) / 9.0

base_lambda_c = (xg_c + xga_o) / 2
base_lambda_o = (xg_o + xga_c) / 2

lambda_c = base_lambda_c * (0.75 + 0.25 * fattore_sot_casa)
lambda_o = base_lambda_o * (0.75 + 0.25 * fattore_sot_ospite)
lambda_totale = lambda_c + lambda_o


def poisson(lmbda, k):
  return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)


p_1, p_x, p_2 = 0.0, 0.0, 0.0
p_over25 = 0.0
p_over15_casa = 0.0
p_over15_ospite = 0.0

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
    if i >= 2:
      p_over15_casa += prob_punteggio
    if j >= 2:
      p_over15_ospite += prob_punteggio

edge_1 = ((p_1 * q_1) - 1) * 100
edge_x = ((p_x * q_x) - 1) * 100
edge_2 = ((p_2 * q_2) - 1) * 100
edge_over = ((p_over25 * q_over) - 1) * 100
edge_under = (((1 - p_over25) * q_under) - 1) * 100
edge_over15_c = ((p_over15_casa * q_over15_c) - 1) * 100
edge_over15_o = ((p_over15_ospite * q_over15_o) - 1) * 100

# --- DASHBOARD VISIVO ---
st.subheader(f"⚔️ Analisi di Scostamento: {match_nome}")

col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "Lavagna Book (Overround)",
    f"{round(overround_1x2, 2)}%",
    delta_color="inverse",
)
col2.metric("Lambda Casa Corretto", round(lambda_c, 2))
col3.metric("Lambda Ospite Corretto", round(lambda_o, 2))
col4.metric(
    "Totale Gol Attesi (Somma)",
    round(lambda_totale, 2),
    help="Somma dei Lambda (Casa + Ospite)",
)

st.markdown("---")
st.markdown("### 📊 Tabella Comparativa: Modello Integrato vs Bookmaker")

df_comparativa = pd.DataFrame({
    "Mercato / Segno": [
        "1 (Casa)",
        "X (Pareggio)",
        "2 (Ospite)",
        "Over 2.5",
        "Under 2.5",
        "Over 1.5 Casa",
        "Over 1.5 Ospite",
    ],
    # Arrotondamento delle quote book a numeri interi senza decimali (es. int() o round(..., 0))
    "Quota Book": [
        int(round(q_1, 0)),
        int(round(q_x, 0)),
        int(round(q_2, 0)),
        int(round(q_over, 0)),
        int(round(q_under, 0)),
        int(round(q_over15_c, 0)),
        int(round(q_over15_o, 0)),
    ],
    "Prob. Reale Modello": [
        f"{round(p_1*100, 1)}%",
        f"{round(p_x*100, 1)}%",
        f"{round(p_2*100, 1)}%",
        f"{round(p_over25*100, 1)}%",
        f"{round((1-p_over25)*100, 1)}%",
        f"{round(p_over15_casa*100, 1)}%",
        f"{round(p_over15_ospite*100, 1)}%",
    ],
    # Arrotondamento delle quote eque reali a numeri interi senza decimali
    "Quota Equa Reale": [
        int(round(1 / p_1, 0)) if p_1 > 0 else 0,
        int(round(1 / p_x, 0)) if p_x > 0 else 0,
        int(round(1 / p_2, 0)) if p_2 > 0 else 0,
        int(round(1 / p_over25, 0)) if p_over25 > 0 else 0,
        int(round(1 / (1 - p_over25), 0)) if (1 - p_over25) > 0 else 0,
        int(round(1 / p_over15_casa, 0)) if p_over15_casa > 0 else 0,
        int(round(1 / p_over15_ospite, 0)) if p_over15_ospite > 0 else 0,
    ],
    "Edge (Valore %)": [
        f"+{round(edge_1, 1)}%" if edge_1 > 0 else f"{round(edge_1, 1)}%",
        f"+{round(edge_x, 1)}%" if edge_x > 0 else f"{round(edge_x, 1)}%",
        f"+{round(edge_2, 1)}%" if edge_2 > 0 else f"{round(edge_2, 1)}%",
        f"+{round(edge_over, 1)}%" if edge_over > 0 else f"{round(edge_over, 1)}%",
        f"+{round(edge_under, 1)}%"
        if edge_under > 0
        else f"{round(edge_under, 1)}%",
        f"+{round(edge_over15_c, 1)}%"
        if edge_over15_c > 0
        else f"{round(edge_over15_c, 1)}%",
        f"+{round(edge_over15_o, 1)}%"
        if edge_over15_o > 0
        else f"{round(edge_over15_o, 1)}%",
    ],
})


def evidenzia_positivo(val):
  if isinstance(val, str) and val.startswith("+"):
    return (
        "color: #22c55e; font-weight: bold; background-color: rgba(34, 197, 94,"
        " 0.1);"
    )
  return ""


df_styled = df_comparativa.style.map(
    evidenzia_positivo, subset=["Edge (Valore %)"]
)

st.dataframe(df_styled, use_container_width=True)

st.markdown("---")
st.markdown("### 🎯 Segnali di Inefficienza Rilevati (Value Finder)")

valori_trovati = False
edges = {
    "Segno 1": edge_1,
    "Segno X": edge_x,
    "Segno 2": edge_2,
    "Over 2.5": edge_over,
    "Under 2.5": edge_under,
    "Over 1.5 Casa": edge_over15_c,
    "Over 1.5 Ospite": edge_over15_o,
}

for mercato, val in edges.items():
  if val >= 3.5:
    valori_trovati = True
    st.success(
        f"🔥 **POSSIBILE VALUE BET SU [{mercato}]**: Il tuo modello rileva un"
        f" vantaggio stimato del **+{round(val, 1)}%** rispetto al banco."
    )

if not valori_trovati:
  st.info(
      "🛡️ **NESSUN VARCO EVIDENTE**: Le quote del bookmaker sui vari mercati"
      " sono ben allineate alle stime del modello."
  )