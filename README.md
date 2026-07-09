# Calculadora de KPIs

Ferramenta em Python para calcular KPIs de campanhas de marketing digital.

**Métricas:** CTR, CPC, CPA, ROAS e CVR.

| KPI | Fórmula |
|-----|---------|
| CTR | cliques ÷ impressões × 100 |
| CPC | gasto ÷ cliques |
| CPA | gasto ÷ conversões |
| ROAS | receita ÷ gasto |
| CVR | conversões ÷ cliques × 100 |

## Estrutura

```
Calculadora_KPIS/
├── app.py          # interface web
├── main.py         # interface terminal
├── kpis/           # calculos, modelos e leitura de csv
├── dados/          # csv de exemplo
├── tests/
├── web.bat         # atalho para abrir a web
└── rodar.bat       # atalho para o terminal
```

`app.py` e `main.py` são só a interface. A lógica fica em `kpis/`.

## Instalação

```bash
python -m pip install -r requirements.txt
```

## Como rodar

**Web** (recomendado) — abre em `http://localhost:8501`:

```bash
web.bat
```

**Terminal** — menu interativo no console:

```bash
rodar.bat
```

## CSV

Colunas obrigatórias: `nome`, `gasto`, `impressoes`, `cliques`, `conversoes`  
Coluna opcional: `receita`

```csv
nome,gasto,impressoes,cliques,conversoes,receita
Minha Campanha,1000,50000,1200,30,4500
```

No terminal, opção `2` pede o caminho do arquivo. Na web, use a aba **Arquivo CSV**.

## Testes

```bash
python -m unittest discover -s tests -v
```

## Próximos passos

- [x] Interface web com Streamlit
- [ ] Comparar campanhas e destacar melhores/piores KPIs
- [ ] Relatórios automáticos (PDF/Excel)
