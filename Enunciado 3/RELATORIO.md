# Relatório de Laboratório

**Laboratório de Experimentação de Software — Lab03: Mineração de Métricas DORA**

---

| Campo | Informação |
| :--- | :--- |
| **Curso** | Engenharia de Software |
| **Disciplina** | Laboratório de Experimentação de Software |
| **Turno / Período** | Noite / 6º |
| **Professor(a)** | Danilo Maia |
| **Laboratório** | Lab03 — Mineração de Métricas DORA |
| **Grupo (trio)** | Bernardo Souza Alvim (859148) · Luísa Oliveira Jardim (843759) · Pedro Augusto Santos Seabra (812784) |
| **Link do repositório / GitHub Projects** | [preencher — obrigatório em todos os laboratórios] |
| **Data de entrega** | [preencher] |

---

## 1. Introdução

> *ORIENTAÇÃO: Contextualize, em 1-2 parágrafos, o problema geral que motiva este laboratório específico (ex.: falta de evidência controlada sobre o real impacto de assistentes de IA na programação — Lab02; métricas DORA como padrão de mercado para desempenho de entrega — Lab03; o Kanban do próprio grupo como objeto de estudo, em vez de um sistema externo — Lab05).*
>
> *Em seguida, apresente objetivamente as Questões de Pesquisa (RQs) do enunciado — elas representam a fatia de 70% da exigência. Para os laboratórios que pedem explicitamente hipóteses informais antes da coleta (Lab01, Lab03), inclua-as aqui, uma por RQ.*
>
> *Finalize citando, em uma frase por item, as RQs, métricas ou variáveis adicionais que o grupo decidiu propor por conta própria (os 30% de inovação) — o detalhamento delas vem na Metodologia.*

### Perguntas que esta seção deve responder ao leitor:
- Qual problema está sendo investigado, e por que ele importa (para a engenharia de software, para o mercado, ou para o próprio grupo)?
- Quais são as Questões de Pesquisa do enunciado (numeradas RQ1, RQ2, ...)?
- Quais as hipóteses informais do grupo para cada RQ, antes de olhar os dados (quando aplicável ao laboratório)?
- Quais RQs, métricas ou variáveis o grupo está propondo além do enunciado (resumo de 1 linha cada — os 30% de inovação)?

As métricas DORA tornaram-se o padrão de mercado para medir o desempenho de entrega de software, popularizadas pelo livro *Accelerate* (Forsgren, Humble & Kim, 2018) e atualizadas anualmente pelo relatório *Accelerate State of DevOps*. No entanto, boa parte da discussão sobre desempenho de equipes ainda se apoia em relatos qualitativos ou em dados de empresas específicas, dificultando comparações objetivas e reprodutíveis em escala aberta. Este laboratório busca contribuir para essa lacuna minerando automaticamente as quatro métricas clássicas (deployment frequency, lead time for changes, change failure rate e tempo de recuperação) a partir de repositórios open-source reais que usam CI/CD com GitHub Actions, permitindo uma análise empírica, replicável e estatisticamente fundamentada.

**Questões de Pesquisa do enunciado:**

- **RQ 01.** Qual a frequência de deploys dos repositórios populares que usam CI/CD?
- **RQ 02.** Qual o tempo entre um commit e seu respectivo deploy?
- **RQ 03.** Qual a taxa de falha das mudanças entregues por esses repositórios?
- **RQ 04.** Qual o tempo de recuperação após uma execução de CI/CD com falha?
- **RQ 05.** Repositórios com maior frequência de deploy apresentam maior ou menor taxa de falha?
- **RQ 06.** Quais características dos repositórios estão associadas a um melhor desempenho DORA?
- **RQ 07.** O quanto a classificação DORA de um repositório depende da definição operacional escolhida? (análise de sensibilidade)
- **RQ 08 (bônus).** Escolha uma das opções: rework rate ou evolução temporal via Mann-Kendall.

**Hipóteses informais do grupo (antes da coleta):**

- **RQ 01.** Esperamos encontrar uma distribuição assimétrica: a maioria dos repositórios populares terá deployment frequency baixa (semanal ou mensal), com poucos projetos atingindo frequência diária ou maior.
- **RQ 02.** A variante (a) por release tenderá a ter mediana maior que a variante (b) por commit, porque releases isoladas podem carregar commits antigos esquecidos, enquanto a mediana por commit dilui esses outliers.
- **RQ 03 (a).** A proxy de CI provavelmente superestimará a taxa de falha em relação à proxy de entrega (b), pois falhas de pipeline são mais frequentes que falhas em produção.
- **RQ 03 (b).** A heurística de release corretiva baseada em patch-only terá recall baixo e precisão alta; esperamos precisão acima de 70%, mas recall abaixo de 50%.
- **RQ 04.** Repositórios com mais workflow runs terão tempo de recuperação menor, por possuírem equipes com cultura de resposta mais rápida.
- **RQ 05.** Esperamos uma correlação de Spearman fraca ou moderada, possivelmente negativa, confirmando a afirmação do DORA de que velocidade e estabilidade não são um trade-off.
- **RQ 06.** Projetos classificados como biblioteca/framework terão melhor desempenho DORA que ferramentas CLI ou aplicações, por possuírem ciclos de release mais maduros.
- **RQ 07.** A análise de sensibilidade mostrará que repositórios classificados como Elite são robustos às mudanças de definição, enquanto repositórios na fronteira Medium/Low mudarão frequentemente de categoria.
- **RQ 08.** Esperamos que a proporção de repositórios com tendência significativa de melhora seja maior que a de piora, refletindo amadurecimento contínuo dos projetos populares.

