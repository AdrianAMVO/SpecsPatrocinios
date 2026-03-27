import streamlit as st
from pypdf import PdfReader, PdfWriter
import tempfile
import os

st.set_page_config(page_title="Generador de Specs", layout="centered")

PDF_MAESTRO = "HOTSALE_SPECS.pdf"

# Siempre incluir base
PAGINAS_BASE = list(range(4, 13))  # 4-12

PATROCINIO_A_CONCEPTOS = {
    "Bronce fijo": [
        "Pauta Digital en Carrusel",
        "Ofertas Hot visibles en sitio",
        "Email Marketing Multimarca",
    ],
    "Plata": [
        "Pauta Digital en Carrusel",
        "Ofertas Hot visibles en sitio",
        "Email Marketing Multimarca",
        "Post exclusivo de marca",
    ],
    "Oro": [
        "Pauta Digital en Carrusel",
        "Ofertas Hot visibles en sitio",
        "Email Marketing Multimarca",
        "Post exclusivo de marca",
    ],
    "Platino": [
        "Pauta Digital en Carrusel",
        "Ofertas Hot visibles en sitio",
        "Email Marketing Multimarca",
        "Post exclusivo de marca",
        "Hero Banner Home",
        "Cintillos Home",
    ],
}

CONCEPTO_A_PAGINAS = {
    "Pauta Digital en Carrusel": [49],
    "Ofertas Hot visibles en sitio": [11],
    "Email Marketing Multimarca": [51],
    "Email Marketing Exclusivo de marca": [52],
    "Post exclusivo de marca": [48],
    "Mega Ofertas": [15, 16],
    "Hero Banner Categoría": [31],
    "Hero Banner Home": [28],
    "Cintillos Home": [29],
}

EXTRAS_DISPONIBLES = [
    "Mega Ofertas",
    "Hero Banner Categoría",
    "Hero Banner Home",
    "Cintillos Home",
    "Email Marketing Exclusivo de marca",
]

def obtener_paginas(patrocinio, extras):
    paginas = set(PAGINAS_BASE)

    conceptos = PATROCINIO_A_CONCEPTOS.get(patrocinio, [])
    for concepto in conceptos:
        paginas.update(CONCEPTO_A_PAGINAS.get(concepto, []))

    for extra in extras:
        paginas.update(CONCEPTO_A_PAGINAS.get(extra, []))

    return sorted(paginas), conceptos

def generar_pdf(input_pdf_path, paginas_humanas):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for pagina in paginas_humanas:
        idx = pagina - 1
        if 0 <= idx < len(reader.pages):
            writer.add_page(reader.pages[idx])

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    output_path = temp_file.name
    temp_file.close()

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path

st.title("Generador de Specs")

if not os.path.exists(PDF_MAESTRO):
    st.error(f"No se encontró el PDF: {PDF_MAESTRO}")
    st.stop()

patrocinio = st.selectbox(
    "Selecciona patrocinio",
    list(PATROCINIO_A_CONCEPTOS.keys())
)

extras = st.multiselect(
    "Selecciona extras",
    EXTRAS_DISPONIBLES
)

if st.button("Generar PDF"):
    paginas, conceptos = obtener_paginas(patrocinio, extras)

    st.success("PDF generado")
    st.write("Patrocinio:", patrocinio)
    st.write("Conceptos:", conceptos)
    st.write("Extras:", extras if extras else "Ninguno")
    st.write("Páginas:", paginas)

    pdf_generado = generar_pdf(PDF_MAESTRO, paginas)

    with open(pdf_generado, "rb") as f:
        st.download_button(
            label="Descargar PDF",
            data=f,
            file_name=f"Specs_{patrocinio.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
