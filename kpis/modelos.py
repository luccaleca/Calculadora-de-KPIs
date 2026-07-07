from dataclasses import dataclass


@dataclass
class Campanha:
    nome: str
    gasto: float
    impressoes: int
    cliques: int
    conversoes: int
    receita: float = 0.0


@dataclass
class ResultadoKPI:
    ctr: float
    cpc: float
    cpa: float
    roas: float
    cvr: float
