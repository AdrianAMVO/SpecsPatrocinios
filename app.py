import streamlit as st
from pypdf import PdfReader, PdfWriter
import os

st.title("Prueba de PDF")

st.success("pypdf cargó correctamente")

archivo = "HOTSALE_SPECS.pdf"

if os.path.exists(archivo):
    st.write("PDF encontrado:", archivo)
else:
    st.error("No se encontró HOTSALE_SPECS.pdf")
