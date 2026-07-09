from dataclasses import dataclass


# dados de entrada de uma campanha
@dataclass
class Campanha:
    nome: str
    gasto: float
    impressoes: int
    cliques: int
    conversoes: int
    receita: float = 0.0


# resultado dos calculos de kpi
@dataclass
class ResultadoKPI:
    ctr: float
    cpc: float
    cpa: float
    roas: float
    cvr: float
