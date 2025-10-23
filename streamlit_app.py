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
    # FORNECEDOR
    pdf.cell(65, 12, str(row['FORNECEDOR']), align='C', ln=1)
    # MECÂNICA/OBS
    pdf.set_font("Arial", '', 9)
    pdf.cell(65, 7, str(row['MECANICA/OBS']), align='C', ln=1)
    # DESTAQUE: cupom / percentual
    if pd.notna(row['URN']) and len(str(row['URN'])) > 0:
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(0,60,200)
        pdf.cell(65, 15, f"{row['URN']}", align='C', ln=1)
        pdf.set_text_color(0,0,0)
    else:
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(65, 15, f"{str(row['%BENEF'])}", align='C', ln=1)
    pdf.set_font("Arial", '', 8)
    # VIGÊNCIA (local / região)
    pdf.cell(65, 6, str(row['VIGÊNCIA']), align='C', ln=1)
    # AÇÃO (segmento de clientes)
    pdf.cell(65, 6, f"Segmento: {str(row['AÇÃO'])}", align='C', ln=1)
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
        if (i+1) % cards_p_linha == 0:
            x = 10
            y += 110
            if y > 250:
                pdf.add_page()
                y = 20
    return pdf

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Colunas da planilha:", list(df.columns))
    for grupo, grupo_df in df.groupby('GRUPO PRODUTOS'):
        pdf = gerar_pdf(grupo, grupo_df.reset_index())
        buffer = io.BytesIO()
        pdf.output(buffer)
        st.download_button(
            label=f"Baixar PDF [{grupo}]",
            data=buffer.getvalue(),
            file_name=f"{grupo}.pdf",
            mime="application/pdf"
        )
