import math
import pandas as pd
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="Scanner-Footy Pro - Poisson & Matrix Engine",
    page_icon="⚽",
    layout="wide",
)

# Stile grafico professionale
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
    '<div class="main-title">⚽ SCANNER-FOOTY PRO (Poisson Matrix Engine)</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">Modello Matematico Avanzato di Incrocio xG & Tiri</div>',
    unsafe_allow_html=True,
)

# Sidebar per l'inserimento dei parametri avanzati
st.sidebar.header("🎛️ Parametri di Ingresso Match")

st.sidebar.subheader("🏠 Squadra di Casa")
casa_nome = st.sidebar.text_input("Nome Casa", "Squadra Casa")
xg_fatti_c = st.sidebar.number_input("xG Fatti Casa (Media)", 0.0, 5.0, 1.65, 0.05)
xga_subiti_c = st.sidebar.number_input(
    "xG Subiti Casa (Media)", 0.0, 5.0, 0.95, 0.05
)
tiri_porta_c = st.sidebar.number_input("Tiri in Porta Medi Casa", 0.0, 20.0, 5.4, 0.1)

st.sidebar.subheader("✈️ Squadra Ospite")
ospite_nome = st.sidebar.text_input("Nome Ospite", "Squadra Ospite")
xg_fatti_o = st.sidebar.number_input(
    "xG Fatti Ospite (Media)", 0.0, 5.0, 1.25, 0.05
)
xga_subiti_o = st.sidebar.number_input(
    "xG Subiti Ospite (Media)", 0.0, 5.0, 1.30, 0.05
)
tiri_porta_o = st.sidebar.number_input(
    "Tiri in Porta Medi Ospite", 0.0, 20.0, 4.1, 0.1
)

st.sidebar.markdown("---")
st.sidebar.subheader("💰 Quote di Mercato")
quota_over25 = st.sidebar.number_input(
    "Quota Over 2.5", min_value=1.01, max_value=10.0, value=1.95, step=0.05
)
quota_goal = st.sidebar.number_input(
    "Quota Goal (BTTS)", min_value=1.01, max_value=10.0, value=1.80, step=0.05
)


# --- MOTORE MATEMATICO A POISSON BIVARIATO E CORRETTO ---
def poisson_prob(lmbda, k):
  return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)


# Calcolo degli Expected Goals attesi per il singolo match (Incrocio Forza Attacco / Difesa)
# Media generale di riferimento del campionato (ipotizzata standard a 2.6 gol a partita)
media_gol_campionato = 2.6

forza_attacco_casa = xg_fatti_c / (media_gol_campionato / 2)
forza_difesa_ospite = xga_subiti_o / (media_gol_campionato / 2)
forza_attacco_ospite = xg_fatti_o / (media_gol_campionato / 2)
forza_difesa_casa = xga_subiti_c / (media_gol_campionato / 2)

# Correzione basata anche sul volume pulito dei tiri in porta
fattore_tiri_casa = tiri_porta_c / 4.8  media di riferimento tiri
fattore_tiri_ospite = tiri_porta_o / 4.8

lambda_casa = (
    forza_attacco_casa * forza_difesa_ospite * (media_gol_campionato / 2)
) * (0.8 + 0.2 * fattore_tiri_casa)
lambda_ospite = (
    forza_attacco_ospite * forza_difesa_casa * (media_gol_campionato / 2)
) * (0.8 + 0.2 * fattore_tiri_ospite)

# Generazione della matrice di Poisson (fino a 6 gol per squadra)
matrice_prob = [[0.0 for _ in range(7)] for _ in range(7)]
prob_over25 = 0.0
prob_btts = 0.0
prob_1x2 = [0.0, 0.0, 0.0]  # 1, X, 2

for i in range(7):
  for j in range(7):
    p = poisson_prob(lambda_casa, i) * poisson_prob(lambda_ospite, j)
    matrice_prob[i][j] = p
    if i + j > 2:
      prob_over25 += p
    if i > 0 and j > 0:
      prob_btts += p
    if i > j:
      prob_1x2[0] += p
    elif i == j:
      prob_1x2[1] += p
    else:
      prob_1x2[2] += p

prob_over25_pct = prob_over25 * 100
prob_btts_pct = prob_btts * 100

quota_equa_over = round(100 / prob_over25_pct, 2) if prob_over25_pct > 0 else 99.0
edge_over = round(((prob_over25_pct / 100) * quota_over25 - 1) * 100, 1)

# --- LAYOUT VISIVO PRINCIPALE ---
st.subheader(f"⚔️ Analisi Avanzata: {casa_nome} vs {ospite_nome}")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Expected Goals (Poisson)", f"{round(lambda_casa, 2)} - {round(lambda_ospite, 2)}")
c2.metric("Probabilità Over 2.5", f"{round(prob_over25_pct, 1)}%")
c3.metric("Quota Equa Modello", quota_equa_over)
c4.metric(
    "Edge / Valore Over",
    f"+{edge_over}%" if edge_over > 0 else f"{edge_over}%",
    delta="Value Bet" if edge_over > 4 else "No Value",
)

st.markdown("---")

col_tab, col_res = st.columns([1, 1])

with col_tab:
  st.markdown("### 📊 Matrice di Forza Relativa & Dati")
  df_forze = pd.DataFrame({
      "Parametro Analitico": [
          "Forza Offensiva Relativa",
          "Forza Difensiva Relativa",
          "Incidenza Tiri in Porta",
          "Gol Attesi (Lambda)",
      ],
      casa_nome: [
          round(forza_attacco_casa, 2),
          round(forza_difesa_casa, 2),
          round(tiri_porta_c, 1),
          round(lambda_casa, 2),
      ],
      ospite_nome: [
          round(forza_attacco_ospite, 2),
          round(forza_difesa_ospite, 2),
          round(tiri_porta_o, 1),
          round(lambda_ospite, 2),
      ],
  })
  st.dataframe(df_forze, use_container_width=True)

with col_res:
  st.markdown("### 🎯 Esito Modello Statistico")
  st.write(
      f"• **Probabilità Goal (BTTS):** `{round(prob_btts_pct, 1)}%` (Quota"
      f" Equa: `{round(100/prob_btts_pct, 2)}`)"
  )
  st.write(
      f"• **Probabilità Segno 1X2:** 1 (`{round(prob_1x2[0]*100,1)}%`) | X ("
      f"`{round(prob_1x2[1]*100,1)}%`) | 2 (`{round(prob_1x2[2]*100,1)}%`)"
  )

  if edge_over >= 4.0:
    st.success(
        f"🔥 **VALUE BET OVER 2.5**: Il modello di Poisson bivariato rileva un"
        f" vantaggio stimato del **+{edge_over}%** rispetto alla quota del"
        f" bookmaker."
    )
  else:
    st.info(
        "🛡️ **PASS**: Il mercato offre quote perfettamente allineate o inferiori"
        " al rischio calcolato dalla matrice."
    )