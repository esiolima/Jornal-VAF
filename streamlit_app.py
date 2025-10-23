import streamlit as st
from fpdf import FPDF
import io
import pandas as pd

st.title("Gerador Manual de Cards Marketing")

# Usar sessão para armazenar os cards criados
if 'cards' not in st.session_state:
    st.session_state.cards = []

with st.form("form-card"):
    ordem = st.number_input("ORDEM", min_value=1, step=1)
    fornecedor = st.text_input("FORNECEDOR")
    cupom = st.text_input("CUPOM")
    categoria = st.text_input("CATEGORIA")
    mecanica = st.text_area("MECANICA")
    beneficio = st.text_input("BENEFICIO")
    urn = st.text_input("URN (texto pequeno)")
    cliente = st.text_input("CLIENTE")
    submitted = st.form_submit_button("Adicionar Card")

if submitted:
    st.session_state.cards.append({
        'ORDEM': ordem,
        'FORNECEDOR': fornecedor,
        'CUPOM': cupom,
        'CATEGORIA': categoria,
        'MECANICA': mecanica,
        'BENEFICIO': beneficio,
        'URN': urn,
        'CLIENTE': cliente
    })
    st.success("Card adicionado!")

def cria_card(pdf, row):
    pdf.set_fill_color(255,255,255)  # fundo branco
    pdf.rect(pdf.get_x(), pdf.get_y(), 65, 100, 'F')
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(65, 12, str(row['FORNECEDOR']), align='C', ln=1)
    pdf.set_font("Arial", '', 9)
    pdf.cell(65, 7, str(row['MECANICA']), align='C', ln=1)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0,60,200)
    pdf.cell(65, 15, str(row['BENEFICIO']), align='C', ln=1)
    pdf.set_text_color(0,0,0)
    pdf.set_font("Arial", '', 8)
    pdf.cell(65, 5, str(row['URN']), align='C', ln=1)
    pdf.cell(65, 6, f"Segmento: {str(row['CLIENTE'])}", align='C', ln=1)
    pdf.ln(3)

def gerar_pdf(grupo, dados):
    dados = sorted(dados, key=lambda x: x['ORDEM'])
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_auto_page_break(auto=False, margin=12)
    x, y = 10, 20
    cards_p_linha = 3
    for i, row in enumerate(dados):
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

if st.session_state.cards:
    st.subheader("Cards criados")
    for c in st.session_state.cards:
        st.write(f"{c['ORDEM']} - {c['FORNECEDOR']} - {c['CATEGORIA']}")

    grupo_categorias = {}
    for c in st.session_state.cards:
        grupo_categorias.setdefault(c['CATEGORIA'], []).append(c)

    for grupo, lista in grupo_categorias.items():
        pdf = gerar_pdf(grupo, lista)
        buf = io.BytesIO()
        pdf.output(buf)
        st.download_button(
            label=f"Baixar PDF [{grupo}]",
            data=buf.getvalue(),
            file_name=f"{grupo}.pdf",
            mime="application/pdf"
        )
