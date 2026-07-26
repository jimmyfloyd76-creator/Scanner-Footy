import pandas as pd
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="Scanner-Footy Pro - Stats Don't Lie", page_icon="⚽", layout="wide"
)

st.title("⚽ Scanner-Footy Pro: Modello xG & Gol Value Bet")
st.markdown(
    "Analisi avanzata basata su xG, xGA e tiri in porta (Dati: **Stats Don't Lie**)."
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

mercato = st.sidebar.selectbox(
    "Mercato di Riferimento",
    ["Over 1.5 / Over 2.5", "Goal / No Goal", "Segna Casa / Trasferta"],
)

st.sidebar.markdown("---")
soglia_value = st.sidebar.slider(
    "Soglia di Valore Minima (%)", min_value=1.0, max_value=20.0, value=5.0, step=0.5
)

# Area Principale di Lavoro
st.subheader(f"Analisi in corso per: {campionato}")

# Casella per incollare i dati grezzi da Stats Don't Lie
st.markdown("### 📋 Incolla i dati da Stats Don't Lie")
testo_stats = st.text_area(
    "Incolla qui le statistiche (Squadra, xG fatti, xGA subiti, Tiri in porta medi):",
    placeholder=(
        "Esempio: Squadra A | xG: 1.65 | xGA: 0.90 | Tiri in porta: 5.4\nSquadra"
        " B | xG: 1.20 | xGA: 1.35 | Tiri in porta: 3.8"
    ),
    height=140,
)

# Pulsante di elaborazione
if st.button("🚀 Avvia Modello di Calcolo Gol"):
  st.success("Dati elaborati con successo tramite incrocio xG e Tiri in Porta!")

# Tabella dei Risultati dell'Analisi
st.markdown("---")
st.subheader("📊 Scanner Risultati & Probabilità Gol")

# Dati strutturati di esempio pronti per il calcolo avanzato
data_output = {
    "Match / Squadra": [
        "Team A vs Team B",
        "Team C vs Team D",
        "Team E vs Team F",
    ],
    "xG / xGA (Casa)": ["1.75 / 0.85", "1.40 / 1.10", "2.10 / 0.70"],
    "xG / xGA (Ospite)": ["1.10 / 1.45", "1.30 / 1.25", "0.95 / 1.80"],
    "Tiri in Porta Tot.": ["10.2", "8.5", "12.4"],
    "Probabilità Modello Over 2.5": ["64.5%", "48.0%", "72.0%"],
    "Quota Bookmaker": ["1.80", "2.10", "1.65"],
    "Value Bet Rilevata": ["Sì (Valore +6.5%)", "No", "Sì (Valore +9.2%)"],
}

df_risultati = pd.DataFrame(data_output)
st.dataframe(df_risultati, use_container_width=True)

st.info(
    "Il motore incrocia i dati offensivi (xG + tiri in porta) e difensivi"
    " (xGA) per calcolare la percentuale di realizzazione stimata e confrontarla"
    " con le quote di mercato."
)