# PLAN.md — Lab03: Mineração de Métricas DORA

> Protótipo de kanban e documento de referência para o grupo (Alvim, Luísa, Pedro).
> **Status:** passível de mudanças — editar via Issues do GitHub Projects.

---

## Visão geral

| Item | Valor |
|---|---|
| **Grupo** | Bernardo Alvim (A), Luísa Jardim (B), Pedro Seabra (C) |
| **Janela** | 2025-10-01 → 2026-09-30 (configurável em `config.toml`) |
| **Stack** | Python 3.12 + uv · httpx · SQLite · pandas/scipy/statsmodels/sklearn/pymannkendall/matplotlib · pytest + pytest-cov + ruff |
| **Repositório** | `Enunciado 3/` |
| **Entrada única** | `python -m pipeline --config config.toml` |
| **CI** | GitHub Actions do próprio grupo (matrix 3.12/3.13 + smoke test com `--limit 2`) |

---

## Kanban por sprint (S01 → Final)

| Sprint | Membro A | Membro B | Membro C |
|---|---|---|---|
| **S01** (5 pt) | Seleção, funil, coleta de metadados, GraphQL batch + rate budget | Coleta releases/tags/commits + funções + testes de lead time | Workflow runs (divisão mensal) + CFR(a) + recovery + pytest + CI do grupo |
| **S02** (5 pt) | Amostra-ouro 60 repos + gerador de planilha + rótulo independente | Heurística CFR(b): v1→F1 ≥ 0,70 + precisão/recall + consenso | Pipeline 300+ repos + dicionário de dados + diff-datasets + dataset para S03 |
| **S03** (5 pt) | RQ01-RQ04 + classificação DORA C1 + Kaplan-Meier + bootstrap BCa | RQ05 + RQ06 (Spearman, Kruskal-Wallis/Mann-Whitney, Holm, Cliff's delta, Dunn post-hoc) | RQ07 (C1×C2×C3 + κ ponderado) + RQ08 (rework rate + Mann-Kendall) + relatório auto-gerado |
| **Final** (5 pt) | Executar pipeline do outro grupo + checklist de travas | Comparar CSV + abrir Issues de divergência | Responder Issues + ajustar pipeline + ameaças à validade + revisão final do artigo |

> Papéis são uma **proposta**. Ajustes via Issues com `Assignee` por integrante.

---

## Tarefas detalhadas

### S01 — Pipeline base

#### T01 Scaffold
- *Objetivo:* Criar estrutura base do projeto Python com layout padrão, dependências e CI.
- *Regras de negócio / restrições:*
  - Layout: `src/pipeline/`, `src/metrics/`, `tests/`, `scripts/`, `data/`, `config.toml`.
  - Não commitar `data/cache/` nem `.env` (nem `.env.example` com valores reais).
  - Python 3.12 mínimo; usar `uv` como gerenciador de ambientes e lock file.
- *Critérios de aceitação:*
  - `uv sync` instala dependências sem erros.
  - `uv run pytest --collect-only` descobre testes.
  - `.github/workflows/testes.yml` existe, é válido e aponta para Python 3.12.
- *Implementação:* Criar diretórios, `pyproject.toml` com `[project]`, `[tool.ruff]`, `[tool.pytest.ini_options]`. `.gitignore` padrão Python. `README.md` com pré-requisitos, variáveis e comando de início.
- *Dependências:* Nenhuma.

#### T02 Cliente GitHub
- *Objetivo:* Camada de acesso à API GitHub (GraphQL em lote + REST paginada) sem bibliotecas prontas.
- *Regras de negócio / restrições:*
  - **Proibido** usar PyGithub/Octokit ou qualquer cliente de terceiro para GitHub.
  - GraphQL deve usar aliases para múltiplas queries em uma requisição (lote), reduzindo round-trips.
  - REST deve seguir o cabeçalho `Link: rel="next"` para paginação.
  - Backoff exponencial em erros 429/5xx: esperas de 1s, 2s, 4s, 8s; máximo 5 tentativas.
  - Respeitar `X-RateLimit-Remaining`/`X-RateLimit-Reset`: pausar execução até o reset quando a cota acabar.
- *Critérios de aceitação:*
  - Consulta de teste retorna dados válidos.
  - `GET /rate_limit` funciona e registra cota atual.
  - Retry automático em 429 e 5xx.
- *Implementação:* `src/github/gql.py` (batch com aliases), `src/github/rest.py` (paginação, tratamento de headers), `src/github/models.py` (dataclasses para `Repository`, `Release`, `WorkflowRun`, `Commit`).
- *Dependências:* T01.

#### T03 Cache SQLite + staleness
- *Objetivo:* Persistir respostas da API em disco para retomada e redução de quota.
- *Regras de negócio / restrições:*
  - Content-addressed: chave = hash do método + URL + body (se aplicável).
  - Tabela `responses(url_hash, url, method, body, status, response_body, fetched_at)`.
  - `staleness_report.json` por stage com `stale_count` (repos que mudaram desde a última coleta).
  - Retomada por stage: se stage `collect` foi completado com sucesso, não repetir chamadas desse stage.
  - Nunca commitar `data/cache/`.
- *Critérios de aceitação:*
  - Interromper e retomar não repete requests já concluídos.
  - Relatório de staleness correto após nova execução.
- *Implementação:* `src/cache/sqlite_store.py` com métodos `get`, `put`, `get_stale`, `clear_stage`.
- *Dependências:* T02.

#### T04 Seleção de candidatos
- *Objetivo:* Buscar repositórios candidatos respeitando o limite de 1.000 resultados por query.
- *Regras de negócio / restrições:*
  - Fatiar busca por faixa de estrelas: `stars:1000..2000`, `stars:2000..5000`, etc.
  - Opcionalmente fatiar por linguagem principal.
  - Parar ao atingir `max_candidates` configurado em `config.toml`.
  - Registrar a `query` usada em `meta/search_queries/`.
- *Critérios de aceitação:*
  - CSV `data/raw/candidates.csv` com `full_name`, `stars`, `language`, `default_branch`, `created_at`.
  - Nenhuma query retorna mais de 1.000 itens sem paginação.
- *Implementação:* `src/collector/search.py`. Usar REST `GET /search/repositories`.
- *Dependências:* T02, T03.

#### T05 Releases, Tags e Commits
- *Objetivo:* Coletar releases válidas, tags e commits entre releases consecutivas.
- *Regras de negócio / restrições:*
  - Releases: filtrar `draft=false`, ordenar por `published_at`. Pré-releases entram só como variante C2/C3.
  - Tags: se não houver release anterior, coletar tags e usar a data do commit apontado.
  - Commits: endpoint `compare/{base}...{head}` paginando `per_page=250`. Registrar casos de 404 (tag apagada ou reescrita) para métrica de lead time.
- *Critérios de aceitação:*
  - JSON por repo com `releases[]`, `tags[]`, `commits_between[]`.
  - Release sem commits anteriores é registrada e ignorada no cálculo de lead time.
- *Implementação:* `src/collector/releases.py`, `src/collector/tags.py`, `src/collector/commits.py`.
- *Dependências:* T02, T03.

#### T06 Workflow runs
- *Objetivo:* Coletar execuções de CI/CD do default branch disparadas por push.
- *Regras de negócio / restrições:*
  - Divisão mensal da janela para não estourar limite de 1.000 por query.
  - Filtros obrigatórios: `branch={default_branch}`, `event=push`.
  - Ignorar conclusões `cancelled`, `skipped`, `neutral`, `action_required`, `stale` e vazio.
  - Registrar total de runs por mês para auditoria.
- *Critérios de aceitação:*
  - JSON por repo por mês com apenas runs válidos.
  - Nenhum mês ultrapassa 1.000 resultados sem paginação.
- *Implementação:* `src/collector/runs.py`.
- *Dependências:* T02, T03, T04.

#### T07 Métricas puras (lead time, CFR, recovery)
- *Objetivo:* Funções puras para cálculo das métricas, sem I/O, prontas para teste.
- *Regras de negócio / restrições:*
  - Lead time (a): por release = `published_at - oldest_commit_in_release`.
  - Lead time (b): por commit = mediana de todos os commits de todas as releases.
  - CFR(a) = `failures / (failures + successes)` por repo.
  - Recovery: episódio começa na primeira falha após sucesso e termina no próximo sucesso. Tempo = `updated_at_success - run_started_at_first_failure`.
  - Casos de borda obrigatórios: release sem commits novos, falha censurada (fim fora da janela), runs `cancelled` (ignorados), repo com 1 release.
- *Critérios de aceitação:*
  - Fixtures com exemplos numéricos do enunciado passam.
  - Cobertura ≥ 80% do módulo `metrics/`.
- *Implementação:* `metrics/lead_time.py`, `metrics/cfr.py`, `metrics/recovery.py`. Fixtures em `tests/fixtures/`.
- *Dependências:* T05, T06.

#### T08 CLI
- *Objetivo:* Interface de entrada única para todo o pipeline.
- *Regras de negócio / restrições:*
  - Ler configuração de `config.toml`.
  - Token via variável de ambiente `GITHUB_TOKEN` (nunca committado).
  - Subcomandos: `collect`, `metrics`, `report`.
  - Flag `--limit N` para smoke tests.
  - Logging estruturado (nível INFO por padrão, DEBUG com flag).
- *Critérios de aceitação:*
  - `python -m pipeline --help` exibe ajuda.
  - `collect --limit 2` baixa e processa 2 repositórios.
  - Saída de erro é amigável quando token está faltando.
- *Implementação:* `pipeline/cli.py` com `typer` ou `argparse`.
- *Dependências:* T01, T03, T07.

#### T09 CI do grupo
- *Objetivo:* Testes automáticos no GitHub Actions do próprio grupo.
- *Regras de negócio / restrições:*
  - Matrix: Python 3.12 e 3.13.
  - `pytest --cov=metrics --cov-fail-under=80 --cov-report=term-missing`.
  - `ruff check src/ tests/` como etapa separada.
  - Não commitar segredos.
- *Critérios de aceitação:*
  - CI verde em push e pull_request.
  - Badge `tests passing` visível no README.
- *Implementação:* `.github/workflows/testes.yml`.
- *Dependências:* T07, T08.

#### T10 Funil + dicionário (esqueleto)
- *Objetivo:* Documentar o processo de seleção e a estrutura dos dados.
- *Regras de negócio / restrições:*
  - Funil: candidatos → com Actions → com ≥5 releases e ≥50 runs → amostra final. Cada etapa com contagem e motivo de descarte.
  - Dicionário: nome da coluna, tipo, unidade, fórmula/origem na API.
- *Critérios de aceitação:*
  - `reports/funnel.md` com estrutura de tabela.
  - `docs/data_dictionary.md` com colunas de `candidates.csv`.
- *Implementação:* Arquivos Markdown.
- *Dependências:* T04.

### S02 — Amostra e validação

#### T11 Planilha-ouro
- *Objetivo:* Gerar planilha estruturada para rotulagem manual de 60 repositórios.
- *Regras de negócio / restrições:*
  - Sortear 60 repositórios da amostra final com seed fixa (`random_state=42`).
  - Colunas obrigatórias: `full_name`, `project_type` (biblioteca/framework, aplicação/serviço, ferramenta CLI, outro), `delivers_to_user` (sim/não/incerto), `release_url_1`..`release_url_5` (links diretos para a página da release no GitHub), `notes`.
  - Links devem ser clicáveis em CSV/Excel.
- *Critérios de aceitação:*
  - CSV com exatamente 60 linhas e colunas corretas.
  - Reproduzível: rodar o script novamente gera a mesma amostra.
- *Implementação:* `scripts/generate_gold.py`.
- *Dependências:* T16.

#### T12 Rótulos independentes
- *Objetivo:* Coletar rotulagens dos 3 integrantes sem comunicação.
- *Regras de negócio / restrições:*
  - Cada membro preenche seu próprio arquivo: `data/gold/labels_A.csv`, `labels_B.csv`, `labels_C.csv`.
  - Sem consultar os demais e sem ver a saída da heurística automática.
  - Para cada repositório: tipo do projeto, entrega real ao usuário, 5 releases sorteadas (corretiva sim/não).
- *Critérios de aceitação:*
  - 3 CSVs completos com mesmo schema.
  - Auditoria: registrar data/hora de conclusão de cada membro.
- *Implementação:* Scripts de cópia e validação de schema.
- *Dependências:* T11.

#### T13 Concordância e consenso
- *Objetivo:* Medir acordo entre avaliadores e gerar rótulo de consenso.
- *Regras de negócio / restrições:*
  - Usar `aggregate_raters` + `fleiss_kappa` do `statsmodels` por dimensão (tipo, entrega, corretiva).
  - Protocolo de desempate: maioria simples; em caso 1-1-1, decisão em reunião registrada em `docs/consensus_protocol.md`.
  - Rótulo de consenso em `data/gold/labels_consensus.csv`.
- *Critérios de aceitação:*
  - Kappa reportado por dimensão com interpretação (Landis & Koch).
  - Consenso documentado.
- *Implementação:* `scripts/agreement.py`.
- *Dependências:* T12.

#### T14 Heurística CFR(b)
- *Objetivo:* Implementar classificador de release corretiva e refinar até F1 ≥ 0,70.
- *Regras de negócio / restrições:*
  - v1: release é corretiva se mudar apenas o `PATCH` do SemVer.
  - v2: v1 OU commits com mensagem contendo `fix`, `revert`, `hotfix` (case-insensitive).
  - v3: pesos (patch-only = 1, keywords = 2) com corte tunável.
  - Loop automático testa combinações e seleciona a melhor F1 no consenso.
  - Documentar cada versão testada e F1 obtido em `docs/cfr_heuristic_history.md`.
- *Critérios de aceitação:*
  - F1 ≥ 0,70 no consenso.
  - Precisão, recall e F1 salvos em `data/gold/cfr_metrics.json`.
- *Implementação:* `metrics/cfr_release.py` + script de tuning.
- *Dependências:* T13.

#### T15 Dataset completo (≥ 300 repos)
- *Objetivo:* Coletar e processar a amostra final com filtros do enunciado.
- *Regras de negócio / restrições:*
  - Aplicar funil: ≥ 5 releases válidas e ≥ 50 workflow runs válidos no default branch.
  - Repositórios descartados são contabilizados no funil com motivo.
  - Gerar CSVs para C1, C2 e C3.
- *Critérios de aceitação:*
  - `data/datasets/dora_c1.csv`, `dora_c2.csv`, `dora_c3.csv` com ≥ 300 linhas cada.
  - `reports/funnel.md` atualizado com números reais.
- *Implementação:* Executar pipeline completo com `config.toml` de produção.
- *Dependências:* T04, T05, T06, T07, T08.

#### T16 Diff-datasets + template de Issue
- *Objetivo:* Automatizar comparação de CSVs para replicação cruzada.
- *Regras de negócio / restrições:*
  - Comparar colunas numéricas (métricas) com diferença relativa `|a-b|/max(a,b)`.
  - Comparar classificação DORA com % de mesma categoria.
  - Gerar template Markdown de Issue com: comando executado, mensagem de erro (se houver), valores esperados vs. obtidos.
- *Critérios de aceitação:*
  - `scripts/diff_datasets.py` funciona e gera `diff_report.md`.
  - Template salvo em `templates/issue_replicacao.md`.
- *Implementação:* Script + template.
- *Dependências:* T15.

#### T17 Dicionário de dados final
- *Objetivo:* Versão 1.0 da documentação de colunas.
- *Regras de negócio / restrições:*
  - Uma entrada por coluna dos CSVs finais.
  - Campos: nome, tipo, unidade, fórmula/origem, exemplo.
  - Revisar após S03 se novas colunas surgirem.
- *Critérios de aceitação:*
  - `docs/data_dictionary.md` completo e revisado.
- *Implementação:* Documentação.
- *Dependências:* T15.

#### T18 Artigo: seção de metodologia
- *Objetivo:* Escrever a seção de metodologia do artigo científico.
- *Regras de negócio / restrições:*
  - Incluir: fonte de dados, funil de seleção, janela de observação, definições operacionais e variantes C1/C2/C3, protocolo de validação manual.
  - Referenciar `docs/data_dictionary.md` e `reports/funnel.md`.
- *Critérios de aceitação:*
  - Seção pronta para merge no artigo final.
- *Implementação:* Editar `docs/artigo.md` ou arquivo equivalente.
- *Dependências:* T13, T14, T15, T16, T17.

### S03 — Análise

#### T19 RQ01-RQ04 + classificação DORA C1 + sobrevivência + bootstrap
- *Objetivo:* Estatística descritiva, classificação e tratamento de censura.
- *Regras de negócio / restrições:*
  - Mediana e IQR por repositório e agregado (não média/desvio).
  - Classificação C1: release como deploy, lead time (a), CFR(a), recovery.
  - Kaplan-Meier para tempo de recuperação censurado (episódios sem fim na janela).
  - Bootstrap BCa (2.000 amostras) para intervalo de confiança das medianas.
  - Reportar proporção de casos censurados por repositório.
- *Critérios de aceitação:*
  - Tabelas e CSVs com métricas e classificação DORA C1.
  - Gráfico de sobrevivência salvo em `analysis/output/`.
- *Implementação:* `analysis/rq01_rq04.py`, `analysis/recovery_survival.py`, `analysis/bootstrap.py`.
- *Dependências:* T16, T07.

#### T20 RQ05 Spearman
- *Objetivo:* Correlação entre deployment frequency e CFR.
- *Regras de negócio / restrições:*
  - Calcular separadamente para variantes (a) e (b) do CFR.
  - Spearman via `scipy.stats.spearmanr`.
  - Scatter plot com eixo em escala logarítmica.
  - Reportar ρ, p-valor, n e IC por bootstrap.
- *Critérios de aceitação:*
  - Gráfico salvo em `analysis/output/rq05_scatter.png`.
  - Valores reportados em `analysis/output/rq05_metrics.csv`.
- *Implementação:* `analysis/rq05_spearman.py`.
- *Dependências:* T20.

#### T21 RQ06 Kruskal + Holm + delta + Dunn
- *Objetivo:* Testes de diferença entre subgrupos com correção múltipla.
- *Regras de negócio / restrições:*
  - Escolher ≥ 3 fatores entre: linguagem, popularidade (quartis de estrelas), nº contribuidores (quartis), idade (quartis), tipo do projeto (rotulado em S02).
  - Kruskal-Wallis (≥ 3 grupos) ou Mann-Whitney (2 grupos).
  - Correção de Holm via `statsmodels.stats.multipletests` com `method='holm'`.
  - Cliff's delta por par (Romano et al.): |δ| < 0,147 desprezível; < 0,33 pequeno; < 0,474 médio; ≥ 0,474 grande.
  - Dunn post-hoc após Kruskal-Wallis significativo.
- *Critérios de aceitação:*
  - Tabela com p-valores ajustados, ε² ou δ, e interpretação do tamanho de efeito.
- *Implementação:* `analysis/rq06_kruskal.py`.
- *Dependências:* T16, T20.

#### T22 RQ07 sensibilidade + κ ponderado
- *Objetivo:* Medir robustez da classificação DORA a variações de definição.
- *Regras de negócio / restrições:*
  - Comparar C1, C2, C3.
  - % de repositórios que mudam de categoria entre cada par.
  - Kappa de Cohen ponderado (`cohen_kappa_score`, `weights='linear'`).
- *Critérios de aceitação:*
  - Matrizes de transição C1×C2, C1×C3, C2×C3.
  - κ reportado com interpretação.
- *Implementação:* `analysis/rq07_sensitivity.py`.
- *Dependências:* T20.

#### T23 RQ08 bônus
- *Objetivo:* Implementar ambos os bônus do enunciado.
- *Regras de negócio / restrições:*
  - Rework rate = releases corretivas (CFR(b) heurística validada) / total de releases.
  - Mann-Kendall trimestral por repositório usando `pymannkendall`.
  - Reportar proporção de repositórios com tendência significativa (p < 0,05) em cada direção.
- *Critérios de aceitação:*
  - CSVs com `rework_rate` por repo e `trend` (increasing/decreasing/negligible).
- *Implementação:* `analysis/rq08_bonus.py`.
- *Dependências:* T14, T20.

#### T24 Artigo: resultados + discussão
- *Objetivo:* Escrever as seções de resultados e discussão.
- *Regras de negócio / restrições:*
  - Apresentar mediana, IQR, classificação DORA, correlações, testes e tamanhos de efeito.
  - Discutir: o que surpreendeu, por quê, e como a robustez das definições afeta as conclusões.
- *Critérios de aceitação:*
  - Seções prontas para merge no artigo final.
- *Implementação:* Editar `docs/artigo.md` ou equivalente.
- *Dependências:* T20, T21, T22, T23, T24.

### Final — Replicação e revisão

#### T25 Replicação A: execução do outro grupo
- *Objetivo:* Executar o pipeline de outro grupo usando apenas o README.
- *Regras de negócio / restrições:*
  - Usar apenas a documentação do grupo autor. Sem pedir ajuda.
  - Subamostra de 30 repositórios do dataset original.
  - Registrar checklist: dependências instaladas, token configurado, comando executado, erros encontrados, tempo de execução.
- *Critérios de aceitação:*
  - Log de execução (`reports/replication_run.md`) com passo a passo.
- *Implementação:* `scripts/run_other_pipeline.py` + manual.
- *Dependências:* Nenhuma (repositório externo).

#### T26 Replicação B: comparação + Issues
- *Objetivo:* Comparar resultados e abrir Issues de divergência.
- *Regras de negócio / restrições:*
  - Usar `diff_datasets.py` para comparar métricas e classificação DORA.
  - Diferença relativa por métrica; % de repositórios com mesma classificação.
  - Abrir Issue no repo do autor para cada problema, com evidências: comando, erro, esperado vs. obtido.
  - Pequenas diferenças são esperadas por janelas de coleta distintas; documentar explicação.
- *Critérios de aceitação:*
  - Issues abertas com template preenchido.
  - `reports/replication_diff.md` gerado.
- *Implementação:* `scripts/diff_datasets.py` + `gh issue create`.
- *Dependências:* T26, T16.

#### T27 Replicação C: respostas + pipeline doctor
- *Objetivo:* Responder Issues recebidas e validar a saúde do próprio pipeline.
- *Regras de negócio / restrições:*
  - Corrigir pipeline quando houver falha real; justificar quando for comportamento esperado.
  - `pipeline doctor`: comando que valida token, janela, config, cache e dependências.
- *Critérios de aceitação:*
  - Issues respondidas até o prazo.
  - `python -m pipeline doctor` roda sem erros fatais.
- *Implementação:* `scripts/answer_issues.py`, `pipeline doctor` na CLI.
- *Dependências:* T26.

#### T28 Ameaças à validade + revisão final + snapshot
- *Objetivo:* Fechar o artigo e a evidência de processo.
- *Regras de negócio / restrições:*
  - Ameaças em 4 categorias (Wohlin): constructo, interna, externa, conclusão.
  - Cada categoria apoiada em resultados da validação manual e análise de sensibilidade.
  - Snapshot do GitHub Projects exportado para CSV no fechamento.
- *Critérios de aceitação:*
  - `docs/threats.md` completo.
  - Artigo final revisado e dentro das 10 páginas.
  - `data/snapshots/SFinal_<timestamp>.csv` gravado.
- *Implementação:* Documentação + snapshot.
- *Dependências:* T25, T26, T27, T28.

---

## Decisões técnicas

| Decisão | Valor |
|---|---|
| Cliente HTTP | `httpx` sync (NÃO usa PyGithub/Octokit). GraphQL em lote para reduzir quota. |
| Paginação | `Link: rel="next"` + backoff 1/2/4/8s, max 5 tentativas, pause por `X-RateLimit-Reset`. |
| Caching | SQLite `data/cache/`, chave `url_hash`. `staleness_report.json` por stage. |
| Config | `config.toml` + env `GITHUB_TOKEN`. Janela, slices, tokens, paths. |
| Métricas | Funções puras em `metrics/` sem I/O. Fixtures em `tests/fixtures/`. Cobertura alvo ≥ 80%. |
| Relatório | Auto-gerado via matplotlib/plotly + markdown a partir dos CSVs. |
| Reprodutibilidade | `uv.lock`, `Dockerfile`, `manifest.json` (SHA256 das respostas brutas por repo+endpoint). |

---

## Inovações incluídas ("o a mais")

1. **GraphQL em lote + rate budget** — orçamento de cota visível e ETA por etapa.
2. **Reprodutibilidade** — `uv.lock`, Dockerfile, `pipeline doctor`, manifest SHA256.
3. **Cache com staleness + retomada por stage** — relatório de quantos repos mudaram desde a última coleta; retoma pelo último stage completo.
4. **diff-datasets + template de Issue** — entrega final vira mecânica.
5. **Censura com Kaplan-Meier + bootstrap BCa** — Sobrevivência para recovery; confiança robusta para medianas/IQRs.
6. **Relatório + dicionário de dados auto-gerados** — single source of truth no código.
7. **Ambos os bônus RQ08** — rework rate + Mann-Kendall trimestral.

**Fora do escopo (opcional):** snapshot automático do GitHub Projects e dogfooding do próprio repo como achado principal.

---

## Riscos e mitigação

| Risco | Mitigação |
|---|---|
| Rate limit | Cache + batch + stage-resume + divisão mensal de runs. |
| Censura | Reportar proporção censurada, nunca descartar. |
| Heurística ambígua | Loop F1 automático, limite 0,70. Documentar versões testadas. |
| Replicação | diff-datasets + template de Issue; `--limit 2` + smoke test no CI. |
| Validade externa | Discussão: projetos populares ≠ corporativos. |
| Multi-testes inflando FP | Correção de Holm em todas as comparações múltiplas. |

---

## Como começar (S01)

```bash
cd "/home/alvim/github/Lab-Experimentacao-e-Medicao-/Enunciado 3"
cp .env.example .env   # GITHUB_TOKEN=ghp_...
uv sync
uv run pytest --cov=metrics --cov-report=term-missing
uv run python -m pipeline --config config.toml --stage collect --limit 20   # smoke
```

## Dicionário mínimo de Issues sugeridas

- `S01-T01`: scaffold repo + pyproject + ruff + uv.lock
- `S01-T02`: cliente GraphQL/REST + rate limit + backoff
- `S01-T03`: SQLite cache + staleness + resume
- `S01-T04`: busca de candidatos por slices
- `S01-T05`: releases/tags/commits + compare
- `S01-T06`: runs (divisão mensal)
- `S01-T07`: funções + testes de métricas (lead time, CFR, recovery)
- `S01-T08`: CLI `pipeline`
- `S01-T09`: CI + smoke test
- `S01-T10`: funil + dicionário esqueleto
- `S02-T11`: gerador planilha-ouro
- `S02-T12`: rótulos independentes
- `S02-T13`: concordância + consenso
- `S02-T14`: heurística CFR(b) + loop F1
- `S02-T15`: dataset completo 300+
- `S02-T16`: diff-datasets + template Issue
- `S02-T17`: dicionário final
- `S02-T18`: artigo metodologia
- `S03-T19`: RQ01-RQ04 + DORA C1 + sobrevivência + bootstrap
- `S03-T20`: RQ05 Spearman
- `S03-T21`: RQ06 Kruskal + Holm + delta + Dunn
- `S03-T22`: RQ07 (C1×C2×C3 + κ ponderado)
- `S03-T23`: RQ08 rework + Mann-Kendall
- `S03-T24`: artigo resultados + discussão
- `Final-T25`: replicação execução
- `Final-T26`: replicação comparação + Issues
- `Final-T27`: replicação respostas + doctor
- `Final-T28`: ameaças + revisão final + snapshot Project
