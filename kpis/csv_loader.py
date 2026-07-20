import csv
import io
from pathlib import Path

from .modelos import Campanha

COLUNAS_CSV = ("nome", "gasto", "impressoes", "cliques", "conversoes")

EXEMPLO_CSV = (
    "nome,gasto,impressoes,cliques,conversoes,receita\n"
    "Minha Campanha,1000,50000,1200,30,4500"
)


# padroniza nomes das colunas do csv
def _normalizar_linha(linha: dict[str, str]) -> dict[str, str]:
    return {
        chave.strip().lower(): valor.strip()
        for chave, valor in linha.items()
        if chave and chave.strip()
    }


# le csv em texto e retorna lista de campanhas
def carregar_csv_texto(texto: str) -> list[Campanha]:
    texto = texto.strip()
    if not texto:
        raise ValueError("O arquivo está vazio.")

    primeira_linha = texto.splitlines()[0]
    separador = ";" if ";" in primeira_linha and "," not in primeira_linha else ","

    leitor = csv.DictReader(io.StringIO(texto), delimiter=separador)
    if not leitor.fieldnames:
        raise ValueError("Não foi possível ler o cabeçalho do CSV.")

    colunas = {nome.strip().lower() for nome in leitor.fieldnames if nome}
    faltando = [coluna for coluna in COLUNAS_CSV if coluna not in colunas]
    if faltando:
        raise ValueError(
            "Colunas faltando: "
            + ", ".join(faltando)
            + ". Esperado: nome, gasto, impressoes, cliques, conversoes (receita opcional)"
        )

    campanhas: list[Campanha] = []
    for numero, linha in enumerate(leitor, start=2):
        dados = _normalizar_linha(linha)
        if not dados.get("nome"):
            continue

        try:
            campanhas.append(
                Campanha(
                    nome=dados["nome"],
                    gasto=float(dados["gasto"].replace(",", ".")),
                    impressoes=int(dados["impressoes"]),
                    cliques=int(dados["cliques"]),
                    conversoes=int(dados["conversoes"]),
                    receita=float((dados.get("receita") or "0").replace(",", ".")),
                )
            )
        except (KeyError, ValueError) as erro:
            raise ValueError(f"Erro na linha {numero}: dados inválidos.") from erro

    if not campanhas:
        raise ValueError("Nenhuma campanha encontrada no arquivo.")

    return campanhas


# le csv de um arquivo no disco
def carregar_csv(caminho: Path) -> list[Campanha]:
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    texto = caminho.read_text(encoding="utf-8-sig")
    return carregar_csv_texto(texto)