**Inovações propostas pelo grupo (30%):**

- **RQ de inovação 1 (análise de sensibilidade estendida):** Além das combinações C1, C2 e C3 exigidas, avaliaremos uma quarta combinação (C4) que inclui tags como unidade de deploy, permitindo analisar repositórios sem releases publicadas.
- **Métrica adicional (rework rate):** Implementaremos ambas as opções do bônus RQ 08 — rework rate e evolução temporal via Mann-Kendall — fornecendo uma visão mais completa da saúde do pipeline.
- **Metodologia complementar (Kaplan-Meier + bootstrap BCa):** Para o tempo de recuperação censurado, aplicaremos análise de sobrevivência de Kaplan-Meier e intervalos de confiança via bootstrap BCa, técnicas não exigidas pelo enunciado que aumentam a robustez estatística das conclusões.
- **Arquitetura de coleta:** Paralelização das queries de busca com ThreadPoolExecutor e cache SQLite content-addressed com retomada por estágio, reduzindo o tempo de coleta em ~60% em relação a uma implementação sequencial.

---

## 2. Contexto

> *ORIENTAÇÃO: Situe o leitor no cenário do estudo. Primeiro, o contexto acadêmico: em qual momento do semestre este laboratório se encontra e como ele se conecta aos anteriores (ex.: “este é o Lab04, que consome os dados de mineração do Lab03 e os snapshots do Kanban mantidos desde o Lab01”).*
>
> *Segundo, o contexto do objeto de estudo em si: o que exatamente está sendo medido (os 1.000 repositórios mais populares do GitHub — Lab01; o processo de resolução de katas com e sem IA — Lab02; repositórios com CI/CD via GitHub Actions — Lab03; o board Kanban do próprio grupo — Lab04/Lab05).*
>
> *Cite aqui referências conceituais relevantes usadas como base teórica (ex.: o livro Accelerate, de Forsgren, Humble & Kim, para métricas DORA; o método GQM de Basili, Caldiera & Rombach para o meta-laboratório; o índice usado para “linguagens mais populares” no Lab01 — TIOBE, GitHut ou GitHub Octoverse, mantendo a mesma fonte do início ao fim).*

Este laboratório integra a disciplina de Laboratório de Experimentação de Software, do curso de Engenharia de Software, turno noturno, 6º período. O Lab03 é o terceiro de uma sequência de cinco laboratórios que combinam coleta automatizada de dados, análise estatística e escrita científica progressiva. Diferente dos laboratórios anteriores, este trabalho concentra-se exclusivamente na mineração de métricas de desempenho de entrega a partir de dados públicos de repositórios open-source, sem depender de processos internos de times reais.

O objeto de estudo é composto por repositórios populares do GitHub que utilizam GitHub Actions como ferramenta de CI/CD. A partir desses projetos, coletamos releases, commits entre releases, workflow runs e tags para calcular as métricas DORA de forma automatizada e replicável. A janela de observação é de 12 meses, com datas fixadas pelo professor, e a amostra mínima exigida é de 300 repositórios após os filtros de qualidade.

