from pathlib import Path

from kpis import (
    EXEMPLO_CSV,
    Campanha,
    calcular_kpis,
    carregar_csv,
    comparar_campanhas,
    formatar_relatorio,
    formatar_tabela_comparacao,
)

# caminhos usados pelo programa
PASTA_PROJETO = Path(__file__).parent
ARQUIVO_EXEMPLO = PASTA_PROJETO / "dados" / "exemplo.csv"


# leitura de numeros no terminal
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


# cadastro manual de uma campanha
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


# encontra o arquivo csv no disco
def resolver_caminho(caminho_input: str) -> Path:
    caminho = Path(caminho_input.strip().strip('"'))
    if caminho.exists():
        return caminho

    relativo_projeto = PASTA_PROJETO / caminho
    if relativo_projeto.exists():
        return relativo_projeto

    return caminho


# opcoes do menu
def exibir_menu() -> None:
    print("=" * 40)
    print("  Calculadora de KPIs — Marketing")
    print("=" * 40)
    print("1. Calcular KPI de uma campanha")
    print("2. Carregar campanhas de um CSV")
    print("0. Sair")


# mostra relatorio de uma campanha no terminal
def exibir_campanha(campanha: Campanha) -> None:
    print(formatar_relatorio(campanha, calcular_kpis(campanha)))


# loop principal do terminal
def main() -> None:
    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            exibir_campanha(campanha_manual())

        elif opcao == "2":
            print("\nEnvie um CSV com suas campanhas para calcular os KPIs.")
            print("Exemplo de formato:")
            for linha in EXEMPLO_CSV.splitlines():
                print(linha)
            print("\nA coluna receita é opcional. Separe por vírgula (,) ou ponto-e-vírgula (;).")
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

            tabela = formatar_tabela_comparacao(campanhas)
            if tabela:
                print("\nComparação entre campanhas:")
                for linha in tabela:
                    print(f"  {linha}")

                destaques = comparar_campanhas(campanhas)
                if destaques:
                    print("\nDestaques:")
                    for linha in destaques:
                        print(f"  {linha}")

            for campanha in campanhas:
                exibir_campanha(campanha)

        elif opcao == "0":
            print("\nAté logo!")
            break

        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
