import streamlit as st
import pandas as pd

st.set_page_config(page_title="Master Football Scanner", layout="wide")
st.title("⚽ Master Scanner xG & Over 1.5 (Multi-Campionato)")
st.markdown("Incolla o modifica i dati delle squadre nel box sottostante per calcolare automaticamente il valore Over 1.5 basato su xG e Tiri in Porta.")

# Box di testo per incollare i dati di qualsiasi campionato
raw_data = st.text_area(
    "Dati Squadre (Formato: Squadra | xG For | xG Ag | Tiri in Porta)",
    "Hammarby IF | 1.85 | 0.95 | 6.4\nGAIS | 1.92 | 0.90 | 6.8\nMalmö FF | 2.05 | 1.00 | 7.5\nAIK | 1.35 | 1.20 | 4.5"
)

rows = []
for line in raw_data.split('\n'):
    parts = [p.strip() for p in line.split('|')]
    if len(parts) == 4:
        try:
            rows.append({
                'Squadra': parts[0], 
                'xG For': float(parts[1]), 
                'xG Ag': float(parts[2]), 
                'SoT': float(parts[3])
            })
        except ValueError:
            pass

df = pd.DataFrame(rows) if rows else pd.DataFrame(columns=['Squadra', 'xG For', 'xG Ag', 'SoT'])

if not df.empty:
    st.success(f"Database caricato con successo: {len(df)} squadre pronte.")
    
    c1, c2 = st.columns(2)
    with c1:
        h = st.selectbox("Seleziona Squadra di CASA", df['Squadra'].tolist(), index=0)
    with c2:
        a = st.selectbox("Seleziona Squadra OSPITE", df['Squadra'].tolist(), index=1 if len(df) > 1 else 0)
    
    if st.button("Calcola Matchup e Over 1.5"):
        hr = df[df['Squadra'] == h].iloc[0]
        ar = df[df['Squadra'] == a].iloc[0]
        
        # Calcolo incrociato degli xG stimati del match
        xg_h = (hr['xG For'] + ar['xG Ag']) / 2
        xg_a = (ar['xG For'] + hr['xG Ag']) / 2
        tot_xg = xg_h + xg_a
        
        st.markdown(f"### 📊 Report Analitico: **{h} vs {a}**")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("xG Totali Stimati", f"{tot_xg:.2f}")
            if tot_xg >= 2.65:
                st.success("🔥 **OVER 1.5 / 2.5 CONSIGLIATO (Alta Affidabilità)**")
            else:
                st.info("⚠️ Valore gol moderato (Valutare Under/Cautela)")
        with col_m2:
            combined_sot = (hr['SoT'] + ar['SoT']) / 2
            st.metric("Media Tiri in Porta (SoT) Match", f"{combined_sot:.1f}")
            if combined_sot >= 10.0:
                st.success("🎯 Ottimo volume di tiri nello specchio")
            else:
                st.warning("Volume di tiri nello specchio basso")
                
    st.divider()
    st.subheader("📈 Tabella Database Corrente")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("Inserisci dati validi nel formato corretto.")