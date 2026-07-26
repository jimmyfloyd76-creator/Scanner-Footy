import pandas as pd
import streamlit as st

# Configurazione pagina
st.set_page_config(
    page_title="Scanner-Footy Pro - Live Engine",
    page_icon="⚽",
    layout="wide",
)

# Forzatura stili grafici puliti (Tema Scuro)
st.markdown(
    """
    <style>
    .main-title { font-size: 2.2rem; font-weight: 800; color: #38bdf8; text-align: center; }
    .sub-title { text-align: center; color: #9ca3af; margin-bottom: 20px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-title">⚽ SCANNER-FOOTY PRO (Definitive Edition)</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">Inserimento Parametri Reali & Analisi xG</div>',
    unsafe_allow_html=True,
)

# Sidebar per la gestione dati
st.sidebar.header("🎛️ Sorgente Dati")
modalita = st.sidebar.radio(
    "Modalità di inserimento",
    ["Inserimento Manuale Match", "Carica File CSV Personalizzato"],
)

if modalita == "Inserimento Manuale Match":
  st.sidebar.markdown("---")
  st.sidebar.subheader("🏠 Squadra di Casa")
  casa_sel = st.sidebar.text_input("Nome Squadra Casa", "Squadra A")
  xg_fatti_casa = st.sidebar.number_input(
      "xG Fatti (Casa)", 0.0, 5.0, 1.60, 0.05
  )
  xga_subiti_casa = st.sidebar.number_input(
      "xG Subiti (Casa)", 0.0, 5.0, 1.00, 0.05
  )
  tiri_casa = st.sidebar.number_input("Tiri in Porta (Casa)", 0.0, 20.0, 5.0, 0.1)

  st.sidebar.markdown("---")
  st.sidebar.subheader("✈️ Squadra Ospite")
  ospite_sel = st.sidebar.text_input("Nome Squadra Ospite", "Squadra B")
  xg_fatti_ospite = st.sidebar.number_input(
      "xG Fatti (Ospite)", 0.0, 5.0, 1.30, 0.05
  )
  xga_subiti_ospite = st.sidebar.number_input(
      "xG Subiti (Ospite)", 0.0, 5.0, 1.20, 0.05
  )
  tiri_ospite = st.sidebar.number_input(
      "Tiri in Porta (Ospite)", 0.0, 20.0, 4.0, 0.1
  )

  st.sidebar.markdown("---")
  quota_mercato = st.sidebar.number_input(
      "Quota Mercato Over 2.5", 1.01, 10.0, 1.95, 0.05
  )

  # Calcoli analitici
  xg_totale = (
      xg_fatti_casa + xga_subiti_ospite + xg_fatti_ospite + xga_subiti_casa
  ) / 2
  prob_calcolata = min(
      max(
          (xg_totale / 2.7) * 100
          + (tiri_casa + tiri_ospite - 9) * 1.5,
          10.0,
      ),
      95.0,
  )
  quota_equa = round(100 / prob_calcolata, 2)
  edge_valore = round(((prob_calcolata / 100) * quota_mercato - 1) * 100, 1)

  # Layout Principale
  st.subheader(f"⚔️ Match Analizzato: {casa_sel} vs {ospite_sel}")

  col1, col2, col3, col4 = st.columns(4)
  col1.metric("xG Combinati Match", round(xg_totale, 2))
  col2.metric("Probabilità Over 2.5", f"{round(prob_calcolata, 1)}%")
  col3.metric("Quota Equa Calcolata", quota_equa)
  col4.metric(
      "Value / Edge",
      f"+{edge_valore}%" if edge_valore > 0 else f"{edge_valore}%",
      delta="Value Bet" if edge_valore > 3 else "No Value",
  )

  st.markdown("---")
  df_summary = pd.DataFrame({
      "Metrica": ["xG Media Realizzati", "xG Media Subiti", "Tiri in Porta"],
      casa_sel: [xg_fatti_casa, xga_subiti_casa, tiri_casa],
      ospite_sel: [xg_fatti_ospite, xga_subiti_ospite, tiri_ospite],
  })
  st.dataframe(df_summary, use_container_width=True)

  if edge_valore >= 4.0:
    st.success(
        f"🔥 **SEGNALE POSITIVO**: Margine di vantaggio stimato del"
        f" **+{edge_valore}%**."
    )
  else:
    st.info(
        "🛡️ Quota allineata o insufficiente rispetto alle probabilità stimate."
    )

else:
  st.subheader("📁 Caricamento Database Esterno (CSV)")
  st.write(
      "Carica un file CSV contenente le colonne: `Squadra`, `xG_fatti`,"
      " `xGA_subiti`, `tiri_porta`."
  )
  uploaded_file = st.file_uploader("Scegli un file CSV", type=["csv"])
  if uploaded_file is not jamais:
    try:
      df_user = pd.read_csv(uploaded_file)
      st.dataframe(df_user, use_container_width=True)
      st.success("File caricato correttamente!")
    except Exception as e:
      st.error(f"Errore nella lettura del file: {e}")