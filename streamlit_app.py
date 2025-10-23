import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

st.title("Gerador de Cards Varejo - Upload, Edição e PDF")

COLS = ["ORDEM", "FORNECEDOR", "CUPOM", "CATEGORIA", "MECANICA", "BENEFICIO", "URN", "CLIENTE"]

if 'df_cards' not in st.session_state:
    st.session_state.df_cards = pd.DataFrame(columns=COLS)

# Upload da planilha
uploaded_file = st.file_uploader("Faça upload da planilha .xlsx", type=['xlsx'])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    missing_cols = [col for col in COLS if col not in df.columns]
    if missing_cols:
        st.error(f"Colunas faltando na planilha: {missing_cols}")
    else:
        st.session_state.df_cards = df[COLS]

if not st.session_state.df_cards.empty:
    st.subheader("Edite os dados, se precisar")
    df_edited = st.data_editor(st.session_state.df_cards, num_rows="dynamic", use_container_width=True)
    st.session_state.df_cards = df_edited

def cria_card(pdf, row):
    pdf.set_fill_color(255,255,255)
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
    dados = dados.sort_values('ORDEM')
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

if st.button("Gerar PDFs agrupados por categoria"):
    if st.session_state.df_cards.empty:
        st.warning("Carregue e revise os dados primeiro.")
    else:
        grupos = st.session_state.df_cards.groupby('CATEGORIA')
        for nome_grupo, grupo_df in grupos:
            pdf = gerar_pdf(nome_grupo, grupo_df)
            buffer = io.BytesIO()
            pdf.output(buffer)
            st.download_button(
                label=f"Baixar PDF [{nome_grupo}]",
                data=buffer.getvalue(),
                file_name=f"{nome_grupo}.pdf",
                mime="application/pdf"
            )