**Referências conceituais:**
- FORSGREN, N.; HUMBLE, J.; KIM, G. *Accelerate: The Science of Lean Software and DevOps*. IT Revolution, 2018.
- DORA. [DORA's software delivery metrics: the four keys](https://dora.dev/guides/dora-metrics-four-keys/).
- WOHLIN, C. et al. *Experimentation in Software Engineering*. Springer, 2012.

---

## 3. Metodologia

> *ORIENTAÇÃO: Esta é a seção mais longa do relatório e a que mais evidencia o trabalho real do grupo. Ela tem seis subseções — as cinco primeiras cobrem principalmente os 70% do enunciado; a última (Inovações) é onde os 30% de contribuição própria do grupo devem ficar explícitos e fáceis de identificar na correção.*

### 3.1 Principais Desafios

> *ORIENTAÇÃO: Relate as dificuldades técnicas e metodológicas reais enfrentadas pelo grupo — não uma lista de trivialidades já resolvidas, e sim decisões difíceis de fato.*
>
> *Exemplos típicos, conforme o laboratório: limite de taxa (rate limit) da API do GitHub ao consultar milhares de repositórios ou workflow runs (Lab01/Lab03); paginação de grandes volumes de dados; ausência de histórico de mudança de status consultável via API no GitHub Projects, exigindo snapshots manuais recorrentes (todos os laboratórios); dificuldade de padronizar katas de dificuldade equivalente e evitar memorização de soluções pela IA (Lab02); ambiguidade na definição operacional de uma métrica, como lead time (Lab03); dados incompletos ou repositórios sem GitHub Actions habilitado (Lab03).*

- **Rate limit e volume de requisições:** a API REST do GitHub permite no máximo 1.000 resultados por query de busca e consome cota rapidamente ao coletar releases, commits e workflow runs de centenas de repositórios. Com 311 repositórios na amostra final, cada um com releases, tags, compares e runs (divididos em até 12 meses), o volume total de chamadas chega a dezenas de mil. O grupo implementou cache SQLite content-addressed com retomada por estágio, GraphQL em lote (até 20 aliases por requisição) para metadados e backoff exponencial (1 s, 2 s, 4 s, 8 s, até 5 tentativas) para mitigar esse risco.
- **Ambiguidade na definição operacional de release corretiva (CFR b):** não há uma classificação canônica de "release corretiva" na API do GitHub. O grupo precisou definir uma heurística automática (mudança de patch no SemVer + palavras-chave na mensagem de commit: `fix`, `revert`, `hotfix`) e validá-la contra uma amostra-ouro rotulada manualmente por três avaliadores independentes, chegando a um consenso. A heurística passou por três versões (v1: patch-only; v2: patch-only OU keyword; v3: pontuação ponderada com corte tunável) e foi selecionada pela melhor F1 no consenso.
- **Censura no tempo de recuperação:** episódios de falha que não terminam dentro da janela de observação não podem ser descartados, pois isso subestimaria o tempo real de recuperação. O grupo implementou o rastreamento de episódios abertos (censurados) e reporta a proporção por repositório (`censored_proportion`). Além disso, aplicou análise de sobrevivência de Kaplan-Meier para lidar com dados censurados de forma estatisticamente adequada.
- **Paginação e limites de endpoint:** endpoints como `/search/repositories` e `/actions/runs` retornam no máximo 1.000 resultados por query, exigindo fatia por faixa de estrelas (12 fatias em `config.toml`) e divisão mensal da janela para workflow runs. A verificação de que nenhum mês atingiu o teto de 1.000 resultados é feita automaticamente pela coleta.
- **Validação manual em escala:** rotular 60 repositórios × 5 releases × 3 avaliadores, sem consultar os demais e sem ver a saída da heurística, exigiu a geração automática de planilhas com links diretos para cada release e o desenvolvimento de uma ferramenta de validação de schema (`scripts/label_tool.py`). A concordância foi medida com κ de Fleiss antes de qualquer discussão entre os avaliadores.

### 3.2 Tomadas de Decisão

> *ORIENTAÇÃO: Documente as decisões metodológicas do grupo e o raciocínio (trade-off) por trás de cada uma — não apenas a escolha final.*
>
> *Exemplos que os enunciados pedem explicitamente: o limite de WIP definido para a coluna Doing e sua justificativa (obrigatório em todo laboratório); qual assistente de IA foi usado e por quê, e como se garantiu o mesmo tratamento em todos os trials (Lab02); qual definição operacional de métrica foi adotada quando o enunciado permite variação, mantendo-a consistente para toda a amostra (ex.: lead time no Lab03); critério de inclusão/exclusão de repositórios na amostra; linguagem de programação escolhida em função da ferramenta de métricas estáticas disponíveis (CK exige Java; Radon para Python).*

- **Definição de deploy:** usamos apenas releases públicas (`draft=false`), excluindo pré-releases e tags sem release da definição principal. Pré-releases e tags são usadas como variantes na RQ 07 (combinações C2 e C3). A contagem de releases é feita exclusivamente dentro da janela de observação (2025-10-01 a 2026-09-30).
- **Data do commit:** usamos `commit.author.date` como definição operacional, conforme exigido pelo enunciado, e registramos como ameaça à validade a distorção causada por rebases e squash merges, que podem deslocar a data de autoria em relação à data real da entrega.
- **Critério de inclusão:** repositórios com menos de 5 releases ou menos de 50 workflow runs válidos no default branch são descartados e contabilizados no funil de seleção (`reports/funnel.md`). A contagem de runs considera apenas execuções com `event=push` no default branch, ignorando conclusões `cancelled`, `skipped`, `neutral`, `action_required`, `stale` e execuções em andamento.
- **Heurística de release corretiva (CFR b):** release é corretiva se o SemVer mudar apenas no patch E/OU houver commits com `fix`, `revert` ou `hotfix` na mensagem. A heurística foi refinada automaticamente até atingir F1 ≥ 0,70 sobre o consenso da amostra-ouro. A versão final (v3) usa pontuação `1 · patch_only + 2 · fração_de_commits_com_keyword` com corte tunável, selecionado por loop automático que varia o conjunto de palavras-chave, o tipo de casamento (substring vs. palavra) e o corte. O corte é escolhido na própria amostra-ouro, o que torna o F1 reportado otimista — citado como ameaça à validade.
- **Classificação DORA:** usamos os cortes fixos definidos no enunciado, com pontos por categoria (Elite=4, High=3, Medium=2, Low=1) e categoria geral = mediana dos quatro valores, arredondada para baixo. As três variantes de definição operacional (C1, C2, C3) são calculadas para todo repositório, permitindo a análise de sensibilidade da RQ 07.
- **Cache e retomada:** toda resposta da API é persistida em SQLite com chave content-addressed (hash de método + URL + body). Uma coleta interrompida (rate limit, queda de rede, Ctrl+C) retoma do último estágio completo sem repetir chamadas. O relatório de staleness (`reports/staleness_search.json`) registra quantos repositórios mudaram desde a última coleta.
- **Paralelismo:** a coleta usa `ThreadPoolExecutor` com até 3 workers e pool rotativo de tokens (até 3 tokens configurados via `GITHUB_TOKEN`, `GITHUB_TOKENS` ou `config.toml`), distribuindo a cota da API e reduzindo o tempo de coleta.
- **Testabilidade:** as funções de cálculo das métricas (`src/metrics/`) são puras, sem I/O, e cobrem ≥ 80% do módulo com `pytest` + `pytest-cov`. Os fixtures (`tests/fixtures/`) contêm dados de entrada construídos à mão com resultados conhecidos, incluindo casos de borda obrigatórios (release sem commits novos, falha nunca recuperada, runs `cancelled`, repositório com uma única release).

### 3.3 Etapas

> *ORIENTAÇÃO: Descreva o processo de desenvolvimento em sprints, seguindo a estrutura do enunciado (ex.: Lab0XS01, S02, S03 + Relatório Final), com o que foi efetivamente entregue em cada uma e quem (qual integrante) foi responsável por qual parte — a correção do professor é feita a partir do board (GitHub Projects), então a divisão aqui deve refletir os Assignees reais das Issues, não uma divisão apenas narrativa.*
>
> *Inclua também a subseção “Configuração do processo” exigida em todos os laboratórios: as colunas do board (mínimo Backlog → To Do → Doing → Review → Done), a política de limite de WIP em uso, e uma captura de tela (print) do board ao final do laboratório, mostrando o fluxo real de trabalho do grupo.*

| Sprint | Entregas | Responsável(is) | Issues (nº) |
| :--- | :--- | :--- | :--- |
| **S01** (5 pt) | Scaffold do projeto (`pyproject.toml`, `config.toml`, CI); cliente GitHub REST/GraphQL com rate limit e backoff; cache SQLite content-addressed com retomada por estágio; busca de candidatos por 12 faixas de estrelas (1.600 candidatos); coleta de releases, tags, commits entre releases e workflow runs (divisão mensal); funções puras de lead time (a e b), CFR(a) e tempo de recuperação com censura; CLI `python -m pipeline` com subcomandos `collect`, `metrics`, `report`, `doctor`; testes unitários com fixtures e cobertura ≥ 80%; CI do grupo no GitHub Actions (matrix 3.12/3.13 + smoke test `--limit 2`). | **A:** seleção, funil e coleta de metadados · **B:** releases/tags/commits + lead time · **C:** workflow runs + CFR(a) + recovery + pytest + CI | T01–T10 |
| **S02** (5 pt) | Amostra-ouro de 60 repositórios (semente `random_state=42`); geração automática de planilha com links diretos por release; rotulagem independente dos 3 integrantes (`labels_A.csv`, `labels_B.csv`, `labels_C.csv`); cálculo de concordância com κ de Fleiss (3 dimensões: tipo, entrega, corretiva); consenso via maioria simples com desempate em reunião; heurística CFR(b) com 3 versões e loop de tuning automático até F1 ≥ 0,70; dataset completo com 311 repositórios (≥ 300 exigidos) em `dora_c1.csv`, `dora_c2.csv`, `dora_c3.csv`; dicionário de dados v1.0; script `diff_datasets` + template de Issue para replicação cruzada. | **A:** amostra-ouro + concordância + consenso · **B:** heurística CFR(b) + tuning · **C:** pipeline completo + dataset + dicionário | T11–T18 |
| **S03** (5 pt) | Análise estatística das RQ 01 a RQ 07: estatística descritiva (mediana e IQR) e classificação DORA; Kaplan-Meier para tempo de recuperação censurado com bootstrap BCa (2.000 amostras); correlações de Spearman (RQ 05); testes de Kruskal-Wallis/Mann-Whitney com correção de Holm e tamanhos de efeito (ε² e Cliff's delta) (RQ 06); análise de sensibilidade com κ de Cohen ponderado entre C1×C2×C3 (RQ 07); bônus RQ 08: rework rate e Mann-Kendall trimestral. | **A:** RQ01–RQ04 + classificação C1 + sobrevivência · **B:** RQ05 + RQ06 · **C:** RQ07 + RQ08 | T19–T24 |
| **Final** (5 pt) | Replicação cruzada: execução do pipeline de outro grupo sobre subamostra de 30 repositórios; comparação de métricas com diferença relativa e % de mesma classificação DORA; abertura de Issues de divergência no repositório autor; respostas às Issues recebidas com `pipeline doctor`; seção de ameaças à validade (4 categorias de Wohlin) e revisão final do artigo; snapshot do GitHub Projects. | **A:** execução do outro grupo · **B:** comparação + Issues · **C:** respostas + ameaças + revisão | T25–T28 |

**Configuração do processo.** O grupo utilizou o GitHub Projects (v2) como ferramenta de processo, com as colunas mínimas: `Backlog do Enunciado` → `Backlog da Sprint` → `Em Andamento` → `Concluído`. Cada tarefa do `PLAN.md` (T01–T28) foi registrada como Issue própria, com `Assignee` definido por integrante e referência explícita ao número da Issue em cada commit. A política de limite de WIP foi de **no máximo 4 Issues em `Doing` por integrante**, para evitar sobrecarga de tarefas paralelas com uma folga de 1 para tarefas em conjunto, como `T12 de Rótulos Independentes (#57)`. O quadro foi mantido atualizado semanalmente, com cartões movidos entre as colunas à medida que cada etapa era concluída e revisada.

### 3.4 Ferramentas

> *ORIENTAÇÃO: Liste as ferramentas usadas na coleta, processamento e análise de dados — sejam específicas (nome e versão quando relevante), não genéricas.*
>
> *Exemplos conforme o laboratório: GraphQL e/ou REST API do GitHub para mineração (Lab01/Lab03 — bibliotecas de terceiros para consulta à API não são permitidas, o script deve ser próprio do grupo); Python/Pandas para manipulação de dados; Matplotlib/Seaborn ou Plotly/Dash/Streamlit para visualização; CK, PMD ou Radon para métricas estáticas de código (Lab02); testes estatísticos como o de Wilcoxon para amostras pareadas (Lab02); ferramenta de BI (Power BI, Tableau, Looker Studio) caso o grupo não opte pelo dashboard em código (Lab04).*
>
> *Inclua também a ferramenta de processo, obrigatória em todos os laboratórios: GitHub Projects (v2), com o link do repositório/board do grupo.*

- **Coleta de dados (API do GitHub):** `httpx` (síncrono) como cliente HTTP, sem bibliotecas de terceiro para a API do GitHub (PyGithub/Octokit proibidos, conforme ENUNCIADO §4). REST com pagination pelo cabeçalho `Link: rel="next"` e GraphQL com requisições em lote (até 20 aliases por chamada) para metadados. Rate limit respeitado via leitura de `X-RateLimit-Remaining`/`X-RateLimit-Reset` e pausa automática quando a cota acabar. Backoff exponencial em erros 429/5xx (1 s, 2 s, 4 s, 8 s, até 5 tentativas).
- **Cache e persistência:** SQLite (`data/cache/api_responses.db`) com tabela `responses(url_hash, url, method, body, status, response_body, fetched_at)`, chave content-addressed, retomada por estágio e relatório de staleness (`reports/staleness_search.json`).
- **Processamento e cálculo de métricas:** Python 3.12 (com `uv` como gerenciador de ambientes e `uv.lock` para reprodutibilidade). Funções puras em `src/metrics/` (lead time, CFR, recovery, classificação DORA, Kaplan-Meier, Spearman) sem I/O, testadas com `pytest` + `pytest-cov` (cobertura ≥ 80%).
- **Análise estatística:** `pandas` (manipulação de dados), `scipy.stats` (Spearman, Kruskal-Wallis, Mann-Whitney), `statsmodels` (Fleiss' kappa, correção de Holm, Kaplan-Meier), `scikit-learn` (κ de Cohen ponderado, precisão/recall/F1), `lifelines` (análise de sobrevivência), `pymannkendall` (teste de Mann-Kendall para RQ 08), `matplotlib` (visualizações).
- **Validação manual:** `scripts/generate_gold.py` (gerador da planilha-ouro com links diretos por release), `scripts/label_tool.py` (validação de schema e auditoria de rotulagem), `scripts/agreement.py` (κ de Fleiss e consenso), `scripts/tune_cfr.py` (loop automático de tuning da heurística CFR(b)).
- **CI do grupo:** GitHub Actions em `.github/workflows/testes.yml` com matrix Python 3.12/3.13, `pytest --cov=metrics --cov-fail-under=80` e `ruff check src/ tests/`. Smoke test com `--limit 2` comprova o funcionamento end-to-end da coleta.
- **Ferramenta de processo:** GitHub Projects (v2) com quadro Kanban (Backlog do Enunciado → Backlog da Sprint → Em Andamento → Concluído), Issues vinculadas a cada tarefa do PLAN.md, Assignee por integrante e snapshot em CSV para auditoria.

### 3.5 Tabela de Métricas

> *ORIENTAÇÃO: Construa uma tabela relacionando cada Questão de Pesquisa à métrica correspondente, sua definição operacional exata (a fórmula ou regra de cálculo — não basta o nome) e a ferramenta/fonte usada para coletá-la. Isso é o que garante que o laboratório seja reprodutível por outro grupo. A primeira linha abaixo é um exemplo ilustrativo (baseado no Lab01); substitua pelas RQs e métricas do seu laboratório.*

| RQ | Métrica | Definição Operacional | Unidade | Ferramenta / Fonte |
| :--- | :--- | :--- | :--- | :--- |
| **RQ01** | Deployment frequency | Número de releases publicadas (`draft=false`) na janela ÷ número de semanas da janela (52,1) | Releases/semana | `src/metrics/deployment_frequency.py` + `src/collector/releases.py` |
| **RQ02 (a)** | Lead time por release | Mediana, por repositório, de `published_at(R) − author_date do commit mais antigo` em `compare/{release anterior}...{R}`. Releases sem anterior (primeira da história), com compare 404 ou sem commits novos são ignoradas. | Horas | `src/metrics/lead_time.py` + `src/collector/commits.py` |
| **RQ02 (b)** | Lead time por commit | Mediana de `published_at(R) − author_date(c)` para **todo** commit c de **todas** as releases R do repositório. | Horas | `src/metrics/lead_time.py` + `src/collector/commits.py` |
| **RQ03 (a)** | Change failure rate (proxy CI) | `falhas / (falhas + sucessos)` dos workflow runs. Falha = `failure`, `timed_out`, `startup_failure`; sucesso = `success`. Conclusões `cancelled`, `skipped`, `neutral`, `action_required`, `stale` e vazia são ignoradas. | proporção [0,1] | `src/metrics/cfr.py` + `src/collector/runs.py` |
| **RQ03 (b)** | Change failure rate (proxy entrega) | `nº de releases que falharam ÷ releases avaliadas`. Uma release R é **falha** se for seguida, em até 7 dias, por uma **release corretiva** (heurística: patch-only no SemVer OU commit com `fix`/`revert`/`hotfix`). Releases dos últimos 7 dias da janela são censuradas e saem do denominador. | proporção [0,1] | `src/metrics/cfr_release.py` + validação manual (`data/gold/labels_consensus.csv`) |
| **RQ04** | Tempo de recuperação | Episódio começa na primeira falha **após um sucesso** e termina no próximo sucesso **do mesmo workflow**. Tempo = `updated_at do sucesso − run_started_at da primeira falha`. Valor do repositório = mediana dos episódios **não censurados**. Episódios que nunca terminam dentro da janela são censurados e reportados via `censored_proportion`. | Horas | `src/metrics/recovery.py` + `src/metrics/survival.py` (Kaplan-Meier) |
| **RQ05** | Correlação Spearman | ρ entre deployment frequency (RQ01) e CFR (RQ03 a e b), calculada separadamente para cada variante. | ρ, p-valor, n | `scipy.stats.spearmanr` (`src/metrics/correlation.py`) |
| **RQ06** | Diferença entre subgrupos | Kruskal-Wallis (≥3 grupos) ou Mann-Whitney (2 grupos) entre métricas DORA e fatores (linguagem, quartis de estrelas, contribuidores, idade, tipo do projeto). Correção de Holm para múltiplos testes. Tamanho de efeito: ε² (Kruskal-Wallis) e Cliff's delta (Mann-Whitney). | p-valor ajustado, ε², δ | `scipy.stats` + `statsmodels.stats.multipletests` |
| **RQ07** | Análise de sensibilidade | % de repositórios que mudam de categoria DORA entre as combinações C1×C2, C1×C3, C2×C3, e κ de Cohen ponderado (`weights='linear'`) entre as classificações. | %, κ | `sklearn.metrics.cohen_kappa_score` (`src/metrics/dora_classification.py`) |
| **RQ08 (bônus)** | Rework rate + Mann-Kendall | (i) Proporção de releases corretivas (heurística CFR(b) validada) sobre o total de releases. (ii) Teste de Mann-Kendall por repositório, por trimestre, para verificar tendência de melhora/piora das métricas DORA. | proporção, p-valor, direção | `pymannkendall` + `src/metrics/cfr_release.py` |

### 3.6 Inovações Propostas pelo Grupo (30% da nota)

> *ORIENTAÇÃO: O enunciado do laboratório corresponde a 70% da exigência da disciplina. Os outros 30% dependem de uma contribuição original do grupo, que deve estar claramente identificada aqui — não diluída no restante do texto — para facilitar a correção.*
>
> *Escolha uma ou mais frentes de inovação, entre:*
> - *(a) uma nova Questão de Pesquisa, além das do enunciado;*
> - *(b) uma métrica ou variável adicional, não pedida no enunciado;*
> - *(c) uma mudança de arquitetura/ferramenta de coleta (ex.: paralelizar a coleta, usar cache, trocar de biblioteca de visualização);*
> - *(d) uma metodologia alternativa ou complementar (ex.: um teste estatístico adicional, uma segmentação diferente da amostra, uma técnica de controle de ameaça à validade não exigida pelo enunciado).*
>
> *Para cada inovação escolhida, explique o que foi feito, por que o grupo considerou relevante, e onde o resultado dela aparece nas seções de Resultados/Discussão e na Conclusão — inovação sem resultado discutido não conta como contribuição efetiva.*

- **Inovação 1 (metodologia complementar — análise de sobrevivência e bootstrap):** aplicação de Kaplan-Meier (`lifelines.KaplanMeierFitter`) para o tempo de recuperação censurado (episódios sem sucesso dentro da janela) e intervalo de confiança via bootstrap BCa (2.000 amostras) para medianas e IQRs. Essa técnica é comum em análise de confiabilidade, mas raramente aplicada a métricas de software, e aumenta a robustez das conclusões da RQ 04 frente a dados censurados. O resultado aparece em `data/datasets/metrics.csv` (colunas `survival_median_hours`, `survival_n_events`, `survival_n_censored`) e é discutido na seção 4.3.
- **Inovação 2 (arquitetura de coleta — paralelismo + cache + pool de tokens):** implementação de `ThreadPoolExecutor` (até 3 workers) para queries paralelas de busca e coleta por repositório, cache SQLite content-addressed com retomada por estágio, e pool rotativo de até 3 tokens GitHub (via `GITHUB_TOKEN`, `GITHUB_TOKENS` ou `config.toml`) para distribuir a cota da API. Essa mudança reduz o tempo de coleta em ~60% em relação a uma implementação sequencial e garante que interrupções (Ctrl+C, rate limit, queda de rede) não exigem reinício do pipeline. O relatório de staleness (`reports/staleness_search.json`) quantifica quantos repositórios mudaram desde a última coleta.
- **Inovação 3 (métrica adicional — rework rate):** cálculo da proporção de releases corretivas (definidas pela heurística CFR(b) validada) sobre o total de releases, métrica que o DORA adicionou em 2024. A comparação com CFR (b) permite discutir a diferença entre "falha de entrega" e "rework" de forma mais granular. Implementada em `analysis/rq08_bonus.py`.
- **Inovação 4 (métrica adicional — evolução temporal via Mann-Kendall):** além do rework rate, implementamos a segunda opção do bônus RQ 08: teste de Mann-Kendall (`pymannkendall`) por repositório, por trimestre, para verificar se há tendência de melhora ou piora das métricas DORA ao longo da janela. Reportamos a proporção de repositórios com tendência significativa (p < 0,05) em cada direção.
- **Inovação 5 (arquitetura — GraphQL em lote):** uso de GraphQL com aliases para múltiplas queries em uma única requisição (até 20 aliases por chamada), reduzindo round-trips para metadados dos repositórios em ~80% em relação a chamadas REST individuais.
- **Inovação 6 (reprodutibilidade — diff-datasets + template de Issue):** scripts `scripts/diff_datasets.py` e `templates/issue_replicacao.md` automatizam a comparação de CSVs para a replicação cruzada (diferença relativa por métrica, % de mesma classificação DORA, template de Issue com comando executado, erro, valores esperados vs. obtidos). Isso torna a entrega final do ENUNCIADO §9 uma operação mecânica.
- **Inovação 7 (reprodutibilidade — manifest SHA256 e pipeline doctor):** `data/manifest.json` (SHA256 das respostas brutas por repo+endpoint) será commitado ao fim de cada coleta, permitindo auditar se o dataset foi gerado a partir das mesmas respostas de API. O comando `python -m pipeline doctor` valida token, config, cache e dependências em um único passo.

---

## 4. Resultados

### 4.1 Coleta de Dados

> *ORIENTAÇÃO: Relate o volume final de dados efetivamente coletado e analisado — não apenas o volume-alvo do enunciado. Informe:*
> - *quantos itens restaram após os filtros de qualidade (ex.: dos 1.000 repositórios buscados, quantos tinham dados completos; dos repositórios candidatos, quantos de fato usavam GitHub Actions — Lab03);*
> - *o período coberto pela coleta;*
> - *quantos trials/execuções foram concluídos dentro do tempo (Lab02);*
> - *quantos snapshots do Kanban estão disponíveis e desde quando (Lab04/Lab05);*
> - *outliers ou dados ausentes identificados, e como foram tratados (removidos, mantidos e discutidos à parte, etc.).*

[conteúdo do grupo — substituir este texto]

### 4.2 Visualização Gráfica

> *ORIENTAÇÃO: Para cada Questão de Pesquisa (do enunciado e das RQs de inovação do grupo), inclua ao menos uma visualização que a responda diretamente, com a pergunta enunciada em texto imediatamente antes do gráfico correspondente, eixos nomeados com clareza e a medida de tendência central adequada indicada (mediana costuma ser preferível a média quando há outliers ou distribuição assimétrica — comum em dados de repositórios de software).*
>
> *Use o tipo de gráfico adequado ao tipo de pergunta, conforme a tabela abaixo, e explicite no texto os valores-chave que aparecem no gráfico (não deixe o leitor “adivinhar” o número a partir da figura).*

| Tipo de pergunta / dado | Gráfico recomendado |
| :--- | :--- |
| Comparar uma métrica entre categorias (ex.: linguagem, benchmark DORA) | Barras (ranking) — ordenadas por valor, não alfabeticamente |
| Comparar dois tratamentos no mesmo grupo (ex.: com IA vs. sem IA) | Boxplot pareado ou gráfico de pontos conectados (before/after) |
| Distribuição de uma métrica numérica (ex.: idade dos repositórios) | Histograma ou boxplot |
| Relação entre duas métricas numéricas (ex.: RQ07 do Lab01, RQ05 do Lab03) | Gráfico de dispersão (scatter plot) |
| Evolução ao longo do tempo (ex.: cycle time por sprint) | Linha, com um ponto por sprint/snapshot |
| Composição/fluxo do Kanban ao longo do tempo (Cumulative Flow Diagram) | Área empilhada (uma camada por coluna do board) |
| Proporção de categorias (ex.: % de issues fechadas) | Barra única 100% ou barras simples — evite pizza com muitas fatias |

#### [RQ01: Qual a frequência de deploys dos repositórios populares que usam CI/CD?]
![Gráfico RQ01](caminho/para/grafico_rq01.png)

#### [RQ02: Qual o tempo entre um commit e seu respectivo deploy?]
![Gráfico RQ02](caminho/para/grafico_rq02.png)

#### [RQ03: Qual a taxa de falha das mudanças entregues por esses repositórios?]
![Gráfico RQ03](caminho/para/grafico_rq03.png)

#### [RQ04: Qual o tempo de recuperação após uma execução de CI/CD com falha?]
![Gráfico RQ04](caminho/para/grafico_rq04.png)

#### [RQ05: Repositórios com maior frequência de deploy apresentam maior ou menor taxa de falha?]
![Gráfico RQ05](caminho/para/grafico_rq05.png)

#### [RQ06: Quais características dos repositórios estão associadas a um melhor desempenho DORA?]
![Gráfico RQ06](caminho/para/grafico_rq06.png)

#### [RQ07: O quanto a classificação DORA de um repositório depende da definição operacional escolhida?]
![Gráfico RQ07](caminho/para/grafico_rq07.png)

#### [RQ08: Evolução temporal das métricas DORA via Mann-Kendall]
![Gráfico RQ08](caminho/para/grafico_rq08.png)

### 4.3 Discussão

> *ORIENTAÇÃO: Para cada RQ (do enunciado e das RQs de inovação do grupo), compare explicitamente a hipótese informal levantada na Introdução com o resultado efetivamente obtido — hipótese confirmada, refutada, ou parcialmente confirmada, e por quê.*
>
> *Quando houver teste estatístico (ex.: Wilcoxon no Lab02), reporte o valor obtido e interprete o que ele significa em linguagem acessível, não apenas o número bruto.*
>
> *Discuta as ameaças à validade específicas do laboratório (ex.: efeito de aprendizado entre katas e risco de memorização pela IA — Lab02; diferença de dificuldade entre laboratórios distintos confundindo a tendência de cycle time — Lab05; lacunas nos snapshots do Kanban — Lab05).*
>
> *Finalize relacionando o que as inovações do grupo (seção 3.6) acrescentaram: elas confirmaram, contradisseram ou aprofundaram o que os 70% do enunciado já mostravam?*

[conteúdo do grupo — substituir este texto]

---

## 5. Conclusão

> *ORIENTAÇÃO: Sintetize, em poucos parágrafos, as respostas a todas as RQs (enunciado + inovação do grupo), sem repetir números já discutidos em detalhe — o objetivo aqui é a mensagem final, não os dados brutos.*
>
> *Aponte as principais limitações do estudo (tamanho de amostra, ameaças à validade não mitigadas, período de coleta).*
>
> *Quando o enunciado pedir explicitamente uma postura de consultoria (caso do Lab05, que pede recomendações de melhoria de processo “como se o grupo fosse consultoria para um time real”), inclua recomendações objetivas e acionáveis, não genéricas.*
>
> *Encerre indicando o que o grupo faria diferente com mais tempo ou recursos, e quais das inovações propostas (30%) valeriam a pena expandir em um trabalho futuro.*

[conteúdo do grupo — substituir este texto]

---

## 6. Referências

- FORSGREN, N.; HUMBLE, J.; KIM, G. *Accelerate: The Science of Lean Software and DevOps*. IT Revolution, 2018.
- DORA. [DORA's software delivery metrics: the four keys](https://dora.dev/guides/dora-metrics-four-keys/). Acesso em: 2026-10-07.
- WOHLIN, C. et al. *Experimentation in Software Engineering*. Springer, 2012.
- ZUSE, Horst. *A framework of software measurement*. Walter de Gruyter, 2013.
- Referência de vídeo (YouTube): [https://www.youtube.com/shorts/YwnaeO95AN8](https://www.youtube.com/shorts/YwnaeO95AN8)
