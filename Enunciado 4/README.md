# Lab04 — Testes de Hipótese por Dentro (Pearson × Spearman)

Simulação e visualização para comparar os testes de correlação de **Pearson** e **Spearman**
no cenário **tamanho da classe (LOC) × nº de defeitos**, calibrado com dados reais do
NASA KC1 (C++). A entrega final é um dashboard Streamlit.

> **Pergunta:** Em um sistema C++ da NASA, classes maiores tendem a ter mais defeitos de modo
> geral, ou a associação observada é puxada por poucas classes gigantes?

- **Dashboard:** _a preencher após o deploy (T07, #82)_
- **Repositório / GitHub Projects:** https://github.com/luisajardim/Lab-Experimentacao-e-Medicao- · board "Kanban Lab"
- **Planejamento:** [PLAN.md](PLAN.md) · **Enunciado:** [ENUNCIADO.pdf](ENUNCIADO.pdf)

## Integrantes

- Bernardo Souza Alvim (859148)
- Luísa Oliveira Jardim (843759)
- Pedro Augusto Santos Seabra (812784)

## Pré-requisitos

- [uv](https://docs.astral.sh/uv/) (instala o Python 3.12 automaticamente se necessário)

## Como rodar

```bash
cd "Enunciado 4"
uv sync               # instala as dependências
uv run lab04          # comando único: dados → parâmetros → simulação → dashboard (implementado em T07, #82)
```

Desenvolvimento:

```bash
uv run pytest
uv run ruff check .
uv run python -m data   # (re)gera os CSVs do KC1 em data/real/ (T02)
```

Todas as etapas usam semente fixa (`numpy.random.default_rng(42)`), então os resultados são
reproduzíveis.

## Estrutura

```
Enunciado 4/
├── app.py            # dashboard Streamlit (7 seções)
├── src/
│   ├── config.py     # semente, caminhos, situações, grade de efeitos, paleta
│   ├── data.py       # coleta do KC1 + amostra de 30 classes
│   ├── fit.py        # ajuste lognormal (LOC) e binomial negativa (defeitos)
│   ├── generate.py   # gerador de dados simulados (cópula gaussiana)
│   ├── stat_tests.py # Pearson e Spearman vetorizados + dados reais
│   ├── simulate.py   # Monte Carlo (Q1, Q2, Q3)
│   ├── figures.py    # gráficos G1–G4
│   └── cli.py        # comando único `lab04`
├── data/
│   ├── real/         # CSVs do KC1 (completo e amostra) + params.json
│   └── sim/          # p-valores das simulações
├── docs/             # fonte dos dados, cenário
└── tests/
```

## Regras do grupo

- Todo commit referencia o número da Issue (ex.: `feat(generate): cópula gaussiana #78`).
- Cada integrante é Assignee de ao menos uma Issue com código em cada sprint.
