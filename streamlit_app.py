import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

st.set_page_config(layout="wide")
st.title("Gerador de Cards de Marketing – PDF automático")

uploaded_file = st.file_uploader("Envie a planilha .xlsx de campanhas")

def cria_card(pdf, row):
    pdf.set_fill_color(255,255,255)  # fundo branco
    pdf.rect(pdf.get_x(), pdf.get_y(), 65, 100, 'F')
    pdf.set_font("Arial", 'B', 14)
    # LOGO (nome do fornecedor)
    pdf.cell(65, 12, str(row['C']), align='C', ln=1)
    # MECÂNICA
    pdf.set_font("Arial", '', 9)
    pdf.cell(65, 7, str(row['I']), align='C', ln=1)
    # DESTAQUE: desconto/percentual
    if pd.notna(row['D']):
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(0,60,200)
        pdf.cell(65, 15, f"{row['D']}", align='C', ln=1)
        pdf.set_text_color(0,0,0)
    else:
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(65, 15, f"{str(row['E'])}", align='C', ln=1)
    pdf.set_font("Arial", '', 8)
    # LOCALIDADES
    pdf.cell(65, 6, str(row['J']), align='C', ln=1)
    # SEGMENTO DE CLIENTES
    pdf.cell(65, 6, f"Clientes: {str(row['K'])}", align='C', ln=1)
    pdf.ln(3)

def gerar_pdf(grupo, dados):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_auto_page_break(auto=False, margin=12)
    x, y = 10, 20
    cards_p_linha = 3
    for i, (_, row) in enumerate(dados.iterrows()):
        pdf.set_xy(x, y)
        cria_card(pdf, row)
        x += 70
        if (i+1)%cards_p_linha == 0:
            x = 10
            y += 110
            if y > 250:
                pdf.add_page()
                y = 20
    return pdf

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    for categoria, grupo_df in df.groupby('CATEGORIAS'):
        pdf = gerar_pdf(categoria, grupo_df.reset_index())
        buf = io.BytesIO()
        pdf.output(buf)
        st.download_button(
            label=f"Baixar PDF [{categoria}]",
            data=buf.getvalue(),
            file_name=f"{categoria}.pdf",
            mime="application/pdf")
