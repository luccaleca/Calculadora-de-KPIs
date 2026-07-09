import unittest
from pathlib import Path

from kpis import Campanha, calcular_kpis, comparar_campanhas, formatar_moeda
from kpis.calculos import explicar_kpis
from kpis.csv_loader import carregar_csv

PASTA_PROJETO = Path(__file__).parent.parent
ARQUIVO_EXEMPLO = PASTA_PROJETO / "dados" / "exemplo.csv"

# testes das formulas de kpi
class TestCalcularKpis(unittest.TestCase):
    def test_black_friday(self):
        campanha = Campanha(
            nome="Black Friday 2025",
            gasto=5000,
            impressoes=100000,
            cliques=2500,
            conversoes=125,
            receita=16000,
        )

        kpis = calcular_kpis(campanha)

        self.assertAlmostEqual(kpis.ctr, 2.5)
        self.assertAlmostEqual(kpis.cpc, 2.0)
        self.assertAlmostEqual(kpis.cpa, 40.0)
        self.assertAlmostEqual(kpis.roas, 3.2)
        self.assertAlmostEqual(kpis.cvr, 5.0)

    def test_divisao_por_zero(self):
        campanha = Campanha(
            nome="Sem dados",
            gasto=100,
            impressoes=0,
            cliques=0,
            conversoes=0,
        )

        kpis = calcular_kpis(campanha)

        self.assertEqual(kpis.ctr, 0.0)
        self.assertEqual(kpis.cpc, 0.0)
        self.assertEqual(kpis.cpa, 0.0)
        self.assertEqual(kpis.cvr, 0.0)


class TestFormatarMoeda(unittest.TestCase):
    def test_valores_comuns(self):
        self.assertEqual(formatar_moeda(2.0), "R$ 2,00")
        self.assertEqual(formatar_moeda(5000), "R$ 5.000,00")
        self.assertEqual(formatar_moeda(0.07), "R$ 0,07")
        self.assertEqual(formatar_moeda(1234567.89), "R$ 1.234.567,89")
        self.assertEqual(formatar_moeda(float("nan")), "R$ 0,00")


class TestExplicarKpis(unittest.TestCase):
    def test_black_friday(self):
        campanha = Campanha(
            nome="Black Friday 2025",
            gasto=5000,
            impressoes=100000,
            cliques=2500,
            conversoes=125,
            receita=16000,
        )
        kpis = calcular_kpis(campanha)
        linhas = explicar_kpis(campanha, kpis)

        self.assertEqual(len(linhas), 10)
        self.assertIn("cliques ÷ 100.000 impressões", linhas[0])
        self.assertIn("% de quem viu o anúncio e clicou", linhas[1])
        self.assertIn("gasto ÷ 2.500 cliques", linhas[2])


class TestCompararCampanhas(unittest.TestCase):
    def test_exemplo_csv(self):
        campanhas = carregar_csv(ARQUIVO_EXEMPLO)
        comparacao = comparar_campanhas(campanhas)

        self.assertEqual(len(comparacao), 5)
        self.assertIn("Remarketing Carrinho", comparacao[3])
        self.assertIn("4,50x", comparacao[3])

    def test_uma_campanha(self):
        campanha = Campanha("Só uma", 100, 1000, 50, 5)
        self.assertEqual(comparar_campanhas([campanha]), [])


if __name__ == "__main__":
    unittest.main()
