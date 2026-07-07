import unittest
from pathlib import Path

from kpis.csv_loader import carregar_csv

PASTA_PROJETO = Path(__file__).parent.parent
ARQUIVO_EXEMPLO = PASTA_PROJETO / "dados" / "exemplo.csv"


class TestCarregarCsv(unittest.TestCase):
    def test_exemplo_csv(self):
        campanhas = carregar_csv(ARQUIVO_EXEMPLO)

        self.assertEqual(len(campanhas), 4)
        self.assertEqual(campanhas[0].nome, "Black Friday 2025")
        self.assertEqual(campanhas[0].gasto, 5000)

    def test_arquivo_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            carregar_csv(PASTA_PROJETO / "dados" / "nao_existe.csv")


if __name__ == "__main__":
    unittest.main()
