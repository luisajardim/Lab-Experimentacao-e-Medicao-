# Lab04 — Testes de Hipótese por Dentro (Pearson × Spearman)

Simulação e visualização para comparar os testes de correlação de **Pearson** e **Spearman**
no cenário **tamanho da classe (LOC) × nº de defeitos**, calibrado com dados reais do
NASA KC1 (C++). A entrega final é um dashboard Streamlit.

> **Pergunta:** Em um sistema C++ da NASA, classes maiores tendem a ter mais defeitos de modo
> geral, ou a associação observada é puxada por poucas classes gigantes?

- **Dashboard:** <https://experimentacao-lab04-spearman.streamlit.app> · ver [Deploy](#deploy-streamlit-community-cloud)
  - página **Dashboard** (padrão): painel só com gráficos e indicadores, como o professor pediu;
  - página **Relatório**: as 7 seções do enunciado (§4) com os textos curtos de cada gráfico, a tabela dos
    dados reais e a conclusão. As duas usam os mesmos gráficos, e o α escolhido vale nas duas.
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
uv run lab04          # comando único: dados → parâmetros → simulação → dashboard
```

Desenvolvimento:

```bash
uv run pytest
uv run ruff check .
uv run python -m data   # (re)gera os CSVs do KC1 em data/real/ (T02)
uv run python -m fit    # (re)ajusta os parâmetros da simulação em data/real/params.json (T03)
uv run python scripts/piloto.py   # piloto Pearson × Spearman em subamostras do KC1 (T03)
uv run python -m simulate         # simulações de Monte Carlo em data/sim/ (~50 s; usa cache) (T08)
uv run python scripts/parquet_to_csv.py   # exporta pvalues.parquet para CSV em data/sim/export/
uv run lab04 --sample-size        # extra opcional: simulação por tamanho de amostra (~75 s; usa cache) (T14)
```

Todas as etapas usam semente fixa (`numpy.random.default_rng(42)`), então os resultados são
reproduzíveis.

**Tempo de execução:** a simulação completa (4 situações × 7 efeitos × 10.000 réplicas = 280.000 conjuntos) leva cerca de **50 s**; com o cache válido, o `uv run lab04` reaproveita os resultados em ~1 s. Formato dos arquivos em [docs/simulacao.md](docs/simulacao.md).

## Deploy (Streamlit Community Cloud)

A porta de entrada é a pasta [`deploy/`](deploy/) (detalhes no README dela). O Cloud não aceita espaço no
caminho do app, então o deploy é feito de um repositório com o conteúdo desta pasta na raiz, não do
repositório da disciplina (que passa por `Enunciado 4/`). Configuração do app:

- **Main file path:** `deploy/streamlit_app.py` · **branch:** `main` · **Python:** 3.12 (em *Advanced settings*)
- **Visibilidade:** pública (*Share → "This app is public and searchable"*); sem isso, quem abre o link cai no login
- **Subdomínio:** `lab-experimentacao-medicao-lab04` (igual a `DASHBOARD_URL` em `src/config.py`)
- Se o `uv.lock` mudar, regenere `deploy/requirements.txt` (o `tests/test_deploy.py` acusa a divergência).

O app só lê arquivos já commitados (`data/real/` e `data/sim/`): nada é simulado no Cloud. A primeira
carga leva ~6 s, a troca de α ~1 s, e o pico de memória fica em ~340 MB.

## Estrutura

```
Enunciado 4/
├── app.py            # app Streamlit: página Dashboard (painel) e menu para a página Relatório
├── deploy/           # porta de entrada e requirements.txt do Streamlit Cloud
├── src/
│   ├── config.py     # semente, caminhos, situações, grade de efeitos, paleta
│   ├── data.py       # coleta do KC1 + amostra de 30 classes
│   ├── fit.py        # ajuste Gamma (LOC) e binomial negativa (defeitos)
│   ├── generate.py   # gerador de dados simulados (cópula gaussiana)
│   ├── stat_tests.py # Pearson e Spearman vetorizados + dados reais
│   ├── simulate.py   # Monte Carlo (Q1, Q2, Q3)
│   ├── relatorio.py  # página Relatório: as 7 seções com textos e tabelas (§4)
│   ├── sample_size.py # extra: poder e erro tipo I × tamanho da amostra
│   ├── figures.py    # gráficos G1–G4
│   └── cli.py        # comando único `lab04`
├── data/
│   ├── real/         # ARFF e CSVs do KC1, params.json e piloto.json
│   └── sim/          # resultados da simulação (pvalues.parquet, summary.csv, population.csv) — ver docs/simulacao.md
├── docs/             # fonte dos dados, cenário, formato da simulação
├── scripts/          # análises auxiliares (piloto nos dados reais)
└── tests/
```

## Regras do grupo

- Todo commit referencia o número da Issue (ex.: `feat(generate): cópula gaussiana #78`).
- Cada integrante é Assignee de ao menos uma Issue com código em cada sprint.
