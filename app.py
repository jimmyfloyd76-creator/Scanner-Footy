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
    '<div class="sub-title">Selezione Dinamica & Modello Matematico xG</div>',
    unsafe_allow_html=True,
)

# --- DATABASE INTERNO PER CAMPIONATI E SQUADRE ---
db_campionati = {
    "Spagna - Segunda División": {
        "Real Zaragoza": {
            "xG_fatti": 1.55,
            "xGA_subiti": 0.95,
            "tiri_porta": 5.1,
        },
        "Sporting Gijón": {
            "xG_fatti": 1.45,
            "xGA_subiti": 1.00,
            "tiri_porta": 4.8,
        },
        "SD Huesca": {"xG_fatti": 1.15, "xGA_subiti": 1.10, "tiri_porta": 3.8},
        "CD Mirandés": {"xG_fatti": 1.10, "xGA_subiti": 1.25, "tiri_porta": 3.6},
    },
    "Brasile - Série B": {
        "Santos": {"xG_fatti": 1.85, "xGA_subiti": 0.80, "tiri_porta": 6.2},
        "Sport Recife": {"xG_fatti": 1.60, "xGA_subiti": 0.90, "tiri_porta": 5.5},
        "Coritiba": {"xG_fatti": 1.40, "xGA_subiti": 1.15, "tiri_porta": 4.6},
        "América Mineiro": {
            "xG_fatti": 1.50,
            "xGA_subiti": 1.05,
            "tiri_porta": 4.9,
        },
    },
    "Irlanda - Premier Division": {
        "Shamrock Rovers": {
            "xG_fatti": 1.90,
            "xGA_subiti": 0.85,
            "tiri_porta": 6.0,
        },
        "Shelbourne": {"xG_fatti": 1.40, "xGA_subiti": 0.75, "tiri_porta": 4.4},
        "Derry City": {"xG_fatti": 1.70, "xGA_subiti": 0.95, "tiri_porta": 5.6},
        "St Patrick's": {"xG_fatti": 1.50, "xGA_subiti": 1.10, "tiri_porta": 4.8},
    },
    "Svezia - Superettan": {
        "Landskrona BoIS": {
            "xG_fatti": 1.75,
            "xGA_subiti": 0.90,
            "tiri_porta": 5.8,
        },
        "Degerfors IF": {
            "xG_fatti": 1.60,
            "xGA_subiti": 1.05,
            "tiri_porta": 5.2,
        },
        "Örgryte IS": {"xG_fatti": 1.45, "xGA_subiti": 1.25, "tiri_porta": 4.7},
        "GIF Sundsvall": {
            "xG_fatti": 1.20,
            "xGA_subiti": 1.50,
            "tiri_porta": 3.9,
        },
    },
    "Cina - Super League": {
        "Shanghai Port": {
            "xG_fatti": 2.30,
            "xGA_subiti": 0.90,
            "tiri_porta": 7.1,
        },
        "Shanghai Shenhua": {
            "xG_fatti": 2.10,
            "xGA_subiti": 0.75,
            "tiri_porta": 6.8,
        },
        "Beijing Guoan": {
            "xG_fatti": 1.75,
            "xGA_subiti": 1.20,
            "tiri_porta": 5.4,
        },
        "Shandong Taishan": {
            "xG_fatti": 1.80,
            "xGA_subiti": 1.15,
            "tiri_porta": 5.7,
        },
    },
    "Islanda - Pepsideild": {
        "Víkingur Reykjavík": {
            "xG_fatti": 2.10,
            "xGA_subiti": 0.80,
            "tiri_porta": 6.5,
        },
        "Breiðablik": {
            "xG_fatti": 1.95,
            "xGA_subiti": 0.95,
            "tiri_porta": 6.1,
        },
        "Valur": {"xG_fatti": 1.80, "xGA_subiti": 1.10, "tiri_porta": 5.4},
        "KR Reykjavík": {
            "xG_fatti": 1.40,
            "xGA_subiti": 1.30,
            "tiri_porta": 4.5,
        },
    },
}

# --- SIDEBAR: SELEZIONE CAMPIONATO E SQUADRE ---
st.sidebar.header("🎛️ Selezione Match")
campionato_scelto = st.sidebar.selectbox(
    "Seleziona Campionato", list(db_campionati.keys())
)

squadre_disponibili = list(db_campionati[campionato_scelto].keys())

st.sidebar.markdown("---")
casa_nome = st.sidebar.selectbox(
    "Squadra in Casa", squadre_disponibili, index=0
)
ospite_nome = st.sidebar.selectbox(
    "Squadra Ospite",
    squadre_disponibili,
    index=1 if len(squadre_disponibili) > 1 else 0,
)

# Estrazione automatica dei dati di base dal dizionario del campionato scelto
dati_c = db_campionati[campionato_scelto][casa_nome]
dati_o = db_campionati[campionato_scelto][ospite_nome]

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Modifica Dati (Opzionale)")
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

st.sidebar.markdown("---")
st.sidebar.subheader("💰 Quote di Mercato")
quota_over25 = st.sidebar.number_input(
    "Quota Over 2.5", min_value=1.01, max_value=10.0, value=1.95, step=0.05
)


# --- MOTORE MATEMATICO A POISSON BIVARIATO ---
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

matrice_prob = [[0.0 for _ in range(7)] for _ in range(7)]
prob_over25 = 0.0
prob_btts = 0.0
prob_1x2 = [0.0, 0.0, 0.0]

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
st.subheader(f"⚔️ {campionato_scelto}: {casa_nome} vs {ospite_nome}")

c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "Expected Goals (Poisson)",
    f"{round(lambda_casa, 2)} - {round(lambda_ospite, 2)}",
)
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
  st.markdown("### 📊 Matrice di Forza Relativa")
  df_forze = pd.DataFrame({
      "Parametro Analitico": [
          "Forza Offensiva",
          "Forza Difensiva",
          "Tiri in Porta",
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
        f"🔥 **VALUE BET OVER 2.5**: Il modello rileva un vantaggio stimato"
        f" del **+{edge_over}%** rispetto alla quota del bookmaker."
    )
  else:
    st.info(
        "🛡️ **PASS**: Il mercato offre quote perfettamente allineate o inferiori"
        " al rischio calcolato."
    )