import pandas as pd
import streamlit as st

# Configurazione della pagina con layout largo
st.set_page_config(
    page_title="Scanner-Footy Pro | xG Value Engine",
    page_icon="⚽",
    layout="wide",
)

# --- STYLING CSS PERSONALIZZATO (Grafica moderna, sfondo e box dedicati) ---
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #161b22 100%);
        color: #e6edf3;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #58a6ff;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #8b949e;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #21262d;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .highlight-box {
        background-color: rgba(35, 134, 54, 0.15);
        border: 1px solid #238636;
        padding: 15px;
        border-radius: 8px;
        color: #3fb950;
        font-weight: 600;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Intestazione grafica
st.markdown(
    '<div class="main-header">⚽ SCANNER-FOOTY PRO</div>', unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-header">Advanced xG, Shots & Value Bet Analytics Engine</div>',
    unsafe_allow_html=True,
)

# Database esteso dei campionati e delle squadre principali
database_squadre = {
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
    "Ecuador - Serie A": {
        "Independiente del Valle": {
            "xG_fatti": 1.90,
            "xGA_subiti": 0.75,
            "tiri_porta": 6.3,
        },
        "LDU Quito": {"xG_fatti": 1.80, "xGA_subiti": 0.85, "tiri_porta": 5.9},
        "Barcelona SC": {"xG_fatti": 1.70, "xGA_subiti": 0.95, "tiri_porta": 5.6},
        "Emelec": {"xG_fatti": 1.45, "xGA_subiti": 1.10, "tiri_porta": 4.7},
    },
    "Argentina - Lower Divisions": {
        "San Martín de Tucumán": {
            "xG_fatti": 1.50,
            "xGA_subiti": 0.70,
            "tiri_porta": 5.0,
        },
        "Aldosivi": {"xG_fatti": 1.35, "xGA_subiti": 0.85, "tiri_porta": 4.5},
        "Colón": {"xG_fatti": 1.45, "xGA_subiti": 0.90, "tiri_porta": 4.8},
        "Nueva Chicago": {
            "xG_fatti": 1.25,
            "xGA_subiti": 0.80,
            "tiri_porta": 4.1,
        },
    },
}

# Sidebar di configurazione
st.sidebar.header("🎛️ Control Panel")
campionato_scelto = st.sidebar.selectbox(
    "Seleziona Campionato", list(database_squadre.keys())
)

squadre_disponibili = list(database_squadre[campionato_scelto].keys())

st.sidebar.markdown("---")
col_s1, col_s2 = st.sidebar.columns(2)
with col_s1:
  squadra_casa = st.selectbox("Squadra Casa", squadre_disponibili, index=0)
with col_s2:
  squadra_ospite = st.selectbox(
      "Squadra Ospite",
      squadre_disponibili,
      index=1 if len(squadre_disponibili) > 1 else 0,
  )

st.sidebar.markdown("---")
st.sidebar.subheader("💰 Quote di Mercato")
quota_over25 = st.sidebar.number_input(
    "Quota Over 2.5", min_value=1.01, max_value=10.0, value=1.95, step=0.05
)
quota_goal = st.sidebar.number_input(
    "Quota Goal (BTTS)", min_value=1.01, max_value=10.0, value=1.80, step=0.05
)

# Estrazione dati dalle squadre selezionate
dati_c = database_squadre[campionato_scelto][squadra_casa]
dati_o = database_squadre[campionato_scelto][squadra_ospite]

# Motore di calcolo analitico
expected_goals_match = (
    dati_c["xG_fatti"]
    + dati_o["xGA_subiti"]
    + dati_o["xG_fatti"]
    + dati_c["xGA_subiti"]
) / 2
prob_over25_calc = min(
    max(
        (expected_goals_match / 2.7) * 100
        + (dati_c["tiri_porta"] + dati_o["tiri_porta"] - 9) * 1.5,
        15.0,
    ),
    92.0,
)
quota_equa_over = round(100 / prob_over25_calc, 2)
valore_over = round(
    ((prob_over25_calc / 100) * quota_over25 - 1) * 100, 1
)

# Layout Principale - Visualizzazione Risultati
st.markdown(
    f"### ⚔️ Match Analysis: **{squadra_casa} vs {squadra_ospite}**"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
  st.metric(
      label="Expected Goals (xG)",
      value=round(expected_goals_match, 2),
      delta="Totali Match",
  )
with col2:
  st.metric(
      label="Probabilità Over 2.5", value=f"{round(prob_over25_calc, 1)}%"
  )
with col3:
  st.metric(label="Quota Equa Modello", value=quota_equa_over)
with col4:
  st.metric(
      label="Value Edge Over 2.5",
      value=f"+{valore_over}%" if valore_over > 0 else f"{valore_over}%",
  )

st.markdown("---")

# Sezione esito e consiglio operativo
col_esito_1, col_esito_2 = st.columns([2, 1])

with col_esito_1:
  st.markdown("#### 📊 Dettaglio Metriche Squadre")
  df_comparativo = pd.DataFrame({
      "Indicatore": [
          "Media xG Fatti",
          "Media xGA Subiti",
          "Tiri in Porta Medi",
      ],
      squadra_casa: [
          dati_c["xG_fatti"],
          dati_c["xGA_subiti"],
          dati_c["tiri_porta"],
      ],
      squadra_ospite: [
          dati_o["xG_fatti"],
          dati_o["xGA_subiti"],
          dati_o["tiri_porta"],
      ],
  })
  st.dataframe(df_comparativo, use_container_width=True)

with col_esito_2:
  st.markdown("#### 💡 Esito Analisi")
  if valore_over >= 4.0:
    st.markdown(
        f'<div class="highlight-box">🔥 CONSIGLIATO: OVER 2.5<br>Il margine di valore è'
        f" del +{valore_over}%. Le statistiche offensive di {squadra_casa} e le"
        f" concessioni di {squadra_ospite} premono per una gara da gol.</div>",
        unsafe_allow_html=True,
    )
  else:
    st.info(
        "🛡️ NESSUN VANTAGGIO RILEVATO: Le quote offerte dal bookmaker sono"
        " perfettamente allineate o inferiori al rischio calcolato dal"
        " modello. Meglio passare oltre."
    )