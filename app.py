import streamlit as st
import fitz
import tempfile
import os

st.set_page_config(page_title="Generador de Specs", layout="centered")

# =========================
# CONFIGURACIÓN
# =========================

PDF_MAESTRO = "HOTSALE_SPECS.pdf"

# Siempre incluir estas páginas
PAGINAS_BASE = list(range(4, 13))  # 4-12

# Patrocinio -> conceptos
# AQUÍ debes ajustar según tu matriz real de la imagen
PATROCINIO_A_CONCEPTOS = {
    "Bronce fijo": [
        "Pauta Digital en Carrusel",
        "Ofertas Hot visibles en sitio",
        "Email Marketing Multimarca",
    ],
    "Bronce rotativo": [
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
    "Luxury": [
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
    "Diamante fijo": [
        "Pauta Digital en Carrusel",
        "Ofertas Hot visibles en sitio",
        "Email Marketing Multimarca",
        "Post exclusivo de marca",
        "Hero Banner Home",
        "Cintillos Home",
    ],
    "Diamante rotativo": [
        "Pauta Digital en Carrusel",
        "Ofertas Hot visibles en sitio",
        "Email Marketing Multimarca",
        "Post exclusivo de marca",
        "Hero Banner Home",
        "Cintillos Home",
    ],
    "Cintillos principales": [
        "Pauta Digital en Carrusel",
        "Ofertas Hot visibles en sitio",
        "Email Marketing Multimarca",
        "Post exclusivo de marca",
        "Hero Banner Home",
        "Cintillos Home",
    ],
    "Landing de categoría": [
        "Ofertas Hot visibles en sitio",
    ],
}

# Concepto -> páginas
# AQUÍ va el cruce del PDF
CONCEPTO_A_PAGINAS = {
    # Conceptos de la imagen
    "Pauta Digital en Carrusel": [49],
    "Ofertas Hot visibles en sitio": [11],
    "Email Marketing Multimarca": [51],
    "Email Marketing Exclusivo de marca": [52],
    "Post exclusivo de marca": [48],

    # Extras / espacios adicionales
    "Mega Ofertas": [15, 16],
    "Mega Ofertas Showroom": [15, 16],
    "Hero Banner Categoría": [31],
    "Hero Banner Home": [28],
    "Cintillos Home": [29],
    "Cintillos Categoría": [32],
    "Cintillos Buscador": [34],
    "Cintillos Cupones": [36],
    "Cintillos Ofertas Flash": [38],
    "Hero Banner Mega Ofertas": [40],
    "Stories": [21],
    "Cupones": [23],
    "Video Shopping": [25],
    "Marca Destacada": [42, 43, 44, 45, 46],
    "Email Marketing Mega Ofertas": [53],
}

EXTRAS_DISPONIBLES = [
    "Mega Ofertas",
    "Mega Ofertas Showroom",
    "Hero Banner Categoría",
    "Hero Banner Home",
    "Cintillos Home",
    "Cintillos Categoría",
    "Cintillos Buscador",
    "Cintillos Cupones",
    "Cintillos Ofertas Flash",
    "Hero Banner Mega Ofertas",
    "Stories",
    "Cupones",
    "Video Shopping",
    "Marca Destacada",
    "Email Marketing Exclusivo de marca",
    "Email Marketing Mega Ofertas",
]

# =========================
# FUNCIONES
# =========================

def obtener_paginas(patrocinio, extras):
    paginas = set(PAGINAS_BASE)

    conceptos = PATROCINIO_A_CONCEPTOS.get(patrocinio, [])
    for concepto in conceptos:
        paginas.update(CONCEPTO_A_PAGINAS.get(concepto, []))

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
# INTERFAZ
# =========================

st.title("Generador de Specs")

if not os.path.exists(PDF_MAESTRO):
    st.error(f"No se encontró el PDF maestro: {PDF_MAESTRO}")
    st.stop()

patrocinio = st.selectbox(
    "Selecciona patrocinio",
    list(PATROCINIO_A_CONCEPTOS.keys())
)

extras = st.multiselect(
    "Selecciona extras opcionales",
    EXTRAS_DISPONIBLES
)

if st.button("Generar PDF"):
    paginas, conceptos = obtener_paginas(patrocinio, extras)

    st.success("PDF generado correctamente")
    st.write("**Patrocinio seleccionado:**", patrocinio)
    st.write("**Conceptos incluidos por patrocinio:**", conceptos)
    st.write("**Extras seleccionados:**", extras if extras else "Ninguno")
    st.write("**Páginas finales:**", paginas)

    pdf_generado = generar_pdf(PDF_MAESTRO, paginas)

    with open(pdf_generado, "rb") as f:
        st.download_button(
            label="Descargar PDF",
            data=f,
            file_name=f"Specs_{patrocinio.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
