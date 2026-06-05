from fpdf import FPDF
from datetime import datetime
import tempfile
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def _generar_grafica_pastel(ingresos: float, egresos: float) -> str:
    fig, ax = plt.subplots(figsize=(5, 4), dpi=150)
    valores = [ingresos, abs(egresos)]
    etiquetas = [f'Ingresos\n${ingresos:,.2f}', f'Egresos\n${abs(egresos):,.2f}']
    colores = ['#4CAF50', '#ea667e']
    _, _, autotexts = ax.pie(
        valores,
        labels=etiquetas,
        colors=colores,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2.5},
        textprops={'fontsize': 10},
        pctdistance=0.75,
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_color('white')
        at.set_fontweight('bold')
    ax.set_title('Ingresos vs Egresos', fontsize=12, fontweight='bold', pad=14)
    fig.patch.set_facecolor('#fafafa')
    fig.tight_layout()
    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    tmp_path = tmp.name
    tmp.close()
    fig.savefig(tmp_path, format='png', bbox_inches='tight', facecolor='#fafafa')
    plt.close(fig)
    return tmp_path


HEADER_H = 36   # altura del banner rosa en mm
TOP_MARGIN = HEADER_H + 8   # margen superior del contenido


class _PDF(FPDF):
    def __init__(self, titulo, fecha):
        super().__init__()
        self._titulo = titulo
        self._fecha = fecha

    def header(self):
        self.set_fill_color(234, 102, 126)
        self.rect(0, 0, 210, HEADER_H, 'F')
        self.set_fill_color(180, 60, 80)
        self.rect(0, 0, 5, HEADER_H, 'F')
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(255, 255, 255)
        self.set_xy(13, 8)
        self.cell(0, 10, self._titulo)
        self.set_font('Helvetica', '', 8.5)
        self.set_text_color(255, 215, 220)
        self.set_xy(13, 23)
        self.cell(0, 7, f'Generado el {self._fecha}')
        # Resetear cursor al margen superior para que el contenido no solape el banner
        self.set_y(self.t_margin)

    def footer(self):
        self.set_y(-13)
        self.set_fill_color(248, 248, 248)
        self.rect(0, self.get_y(), 210, 13, 'F')
        self.set_draw_color(220, 220, 220)
        self.set_line_width(0.3)
        self.line(0, self.get_y(), 210, self.get_y())
        self.set_font('Helvetica', '', 7.5)
        self.set_text_color(180, 180, 180)
        self.cell(0, 10, f'Generado con agentes de IA  \xb7  Pagina {self.page_no()}', align='C')


