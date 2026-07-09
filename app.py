import streamlit as st

from kpis import Campanha, calcular_kpis
from kpis.csv_loader import carregar_csv_texto

# configuracao da pagina
st.set_page_config(page_title="Calculadora de KPIs", layout="centered")

st.title("Calculadora de KPIs")
st.caption("Métricas de campanhas de marketing")

aba_manual, aba_csv = st.tabs(["Uma campanha", "Arquivo CSV"])


# exibe os kpis na tela
def mostrar_kpis(campanha: Campanha) -> None:
    kpis = calcular_kpis(campanha)

    st.subheader(campanha.nome)
    col1, col2, col3 = st.columns(3)

    col1.metric("CTR", f"{kpis.ctr:.2f}%")
    col2.metric("CPC", f"R$ {kpis.cpc:.2f}")
    col3.metric("CPA", f"R$ {kpis.cpa:.2f}")

    col4, col5, col6 = st.columns(3)
    col4.metric("ROAS", f"{kpis.roas:.2f}x")
    col5.metric("CVR", f"{kpis.cvr:.2f}%")
    col6.metric("Gasto", f"R$ {campanha.gasto:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))


# aba para digitar os dados da campanha
with aba_manual:
    nome = st.text_input("Nome da campanha", "Minha campanha")

    col_esq, col_dir = st.columns(2)
    gasto = col_esq.number_input("Gasto (R$)", min_value=0.0, value=1000.0, step=100.0)
    receita = col_dir.number_input("Receita (R$)", min_value=0.0, value=0.0, step=100.0)

    col_esq, col_dir = st.columns(2)
    impressoes = col_esq.number_input("Impressões", min_value=0, value=10000, step=100)
    cliques = col_dir.number_input("Cliques", min_value=0, value=500, step=10)

    conversoes = st.number_input("Conversões", min_value=0, value=25, step=1)

    if st.button("Calcular", type="primary"):
        campanha = Campanha(
            nome=nome,
            gasto=gasto,
            impressoes=impressoes,
            cliques=cliques,
            conversoes=conversoes,
            receita=receita,
        )
        mostrar_kpis(campanha)


# aba para enviar arquivo csv
with aba_csv:
    arquivo = st.file_uploader("Envie um CSV", type=["csv"])

    if arquivo is not None:
        try:
            texto = arquivo.read().decode("utf-8-sig")
            campanhas = carregar_csv_texto(texto)
            st.success(f"{len(campanhas)} campanha(s) carregada(s).")

            for campanha in campanhas:
                mostrar_kpis(campanha)
                st.divider()

        except ValueError as erro:
            st.error(str(erro))
