import unittest

from kpis import Campanha, calcular_kpis


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


if __name__ == "__main__":
    unittest.main()