def txt_a_pdf(texto, titulo="Reporte", ingresos=None, egresos=None):
    fecha = datetime.now().strftime('%d/%m/%Y')
    pdf = _PDF(titulo, fecha)
    # El margen superior hace que cada nueva pagina empiece DEBAJO del header
    pdf.set_margins(left=15, top=TOP_MARGIN, right=15)
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # ── Gráfica de pastel en página 1 ─────────────────────────────────────
    tmp_img = None
    if ingresos is not None and egresos is not None:
        tmp_img = _generar_grafica_pastel(ingresos, egresos)
        img_w = 88
        x_img = (210 - img_w) / 2
        # La imagen va justo debajo del header (y=HEADER_H+2)
        pdf.image(tmp_img, x=x_img, y=HEADER_H + 2, w=img_w)
        # El contenido arranca debajo de la imagen (~68mm de alto)
        pdf.set_y(HEADER_H + 2 + 68)
    # Si no hay gráfica, el margen superior ya posicionó el cursor correctamente

    # ── Limpieza de caracteres especiales ─────────────────────────────────
    reemplazos = {
        '\u2013': '-', '\u2014': '-', '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2022': '-', '\u2026': '...',
        '\u00e1': 'a', '\u00e9': 'e', '\u00ed': 'i', '\u00f3': 'o', '\u00fa': 'u',
        '\u00c1': 'A', '\u00c9': 'E', '\u00cd': 'I', '\u00d3': 'O', '\u00da': 'U',
        '\u00f1': 'n', '\u00d1': 'N', '\u00fc': 'u', '\u00e0': 'a',
    }
    texto_limpio = texto
    for k, v in reemplazos.items():
        texto_limpio = texto_limpio.replace(k, v)
    texto_limpio = (texto_limpio
        .replace('Ejecutivo', '').replace('ejecutivo', '').replace('EJECUTIVO', '')
    )
    texto_limpio = texto_limpio.encode('latin-1', errors='replace').decode('latin-1')

    # ── Constantes de estilo ───────────────────────────────────────────────
    M = 15          # margen izquierdo
    W = 180         # ancho de texto
    LH = 6.5        # line height normal
    C_TEXTO  = (50, 50, 60)
    C_H1     = (150, 40, 65)
    C_H2     = (220, 85, 110)
    C_H3     = (70, 70, 90)
    C_LABEL  = (150, 40, 65)

    en_bloque_codigo = False

    for linea in texto_limpio.split('\n'):
        linea = linea.strip()

        # ── Bloque de código (```): omitir contenido ───────────────────────
        if linea.startswith('```'):
            en_bloque_codigo = not en_bloque_codigo
            continue
        if en_bloque_codigo:
            continue

        # Limpiar asteriscos de negrita antes de cualquier comparación
        linea_clean = linea.replace('**', '').strip()

        # ── Separador --- ══ ───────────────────────────────────────────────
        if linea.startswith('---') or linea.startswith('==='):
            pdf.ln(2)
            pdf.set_draw_color(210, 170, 180)
            pdf.set_line_width(0.25)
            pdf.line(M, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(4)

        # ── Fila de tabla markdown |---| ──────────────────────────────────
        elif linea.startswith('|--') or linea.startswith('|:'):
            pass  # separador de tabla, se omite

        # ── Fila de datos de tabla markdown | col | col | ─────────────────
        elif linea.startswith('|') and linea.endswith('|'):
            celdas = [c.strip() for c in linea.strip('|').split('|')]
            fila = '  |  '.join(c for c in celdas if c)
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(*C_TEXTO)
            pdf.set_x(M)
            pdf.multi_cell(W, 6, fila, align='L')

        # ── H1  # ─────────────────────────────────────────────────────────
        elif linea.startswith('# '):
            pdf.ln(5)
            pdf.set_fill_color(245, 228, 233)
            pdf.set_font('Helvetica', 'B', 14)
            pdf.set_text_color(*C_H1)
            pdf.set_x(M)
            pdf.multi_cell(W, 9, linea_clean[2:], fill=True, align='L')
            pdf.ln(2)

        # ── H2  ## ────────────────────────────────────────────────────────
        elif linea.startswith('## '):
            pdf.ln(5)
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(*C_H2)
            pdf.set_x(M)
            pdf.multi_cell(W, 8, linea_clean[3:], align='L')
            pdf.set_draw_color(*C_H2)
            pdf.set_line_width(0.35)
            pdf.line(M, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(4)

        # ── H3  ### ───────────────────────────────────────────────────────
        elif linea.startswith('### '):
            pdf.ln(4)
            pdf.set_font('Helvetica', 'B', 10.5)
            pdf.set_text_color(*C_H3)
            pdf.set_x(M)
            pdf.multi_cell(W, 7, linea_clean[4:], align='L')
            pdf.ln(1)

        # ── H4  #### ──────────────────────────────────────────────────────
        elif linea.startswith('#### '):
            pdf.ln(3)
            pdf.set_font('Helvetica', 'BI', 10)
            pdf.set_text_color(*C_H3)
            pdf.set_x(M)
            pdf.multi_cell(W, 6.5, linea_clean[5:], align='L')
            pdf.ln(1)

        # ── Bullet  - o * ─────────────────────────────────────────────────
        elif linea.startswith('- ') or linea.startswith('* '):
            contenido = linea_clean[2:]
            pdf.set_text_color(*C_TEXTO)
            pdf.set_font('Helvetica', '', 10)
            pdf.set_x(M + 2)
            pdf.cell(5, LH, '-')
            pdf.set_x(M + 8)
            pdf.multi_cell(W - 8, LH, contenido, align='L')

        # ── Lista numerada  1. 2. 3. ──────────────────────────────────────
        elif len(linea) > 2 and linea[0].isdigit() and linea[1:3] in ('. ', '- '):
            contenido = linea_clean[3:] if linea_clean[2:3] == ' ' else linea_clean[2:]
            pdf.set_text_color(*C_TEXTO)
            pdf.set_font('Helvetica', '', 10)
            pdf.set_x(M + 2)
            num = linea_clean[0]
            pdf.cell(7, LH, f'{num}.')
            pdf.set_x(M + 10)
            pdf.multi_cell(W - 10, LH, contenido, align='L')

        # ── Etiqueta MAYUS: valor ──────────────────────────────────────────
        elif ':' in linea_clean and len(linea_clean) < 120:
            partes = linea_clean.split(':', 1)
            etiqueta = partes[0].strip()
            if etiqueta.replace(' ', '').isupper() and etiqueta and len(partes) == 2:
                pdf.set_x(M)
                pdf.set_font('Helvetica', 'B', 10)
                pdf.set_text_color(*C_LABEL)
                pdf.cell(58, 7, f'{etiqueta}:')
                pdf.set_font('Helvetica', '', 10)
                pdf.set_text_color(*C_TEXTO)
                pdf.multi_cell(W - 58, 7, partes[1].strip(), align='L')
            else:
                pdf.set_font('Helvetica', '', 10)
                pdf.set_text_color(*C_TEXTO)
                pdf.set_x(M)
                pdf.multi_cell(W, LH, linea_clean, align='L')

        # ── Texto normal ───────────────────────────────────────────────────
        elif linea_clean:
            pdf.set_font('Helvetica', '', 10)
            pdf.set_text_color(*C_TEXTO)
            pdf.set_x(M)
            pdf.multi_cell(W, LH, linea_clean, align='L')

        # ── Línea vacía ────────────────────────────────────────────────────
        else:
            pdf.ln(3.5)

    if tmp_img:
        try:
            os.unlink(tmp_img)
        except OSError:
            pass

    return bytes(pdf.output())
