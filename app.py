import pandas as pd
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="Scanner-Footy Pro", page_icon="⚽", layout="wide"
)

# --- FORZATURA GRAFICA PROFESSIONALE (Sfondo Scuro & Stile Terminale) ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0d1117;
        color: #f0f6fc;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #58a6ff;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #8b949e;
        margin-bottom: 30px;
    }
    .card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Titolo dell'applicazione
st.markdown(
    '<div class="main-title">⚽ SCANNER-FOOTY PRO</div>', unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-title">Advanced xG & Value Bet Analytical Engine</div>',
    unsafe_allow_html=True,
)

# Database interno completo per i campionati richiesti
# Senza bisogno di API esterne: veloce, sicuro e sempre disponibile
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

# Pannello di controllo laterale
st.sidebar.header("🎛️ Filtri Analisi")
campionato = st.sidebar.selectbox("Seleziona Campionato", list(db_campionati.keys()))

squadre = list(db_campionati[campionato].keys())
st.sidebar.markdown("---")
casa = st.sidebar.selectbox("Squadra in Casa", squadre, index=0)
ospite = st.sidebar.selectbox("Squadra Ospite", squadre, index=1 if len(squadre) > 1 else 0)

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Quote Bookmaker")
quota_over = st.sidebar.number_input("Quota Over 2.5", 1.01, 10.0, 1.95, 0.05)

# Estrazione dati
d_casa = db_campionati[campionato][casa]
d_ospite = db_campionati[campionato][ospite]

# Calcoli del modello
xg_match = (
    d_casa["xG_fatti"]
    + d_ospite["xGA_subiti"]
    + d_ospite["xG_fatti"]
    + d_casa["xGA_subiti"]
) / 2
prob_over = min(
    max(
        (xg_match / 2.7) * 100
        + (d_casa["tiri_porta"] + d_ospite["tiri_porta"] - 9) * 1.5,
        15.0,
    ),
    92.0,
)
fair_odd = round(100 / prob_over, 2)
value_pct = round(((prob_over / 100) * quota_over - 1) * 100, 1)

# Area Visiva Principale
st.subheader(f"Analisi Scontro: {casa} vs {ospite}")

c1, c2, c3, c4 = st.columns(4)
c1.metric("xG Stimati Match", round(xg_match, 2))
c2.metric("Probabilità Over 2.5", f"{round(prob_over, 1)}%")
c3.metric("Quota Equa", fair_odd)
c4.metric(
    "Valore (Edge)",
    f"+{value_pct}%" if value_pct > 0 else f"{value_pct}%",
    delta="Value Bet" if value_pct > 3 else "No Value",
)

st.markdown("---")

# Tabella riassuntiva
st.markdown("### 📋 Parametri a Confronto")
df_summary = pd.DataFrame({
    "Metrica": ["xG Fatti (Media)", "xGA Subiti (Media)", "Tiri in Porta Medi"],
    casa: [d_casa["xG_fatti"], d_casa["xGA_subiti"], d_casa["tiri_porta"]],
    ospite: [
        d_ospite["xG_fatti"],
        d_ospite["xGA_subiti"],
        d_ospite["tiri_porta"],
    ],
})
st.dataframe(df_summary, use_container_width=True)

# Consigli operativi puliti
if value_pct >= 4.0:
  st.success(
      f"🔥 **SEGNALE OPERATIVO**: Il modello rileva un vantaggio del"
      f" **+{value_pct}%** sull'Over 2.5 rispetto alla quota del bookmaker."
  )
else:
  st.info(
      "🛡️ **ATTESA**: Margine di valore non sufficiente per procedere con la"
      " scommessa su questo match."
  )