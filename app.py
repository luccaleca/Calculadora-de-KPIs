import streamlit as st

from kpis.calculos import (
    calcular_kpis,
    comparar_campanhas,
    explicar_kpis,
    formatar_moeda,
    formatar_percentual,
    formatar_roas,
)
from kpis.csv_loader import carregar_csv_texto
from kpis.modelos import Campanha
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

    col1.metric("CTR", formatar_percentual(kpis.ctr))
    col2.metric("CPC", formatar_moeda(kpis.cpc))
    col3.metric("CPA", formatar_moeda(kpis.cpa))

    col4, col5, col6 = st.columns(3)
    col4.metric("ROAS", formatar_roas(kpis.roas))
    col5.metric("CVR", formatar_percentual(kpis.cvr))
    col6.metric("Gasto", formatar_moeda(campanha.gasto))

    with st.expander("Ver contas"):
        for linha in explicar_kpis(campanha, kpis):
            st.write(linha)


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
            texto = arquivo.getvalue().decode("utf-8-sig")
            campanhas = carregar_csv_texto(texto)
            st.success(f"{len(campanhas)} campanha(s) carregada(s).")

            comparacao = comparar_campanhas(campanhas)
            if comparacao:
                st.subheader("Comparação entre campanhas")
                for linha in comparacao:
                    st.write(linha)
                st.divider()

            for campanha in campanhas:
                mostrar_kpis(campanha)
                st.divider()

        except ValueError as erro:
            st.error(str(erro))
