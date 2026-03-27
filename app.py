import streamlit as st

st.title("Generador de Specs")

patrocinio = st.selectbox(
    "Selecciona patrocinio",
    ["Bronce fijo", "Plata", "Oro", "Platino"]
)

if st.button("Generar PDF"):
    st.success(f"Generando specs para: {patrocinio}")
