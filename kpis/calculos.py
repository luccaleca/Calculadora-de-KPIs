from .modelos import Campanha, ResultadoKPI


# divisao segura (retorna 0 se denominador for 0)
def _dividir(numerador: float, denominador: float) -> float:
    if denominador == 0:
        return 0.0
    return numerador / denominador


# calcula ctr, cpc, cpa, roas e cvr
def calcular_kpis(campanha: Campanha) -> ResultadoKPI:
    return ResultadoKPI(
        ctr=_dividir(campanha.cliques, campanha.impressoes) * 100,
        cpc=_dividir(campanha.gasto, campanha.cliques),
        cpa=_dividir(campanha.gasto, campanha.conversoes),
        roas=_dividir(campanha.receita, campanha.gasto),
        cvr=_dividir(campanha.conversoes, campanha.cliques) * 100,
    )


# formata moeda, percentual e roas para o terminal
def formatar_moeda(valor: float) -> str:
    if valor != valor:
        return "R$ 0,00"

    sinal = "-" if valor < 0 else ""
    valor = abs(valor)
    texto = f"{valor:.2f}"

    if "." not in texto:
        return f"{sinal}R$ 0,00"

    inteiro, centavos = texto.split(".")
    inteiro_formatado = f"{int(inteiro):,}".replace(",", ".")
    return f"{sinal}R$ {inteiro_formatado},{centavos}"


def formatar_percentual(valor: float) -> str:
    if valor != valor:
        return "0,00%"

    return f"{valor:.2f}%".replace(".", ",")


def formatar_roas(valor: float) -> str:
    if valor != valor:
        return "0,00x"

    return f"{valor:.2f}x".replace(".", ",")


def _fmt_int(valor: int) -> str:
    return f"{valor:,}".replace(",", ".")


# mostra a conta usada em cada kpi
def explicar_kpis(campanha: Campanha, kpis: ResultadoKPI) -> list[str]:
    imp = _fmt_int(campanha.impressoes)
    cli = _fmt_int(campanha.cliques)
    conv = _fmt_int(campanha.conversoes)
    gasto = formatar_moeda(campanha.gasto)
    receita = formatar_moeda(campanha.receita)
    linhas: list[str] = []

    if campanha.impressoes == 0:
        ctr = f"CTR:  sem impressões = {formatar_percentual(kpis.ctr)}"
    else:
        ctr = (
            f"CTR:  {cli} cliques ÷ {imp} impressões × 100 "
            f"= {formatar_percentual(kpis.ctr)}"
        )
    linhas.append(ctr)
    linhas.append("      % de quem viu o anúncio e clicou")

    if campanha.cliques == 0:
        cpc = f"CPC:  sem cliques = {formatar_moeda(kpis.cpc)}"
    else:
        cpc = f"CPC:  {gasto} gasto ÷ {cli} cliques = {formatar_moeda(kpis.cpc)}"
    linhas.append(cpc)
    linhas.append("      quanto você pagou por cada clique")

    if campanha.conversoes == 0:
        cpa = f"CPA:  sem conversões = {formatar_moeda(kpis.cpa)}"
    else:
        cpa = f"CPA:  {gasto} gasto ÷ {conv} conversões = {formatar_moeda(kpis.cpa)}"
    linhas.append(cpa)
    linhas.append("      quanto você pagou por cada conversão")

    if campanha.gasto == 0:
        roas = f"ROAS: sem gasto = {formatar_roas(kpis.roas)}"
    else:
        roas = f"ROAS: {receita} receita ÷ {gasto} gasto = {formatar_roas(kpis.roas)}"
    linhas.append(roas)
    linhas.append("      quanto voltou em receita para cada R$ 1 gasto")

    if campanha.cliques == 0:
        cvr = f"CVR:  sem cliques = {formatar_percentual(kpis.cvr)}"
    else:
        cvr = (
            f"CVR:  {conv} conversões ÷ {cli} cliques × 100 "
            f"= {formatar_percentual(kpis.cvr)}"
        )
    linhas.append(cvr)
    linhas.append("      % de cliques que viraram conversão")

    return linhas


# compara campanhas e destaca melhores kpis
def comparar_campanhas(campanhas: list[Campanha]) -> list[str]:
    if len(campanhas) < 2:
        return []

    resultados = [(campanha, calcular_kpis(campanha)) for campanha in campanhas]

    def melhor_maior(campo: str, rotulo: str, formatar) -> str:
        campanha, kpis = max(resultados, key=lambda item: getattr(item[1], campo))
        return f"Melhor {rotulo}: {campanha.nome} ({formatar(getattr(kpis, campo))})"

    def melhor_menor(campo: str, rotulo: str, formatar) -> str:
        campanha, kpis = min(resultados, key=lambda item: getattr(item[1], campo))
        return f"Menor {rotulo}: {campanha.nome} ({formatar(getattr(kpis, campo))})"

    return [
        melhor_maior("ctr", "CTR", formatar_percentual),
        melhor_menor("cpc", "CPC", formatar_moeda),
        melhor_menor("cpa", "CPA", formatar_moeda),
        melhor_maior("roas", "ROAS", formatar_roas),
        melhor_maior("cvr", "CVR", formatar_percentual),
    ]


# monta o relatorio completo da campanha
def formatar_relatorio(campanha: Campanha, kpis: ResultadoKPI) -> str:
    linhas = [
        "",
        f"Campanha: {campanha.nome}",
        "-" * 40,
        f"Gasto:       {formatar_moeda(campanha.gasto)}  (investido em anúncios)",
        f"Impressões:  {campanha.impressoes:,}".replace(",", ".") + "  (vezes que o anúncio apareceu)",
        f"Cliques:     {campanha.cliques:,}".replace(",", ".") + "  (cliques no anúncio)",
        f"Conversões:  {campanha.conversoes:,}".replace(",", ".") + "  (compras, cadastros, etc.)",
        f"Receita:     {formatar_moeda(campanha.receita)}  (dinheiro gerado)",
        "-" * 40,
        f"CTR:  {formatar_percentual(kpis.ctr)}",
        f"CPC:  {formatar_moeda(kpis.cpc)}",
        f"CPA:  {formatar_moeda(kpis.cpa)}",
        f"ROAS: {formatar_roas(kpis.roas)}",
        f"CVR:  {formatar_percentual(kpis.cvr)}",
        "",
        "Como foi calculado:",
    ]
    linhas.extend(f"  {linha}" for linha in explicar_kpis(campanha, kpis))
    linhas.append("")
    return "\n".join(linhas)
