import streamlit as st
import pymupdf as fitz
import tempfile
import os

st.set_page_config(page_title="Generador de Specs", layout="centered")

# =========================
# CONFIGURACIÓN
# =========================

PDF_MAESTRO = "HOTSALE_SPECS.pdf"

# Páginas base (SIEMPRE)
PAGINAS_BASE = list(range(4, 13))  # 4–12

# Patrocinio → conceptos
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

# Concepto → páginas
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

# Extras disponibles
EXTRAS_DISPONIBLES = [
    "Mega Ofertas",
    "Hero Banner Categoría",
    "Hero Banner Home",
    "Cintillos Home",
    "Email Marketing Exclusivo de marca",
]

# =========================
# FUNCIONES
# =========================

def obtener_paginas(patrocinio, extras):
    paginas = set(PAGINAS_BASE)

    # Patrocinio
    conceptos = PATROCINIO_A_CONCEPTOS.get(patrocinio, [])
    for concepto in conceptos:
        paginas.update(CONCEPTO_A_PAGINAS.get(concepto, []))

    # Extras
    for extra in extras:
        paginas.update(CONCEPTO_A_PAGINAS.get(extra, []))

    return sorted(paginas), conceptos


def generar_pdf(input_pdf_path, paginas_humanas):
    src = fitz.open(input_pdf_path)
    dst = fitz.open()

    for pagina in paginas_humanas:
        idx = pagina - 1
        if 0 <= idx < len(src):
            dst.insert_pdf(src, from_page=idx, to_page=idx)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    output_path = temp_file.name
    temp_file.close()

    dst.save(output_path)
    dst.close()
    src.close()

    return output_path

# =========================
# UI
# =========================

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
    st.write("Extras:", extras if extras else "Ninguno")
    st.write("Páginas:", paginas)

    pdf_generado = generar_pdf(PDF_MAESTRO, paginas)

    with open(pdf_generado, "rb") as f:
        st.download_button(
            label="Descargar PDF",
            data=f,
            file_name=f"Specs_{patrocinio}.pdf",
            mime="application/pdf"
        )
