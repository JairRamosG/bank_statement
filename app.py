import re
import streamlit as st
from src.bank_statement.crew import BankStatement
import pdfplumber
from utils.pdf import txt_a_pdf
from utils.styles import load_css


def _extraer_monto(texto: str, etiqueta: str):
    patron = rf'{etiqueta}[:\s]+\$?\s*([-\d,\.]+)'
    m = re.search(patron, texto, re.IGNORECASE)
    if m:
        return float(m.group(1).replace(',', ''))
    return None

st.set_page_config(
    page_title="Bank Statement AI",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)

st.markdown("""
    <div class='hero-banner'>
        <h1>Bank Statement AI</h1>
        <p>Agentes inteligentes que analizan tu estado de cuenta automaticamente</p>
    </div>
""", unsafe_allow_html=True)

# Inicializar session_state
if 'extraccion' not in st.session_state:
    st.session_state.extraccion = ""
if 'reporte' not in st.session_state:
    st.session_state.reporte = ""
if 'analizado' not in st.session_state:
    st.session_state.analizado = False

# Layout principal
col_upload, col_info = st.columns([2, 1])

with col_upload:
    uploaded_file = st.file_uploader(
        "Sube tu estado de cuenta en PDF",
        type=["pdf"]
    )

with col_info:
    st.markdown("""
        <div class='info-card'>
            <h4 style='color: #a13246; margin:0 0 10px 0;'>Como funciona</h4>
            <p style='color: #666; font-size: 0.9em; margin:0;'>
                1. Sube tu estado de cuenta en PDF<br>
                2. Los agentes extraen la informacion<br>
                3. Se genera un reporte ejecutivo<br>
                4. Descarga ambos documentos en PDF
            </p>
        </div>
    """, unsafe_allow_html=True)

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        texto = ""
        for page in pdf.pages:
            texto += page.extract_text() or ""
        num_paginas = len(pdf.pages)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Documento", uploaded_file.name)
    with col2:
        st.metric("Paginas", num_paginas)
    with col3:
        st.metric("Caracteres extraidos", f"{len(texto):,}")

    st.divider()

    col_btn, _ = st.columns([1, 2])
    with col_btn:
        analizar = st.button("Analizar estado de cuenta")

    if analizar:
        with st.spinner("Los agentes estan analizando tu documento..."):
            inputs = {'document': texto}
            try:
                BankStatement().crew().kickoff(inputs=inputs)
                st.success("Analisis completado!")

                try:
                    with open("extraccion.txt", "r") as f:
                        st.session_state.extraccion = f.read()
                except:
                    pass

                try:
                    with open("reporte.txt", "r") as f:
                        st.session_state.reporte = f.read()
                except:
                    pass

                st.session_state.analizado = True

            except Exception as e:
                st.error(f"Ocurrio un error: {str(e)}")
                st.info("Intenta de nuevo en unos segundos.")

    # Mostrar resultados si ya se analizo
    if st.session_state.analizado:

        if st.session_state.reporte:
            st.markdown(st.session_state.reporte)
        else:
            st.warning("No se genero el archivo de reporte")

        st.markdown("</div>", unsafe_allow_html=True)

        st.divider()
        st.markdown("### Descargar resultados")
        col1, col2 = st.columns(2)

        with col1:
            if st.session_state.extraccion:
                pdf_extraccion = txt_a_pdf(
                    st.session_state.extraccion,
                    titulo="Datos Extraidos"
                )
                st.download_button(
                    label="Descargar Extraccion PDF",
                    data=pdf_extraccion,
                    file_name="extraccion.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

        with col2:
            if st.session_state.reporte:
                ingresos = _extraer_monto(st.session_state.extraccion, "ENTRADAS TOTALES")
                egresos = _extraer_monto(st.session_state.extraccion, "SALIDAS TOTALES")
                pdf_reporte = txt_a_pdf(
                    st.session_state.reporte,
                    titulo="Reporte",
                    ingresos=ingresos,
                    egresos=egresos,
                )
                st.download_button(
                    label="Descargar Reporte PDF",
                    data=pdf_reporte,
                    file_name="reporte.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
