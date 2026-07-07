from pathlib import Path

from kpis import Campanha, calcular_kpis, formatar_relatorio
from kpis.csv_loader import carregar_csv

PASTA_PROJETO = Path(__file__).parent
ARQUIVO_EXEMPLO = PASTA_PROJETO / "dados" / "exemplo.csv"


def ler_float(mensagem: str) -> float:
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print("Valor inválido. Digite um número (ex: 1500 ou 1500,50).")


def ler_int(mensagem: str) -> int:
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Valor inválido. Digite um número inteiro.")


def campanha_manual() -> Campanha:
    print("\n--- Nova campanha ---")
    nome = input("Nome da campanha: ").strip() or "Sem nome"
    gasto = ler_float("Gasto (R$): ")
    impressoes = ler_int("Impressões: ")
    cliques = ler_int("Cliques: ")
    conversoes = ler_int("Conversões: ")
    receita = ler_float("Receita (R$) [0 se não tiver]: ")

    return Campanha(
        nome=nome,
        gasto=gasto,
        impressoes=impressoes,
        cliques=cliques,
        conversoes=conversoes,
        receita=receita,
    )


def resolver_caminho(caminho_input: str) -> Path:
    caminho = Path(caminho_input.strip().strip('"'))
    if caminho.exists():
        return caminho

    relativo_projeto = PASTA_PROJETO / caminho
    if relativo_projeto.exists():
        return relativo_projeto

    return caminho


def exibir_menu() -> None:
    print("=" * 40)
    print("  Calculadora de KPIs — Marketing")
    print("=" * 40)
    print("1. Calcular KPI de uma campanha")
    print("2. Carregar campanhas de um CSV")
    print("0. Sair")


def main() -> None:
    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            campanha = campanha_manual()
            kpis = calcular_kpis(campanha)
            print(formatar_relatorio(campanha, kpis))

        elif opcao == "2":
            caminho_input = input(
                "\nCaminho do CSV [Enter = dados/exemplo.csv]: "
            ).strip()

            if caminho_input:
                caminho = resolver_caminho(caminho_input)
            else:
                caminho = ARQUIVO_EXEMPLO

            try:
                campanhas = carregar_csv(caminho)
            except (FileNotFoundError, ValueError) as erro:
                print(f"\n{erro}")
                continue

            print(f"\nArquivo: {caminho}")
            print(f"{len(campanhas)} campanha(s) carregada(s).")

            for campanha in campanhas:
                kpis = calcular_kpis(campanha)
                print(formatar_relatorio(campanha, kpis))

        elif opcao == "0":
            print("\nAté logo!")
            break

        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
