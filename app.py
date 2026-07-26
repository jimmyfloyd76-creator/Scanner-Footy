import pandas as pd
import streamlit as st

# Configurazione pagina e layout largo
st.set_page_config(
    page_title="Scanner-Footy Pro", page_icon="⚽", layout="wide"
)

# --- CSS FORZATO PER SFONDO SCURO E GRAFICA PROFESSIONALE ---
st.markdown(
    """
    <style>
    /* Sfondo generale scuro stile terminale finanziario */
    .stApp {
        background-color: #0b0f19 !important;
        color: #f3f4f6 !important;
    }
    /* Header principale */
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #38bdf8;
        text-align: center;
        letter-spacing: 1px;
    }
    .sub-title {
        text-align: center;
        color: #9ca3af;
        margin-bottom: 25px;
        font-size: 1rem;
    }
    /* Box metriche e tabelle */
    div[data-testid="stMetric"] {
        background-color: #111827;
        border: 1px solid #1f2937;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Titolo e sottotitolo
st.markdown(
    '<div class="main-title">⚽ SCANNER-FOOTY PRO</div>', unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-title">Advanced xG, Shots & Value Bet Analytics Engine</div>',
    unsafe_allow_html=True,
)

# Database interno strutturato per i campionati di riferimento
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

# Sidebar dei filtri
st.sidebar.header("🎛️ Pannello di Controllo")
campionato_sel = st.sidebar.selectbox(
    "Seleziona Campionato", list(db_campionati.keys())
)

squadre_list = list(db_campionati[campionato_sel].keys())
st.sidebar.markdown("---")
casa_sel = st.sidebar.selectbox("Squadra in Casa", squadre_list, index=0)
ospite_sel = st.sidebar.selectbox(
    "Squadra Ospite",
    squadre_list,
    index=1 if len(squadre_list) > 1 else 0,
)

st.sidebar.markdown("---")
st.sidebar.subheader("💰 Parametri di Mercato")
quota_mercato = st.sidebar.number_input(
    "Quota Over 2.5", min_value=1.01, max_value=10.0, value=1.95, step=0.05
)

# Estrazione dati delle squadre scelte
d_casa = db_campionati[campionato_sel][casa_sel]
d_ospite = db_campionati[campionato_sel][ospite_sel]

# Motore di calcolo analitico avanzato xG & Tiri
xg_totale = (
    d_casa["xG_fatti"]
    + d_ospite["xGA_subiti"]
    + d_ospite["xG_fatti"]
    + d_casa["xGA_subiti"]
) / 2
prob_calcolata = min(
    max(
        (xg_totale / 2.7) * 100
        + (d_casa["tiri_porta"] + d_ospite["tiri_porta"] - 9) * 1.5,
        15.0,
    ),
    92.0,
)
quota_equa = round(100 / prob_calcolata, 2)
edge_valore = round(((prob_calcolata / 100) * quota_mercato - 1) * 100, 1)

# Sezione Principale
st.subheader(f"⚔️ Scontro Diretto: {casa_sel} vs {ospite_sel}")

m1, m2, m3, m4 = st.columns(4)
m1.metric("xG Stimati Match", round(xg_totale, 2))
m2.metric("Probabilità Over 2.5", f"{round(prob_calcolata, 1)}%")
m3.metric("Quota Equa Modello", quota_equa)
m4.metric(
    "Valore (Edge)",
    f"+{edge_valore}%" if edge_valore > 0 else f"{edge_valore}%",
    delta="Value Bet" if edge_valore > 3 else "No Value",
)

st.markdown("---")

# Tabella comparativa dettagliata
st.markdown("### 📊 Tabella Statistica Comparativa")
df_analisi = pd.DataFrame({
    "Parametro Statistico": [
        "Expected Goals Fatti (Media)",
        "Expected Goals Subiti (Media)",
        "Tiri in Porta Medi",
    ],
    casa_sel: [
        d_casa["xG_fatti"],
        d_casa["xGA_subiti"],
        d_casa["tiri_porta"],
    ],
    ospite_sel: [
        d_ospite["xG_fatti"],
        d_ospite["xGA_subiti"],
        d_ospite["tiri_porta"],
    ],
})
st.dataframe(df_analisi, use_container_width=True)

# Esito operativo dell'intelligenza analitica
if edge_valore >= 4.0:
  st.success(
      f"🔥 **SEGNALE VALUE BET ATTIVO**: Il modello evidenzia un margine di"
      f" vantaggio del **+{edge_valore}%** rispetto alla quota offerta dal"
      f" bookmaker sull'Over 2.5."
  )
else:
  st.info(
      "🛡️ **NESSUN VANTAGGIO**: Le quote di mercato sono allineate o inferiori"
      " al rischio reale calcolato. Si consiglia di monitorare altri match."
  )