# Calculadora de KPIs

Ferramenta em Python para calcular KPIs de performance de campanhas de marketing digital. Aceita entrada manual, importação de CSV e exibe os resultados via terminal ou interface web (Streamlit).

**Métricas:** CTR, CPC, CPA, ROAS e CVR.
## KPIs calculados

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
├── app.py               # interface web (Streamlit)
├── main.py              # menu interativo (terminal)
├── kpis/
│   ├── modelos.py       # dataclasses Campanha e ResultadoKPI
│   ├── calculos.py      # funções de cálculo e formatação
│   └── csv_loader.py    # leitura de CSV
├── dados/
│   └── exemplo.csv      # campanhas de exemplo
├── tests/
└── requirements.txt
```

## Como rodar

Interface web:

```bash
web
```

Ou dê dois cliques em `web.bat`.

Terminal:

```bash
rodar
```

Ou dê dois cliques em `rodar.bat`.

Se preferir o comando completo:

```bash
python -m streamlit run app.py
python main.py
```

Abre no navegador em `http://localhost:8501`.

## Formato do CSV

Colunas obrigatórias: `nome`, `gasto`, `impressoes`, `cliques`, `conversoes`  
Coluna opcional: `receita`

```csv
nome,gasto,impressoes,cliques,conversoes,receita
Minha Campanha,1000,50000,1200,30,4500
```

## Próximos passos

- [x] Interface web com Streamlit
- [ ] Comparar campanhas e destacar melhores/piores KPIs
- [ ] Relatórios automáticos (PDF/Excel)

