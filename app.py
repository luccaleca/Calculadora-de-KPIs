import streamlit as st

from kpis.calculos import (
    calcular_kpis,
    explicar_kpis,
    formatar_moeda,
    formatar_percentual,
    formatar_roas,
    montar_tabela_comparacao,
    montar_tabela_dados,
)
from kpis.csv_loader import carregar_csv_texto
from kpis.modelos import Campanha
# configuracao da pagina
st.set_page_config(page_title="Calculadora de KPIs", layout="centered")

st.title("Calculadora de KPIs")
st.caption("Métricas de campanhas de marketing")

aba_manual, aba_csv = st.tabs(["Uma campanha", "Arquivo CSV"])

_CONFIG_DADOS = {
    "Campanha": st.column_config.TextColumn("Campanha"),
    "Gasto": st.column_config.NumberColumn("Gasto (R$)", format="%.2f"),
    "Impressões": st.column_config.NumberColumn("Impressões", format="%d"),
    "Cliques": st.column_config.NumberColumn("Cliques", format="%d"),
    "Conversões": st.column_config.NumberColumn("Conversões", format="%d"),
    "Receita": st.column_config.NumberColumn("Receita (R$)", format="%.2f"),
}

_CONFIG_COMPARACAO = {
    "Campanha": st.column_config.TextColumn("Campanha"),
    "CTR": st.column_config.NumberColumn("CTR (%)", format="%.2f"),
    "CPC": st.column_config.NumberColumn("CPC (R$)", format="%.2f"),
    "CPA": st.column_config.NumberColumn("CPA (R$)", format="%.2f"),
    "ROAS": st.column_config.NumberColumn("ROAS (x)", format="%.2f"),
    "CVR": st.column_config.NumberColumn("CVR (%)", format="%.2f"),
}


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

            st.subheader("Dados carregados")
            st.dataframe(
                montar_tabela_dados(campanhas),
                column_config=_CONFIG_DADOS,
                hide_index=True,
                use_container_width=True,
            )

            comparacao = montar_tabela_comparacao(campanhas)
            if comparacao:
                st.subheader("Comparação entre campanhas")
                st.dataframe(
                    comparacao,
                    column_config=_CONFIG_COMPARACAO,
                    hide_index=True,
                    use_container_width=True,
                )

            st.divider()
            st.subheader("KPIs por campanha")

            for campanha in campanhas:
                mostrar_kpis(campanha)
                st.divider()

        except ValueError as erro:
            st.error(str(erro))
