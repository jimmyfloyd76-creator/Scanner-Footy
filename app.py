import pandas as pd
import plotly.express as px
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="Scanner-Footy Value Bet", page_icon="⚽", layout="wide"
)

st.title("⚽ Scanner-Footy: Analisi e Value Bet")
st.markdown(
    "Benvenuto nel tuo strumento di analisi calcistica e calcolo delle quote di valore."
)

# Sidebar per la selezione dei campionati e parametri
st.sidebar.header("Parametri di Analisi")
campionato = st.sidebar.selectbox(
    "Seleziona Campionato",
    [
        "Spagna - Segunda División",
        "Brasile - Série B",
        "Irlanda - Premier Division",
        "Svezia - Superettan",
        "Cina - Super League",
        "Islanda - Pepsideild",
        "Ecuador - Serie A",
        "Argentina - Lower Divisions",
    ],
)

st.sidebar.markdown("---")
soglia_value = st.sidebar.slider(
    "Soglia di Valore Minima (%)", min_value=1.0, max_value=15.0, value=5.0, step=0.5
)

# Area Principale di Lavoro
st.subheader(f"Analisi in corso per: {campionato}")

# Dati di esempio strutturati per il test dell'applicazione
data = {
    "Partita": ["Squadra A - Squadra B", "Squadra C - Squadra D"],
    "1X2 (1)": [2.10, 1.85],
    "1X2 (X)": [3.30, 3.40],
    "1X2 (2)": [3.60, 4.20],
    "Probabilità Modello (%)": ["52.0%", "45.0%"],
    "Value Bet Rilevata": ["Sì", "No"],
}

df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)

st.info(
    "Copia i dati dei match da Sportalic o inserisci i parametri per aggiornare la scansione in tempo reale."
)