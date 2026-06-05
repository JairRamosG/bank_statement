from fpdf import FPDF
from datetime import datetime

def txt_a_pdf(texto, titulo="reporte"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    # Header
    pdf.set_fill_color(102, 126, 234)
    pdf.rect(0, 0, 210, 45, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_xy(15, 10)
    pdf.cell(0, 12, titulo)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(15, 28)
    fecha = datetime.now().strftime("%d/%m/%Y")
    pdf.cell(0, 8, f"Generado el {fecha}")
    
    # Contenido
    pdf.set_xy(15, 55)
    
    # Limpiar caracteres especiales
    texto_limpio = (texto
    .replace('–', '-')
    .replace('—', '-')
    .replace('\u2019', "'")
    .replace('\u201c', '"')
    .replace('\u201d', '"')
    .replace('•', '-')  
    .replace('\u2022', '-') 
    .encode('latin-1', errors='replace')
    .decode('latin-1')
)
    for linea in texto_limpio.split('\n'):
        if linea.startswith('# '):
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_text_color(102, 126, 234)
            pdf.set_x(15)
            pdf.multi_cell(180, 9, linea[2:])
            pdf.set_text_color(45, 55, 72)
            pdf.ln(2)
        elif linea.startswith('## '):
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(74, 85, 104)
            pdf.set_x(15)
            pdf.multi_cell(180, 8, linea[3:])
            pdf.set_text_color(45, 55, 72)
            pdf.ln(1)
        elif linea.startswith('### '):
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(45, 55, 72)
            pdf.set_x(15)
            pdf.multi_cell(180, 7, linea[4:])
            pdf.ln(1)
        elif linea.startswith('- ') or linea.startswith('* '):
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(45, 55, 72)
            pdf.set_x(20)
            pdf.multi_cell(175, 6, f"- {linea[2:]}")
        elif linea.strip():
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(45, 55, 72)
            pdf.set_x(15)
            pdf.multi_cell(180, 6, linea)
        else:
            pdf.ln(3)
    
    # Footer
    pdf.set_y(-18)
    pdf.set_fill_color(247, 250, 252)
    pdf.rect(0, pdf.get_y(), 210, 18, 'F')
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(160, 174, 192)
    pdf.set_x(0)
    pdf.cell(0, 10, "Generado por Trip Planner AI", align='C')
    
    return bytes(pdf.output())