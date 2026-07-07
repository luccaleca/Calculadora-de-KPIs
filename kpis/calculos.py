from .modelos import Campanha, ResultadoKPI


def _dividir(numerador: float, denominador: float) -> float:
    if denominador == 0:
        return 0.0
    return numerador / denominador


def calcular_kpis(campanha: Campanha) -> ResultadoKPI:
    return ResultadoKPI(
        ctr=_dividir(campanha.cliques, campanha.impressoes) * 100,
        cpc=_dividir(campanha.gasto, campanha.cliques),
        cpa=_dividir(campanha.gasto, campanha.conversoes),
        roas=_dividir(campanha.receita, campanha.gasto),
        cvr=_dividir(campanha.conversoes, campanha.cliques) * 100,
    )


def formatar_moeda(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_percentual(valor: float) -> str:
    return f"{valor:.2f}%".replace(".", ",")


def formatar_roas(valor: float) -> str:
    return f"{valor:.2f}x".replace(".", ",")


def formatar_relatorio(campanha: Campanha, kpis: ResultadoKPI) -> str:
    linhas = [
        "",
        f"Campanha: {campanha.nome}",
        "-" * 40,
        f"Gasto:       {formatar_moeda(campanha.gasto)}",
        f"Impressões:  {campanha.impressoes:,}".replace(",", "."),
        f"Cliques:     {campanha.cliques:,}".replace(",", "."),
        f"Conversões:  {campanha.conversoes:,}".replace(",", "."),
        f"Receita:     {formatar_moeda(campanha.receita)}",
        "-" * 40,
        f"CTR:  {formatar_percentual(kpis.ctr)}",
        f"CPC:  {formatar_moeda(kpis.cpc)}",
        f"CPA:  {formatar_moeda(kpis.cpa)}",
        f"ROAS: {formatar_roas(kpis.roas)}",
        f"CVR:  {formatar_percentual(kpis.cvr)}",
        "",
    ]
    return "\n".join(linhas)
