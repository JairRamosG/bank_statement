import streamlit as st
from src.bank_statement.crew import BankStatement
import pdfplumber
from utils.pdf import txt_a_pdf

st.set_page_config(
    page_title="Bank Statement AI",
    layout="wide"
)

st.markdown("""
    <style>
        .main { background-color: #fafafa; }
        
        .hero-banner {
            background: linear-gradient(135deg, #ea667e 0%, #a13246 100%);
            padding: 50px 70px;
            text-align: center;
            margin: -1rem -1rem 2rem -1rem;
            border-radius: 0 0 20px 20px;
            box-shadow: 0 4px 20px rgba(161, 50, 70, 0.3);
        }
        
        .hero-banner h1 {
            color: white;
            font-size: 2.8em;
            font-weight: 800;
            margin-bottom: 8px;
            letter-spacing: -1px;
        }
        
        .hero-banner p {
            color: rgba(255,255,255,0.9);
            font-size: 1.1em;
            font-weight: 300;
            margin: 0;
        }

        .info-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            border-left: 4px solid #ea667e;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            margin-bottom: 15px;
        }

        .stButton > button {
            background: linear-gradient(135deg, #ea667e 0%, #a13246 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 14px 30px;
            font-size: 16px;
            font-weight: 600;
            width: 100%;
        }

        .stDownloadButton > button {
            background: white;
            color: #a13246;
            border: 2px solid #ea667e;
            border-radius: 10px;
            font-weight: 600;
        }

        .stDownloadButton > button:hover {
            background: #ea667e;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='hero-banner'>
        <h1>Bank Statement AI</h1>
        <p>Agentes inteligentes que analizan tu estado de cuenta automáticamente</p>
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

    # Mostrar resultados si ya se analizó
    if st.session_state.analizado:

        tab1, tab2 = st.tabs(["Datos Extraidos", "Reporte Ejecutivo"])

        with tab1:
            if st.session_state.extraccion:
                st.text(st.session_state.extraccion)
            else:
                st.warning("No se genero el archivo de extraccion")

        with tab2:
            if st.session_state.reporte:
                st.markdown(st.session_state.reporte)
            else:
                st.warning("No se genero el archivo de reporte")

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
                pdf_reporte = txt_a_pdf(
                    st.session_state.reporte,
                    titulo="Reporte Ejecutivo"
                )
                st.download_button(
                    label="Descargar Reporte PDF",
                    data=pdf_reporte,
                    file_name="reporte.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )