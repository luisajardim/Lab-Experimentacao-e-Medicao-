# Lab05 — Experimento em Software Real: npm × pnpm × Yarn × Bun

Experimento controlado com gerenciadores de pacotes Node no **Windows 11**, combinado com dados de
operação (séries de downloads da API pública do npm).

> **Pergunta:** quanto tempo e quanto disco cada gerenciador gasta para instalar projetos Node reais
> no Windows? As promessas dos fabricantes se confirmam? A adoção real acompanha o desempenho?

- **Planejamento e tarefas:** [PLAN.md](PLAN.md) · **Enunciado:** [ENUNCIADO.pdf](ENUNCIADO.pdf)
- **Repositório / GitHub Projects:** https://github.com/luisajardim/Lab-Experimentacao-e-Medicao- · board "Kanban Lab" (label `Enunciado 5`)
- **Schema dos dados:** [docs/schema.md](docs/schema.md) · **Registry local:** [docs/registry.md](docs/registry.md) · **Runner:** [docs/runner.md](docs/runner.md)

## Integrantes

- Bernardo Souza Alvim (859148)
- Luísa Oliveira Jardim (843759)
- Pedro Augusto Santos Seabra (812784)

## Pré-requisitos

- [uv](https://docs.astral.sh/uv/) (instala o Python 3.12 automaticamente se necessário)
- Para a coleta (a partir da T02/T04): Node.js e os gerenciadores nas versões do protocolo (T07)

## Como rodar

```bash
cd "Enunciado 5"
uv sync               # instala as dependências
uv run lab05          # comando único: prepara os dados e abre o dashboard
```

Configuração local (opcional): copie `.env.example` para `.env`. Hoje ele só define
`LAB05_WORKDIR`, a pasta de trabalho da coleta (padrão: `.work/`; nunca num `tmpfs` como o `/tmp` do WSL).

Desenvolvimento:

```bash
uv run pytest
uv run ruff check .
uv run lab05 synthetic   # (re)gera o CSV sintético em data/raw/synthetic/ (T01)
uv run lab05 registry up|status|warm|down   # Verdaccio local em http://localhost:4873/ (T02)
uv run lab05 collect --machine <nome> [--pilot] [--dry-run]   # coleta medida (T04)
```

Enquanto não há coleta real, o dashboard e a análise usam o **CSV sintético** (números inventados,
semente fixa), no mesmo formato da coleta. Ver [docs/schema.md](docs/schema.md).

## Estrutura

```
src/        config.py (tratamentos, cenários, projetos, paleta) · schema.py (contrato de runs.csv)
            synthetic.py (CSV sintético) · registry.py (Verdaccio) · runner.py + metrics.py (coleta)
            cli.py (uv run lab05)
app.py      dashboard Streamlit (abas na T10)
projects/   projetos-carga + lockfiles por gerenciador (layout em projects/README.md)
registry/   config do Verdaccio (storage local, não versionado)
data/raw/   <maquina>/runs.csv + specs.json, uma pasta por bloco
docs/       schema, proposta, protocolo, poder, ameaças
tests/      pytest
```
