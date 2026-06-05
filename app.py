import streamlit as st
from src.bank_statement.crew import BankStatement
import pdfplumber
from utils.pdf import txt_a_pdf

st.set_page_config(
    page_title="Bank Account Analysis",
    layout="centered"
)

# Estilos personalizados
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        
        .hero-banner {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 60px 70px;
            text-align: center;
            margin: -1rem -1rem 2rem -1rem;
        }
        
        .hero-banner h1 {
            color: white;
            font-size: 3em;
            font-weight: 800;
            margin-bottom: 10px;
            letter-spacing: -1px;
        }
        
        .hero-banner p {
            color: rgba(255,255,255,0.85);
            font-size: 1.1em;
            font-weight: 300;
        }

        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 30px;
            font-size: 16px;
            font-weight: 600;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# Hero Banner
st.markdown("""
    <div class='hero-banner'>
        <h1>Bank Statement AI</h1>
        <p><b>Agentes que analizan tu estado de cuenta automáticamente</b></p>
    </div>
""", unsafe_allow_html=True)

# Upload PDF
uploaded_file = st.file_uploader("Sube tu estado de cuenta en PDF", type=["pdf"])

if uploaded_file:
    # Extraer texto del PDF
    with pdfplumber.open(uploaded_file) as pdf:
        texto = ""
        for page in pdf.pages:
            texto += page.extract_text() or ""

    st.success(f"Documento cargado — {len(pdf.pages)} páginas")

    st.divider()

    if st.button("Analizar estado de cuenta"):
        with st.spinner("Los agentes están analizando tu documento..."):
            inputs = {'document': texto}
            try:
                result = BankStatement().crew().kickoff(inputs=inputs)

                st.success("¡Análisis completado!")

                # Mostrar extraccion.txt
                try:
                    with open("extraccion.txt", "r") as f:
                        extraccion = f.read()
                    st.markdown("## Datos Extraídos")
                    st.text(extraccion)
                    st.divider()
                except:
                    pass

                # Mostrar reporte.txt
                try:
                    with open("reporte.txt", "r") as f:
                        reporte = f.read()
                    st.markdown("## Reporte")
                    st.markdown(reporte)
                    st.divider()
                except:
                    pass

                # Descargar PDFs
                col1, col2 = st.columns(2)

                with col1:
                    if extraccion:
                        pdf_extraccion = txt_a_pdf(extraccion, titulo="Reporte de datos Extraídos")
                        st.download_button(
                            label="Descargar Extracción",
                            data=pdf_extraccion,
                            file_name="extraccion.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

                with col2:
                    if reporte:
                        pdf_reporte = txt_a_pdf(reporte, titulo="Reporte Final")
                        st.download_button(
                            label="Descargar Reporte",
                            data=pdf_reporte,
                            file_name="reporte.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

            except Exception as e:
                st.error(f"Ocurrió un error: {str(e)}")
                st.info("Intenta de nuevo en unos segundos.")