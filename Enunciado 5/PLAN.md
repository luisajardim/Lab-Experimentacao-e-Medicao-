# PLAN.md — Lab05: Experimento em Software Real (gerenciadores de pacotes Node)

> Protótipo de kanban e documento de referência para o grupo (Alvim, Luísa, Pedro).
> **Status:** passível de mudanças — editar via Issues do GitHub Projects.

---

## Visão geral

| Item | Valor |
|---|---|
| **Grupo** | Bernardo Alvim, Luísa Jardim, Pedro Seabra (divisão por cadeias de dependência) |
| **Software** | Gerenciadores de pacotes Node: **npm** (controle) × **pnpm** × **Bun** × **Yarn** (Classic 1.22, Berry 4 `node-modules`, Berry 4 PnP), no **Windows 11** |
| **Pergunta** | Quanto tempo e quanto disco cada gerenciador gasta para instalar projetos Node reais no Windows? As promessas dos fabricantes (benchmarks do pnpm, "até 25×" do Bun) se confirmam? A adoção real acompanha o desempenho? |
| **Caminhos** | (1) **Experimento controlado** nas 3 máquinas do grupo · (2) **Dados de operação**: séries de downloads da API pública do npm |
| **Por que esse software** | Real e em operação: os 4 têm versões mantidas e são usados em produção e em CI. Alto impacto: o npm registry tem bilhões de downloads por semana. Os números, com fonte e data de acesso, ficam em `docs/proposta.md` (T06) |
| **Stack** | Python 3.12 + uv · numpy/scipy/pandas · psutil · Plotly · Streamlit · pytest + ruff · Verdaccio (registry local) |
| **Repositório** | `Enunciado 5/` |
| **Entrada única** | `uv run lab05` → lê os dados versionados → análise → abre o dashboard |
| **Documento final** | Artigo no template SBC (`Templates/SBC`) + dashboard Streamlit (local + Streamlit Community Cloud) |
| **Prazos** | **S01: 19/11/2026** · **S02: 26/11/2026** · **S03 + Final (artigo + apresentação de 10 min): 03/12/2026** |

---

## Kanban por sprint (S01 → Final)

| Sprint | Bernardo: coleta e infra | Luísa: método, caminho 2 e escrita | Pedro: análise e dashboard |
|---|---|---|---|
| **S01** (19/11) | T01 scaffold + **schema dos dados** → T02 Verdaccio → T04 runner → T05 **piloto** | T03 projetos-carga + lockfiles → T06 proposta (3 critérios, GQM, hipóteses, 7 categorias) · T07 protocolo + specs | T08 testes estatísticos → T09 nº de repetições (poder) · T10 dashboard base |
| **S02** (26/11) | T11 deploy (clone + subtree) · T12a coleta completa → T13 validação e versionamento · T14 aba Yarn × Yarn | T12b coleta completa · T15 downloads do npm → T16 aba Adoção × desempenho · T17 ameaças + esqueleto do artigo | T12c coleta completa · T18 aba Todos × npm |
| **S03 + Final** (03/12) | T19 checagem no registry real · T22a artigo (instrumentação, reaproveitamento) · T23a apresentação | T21 7 categorias revisadas + conclusões · T22b artigo (intro, método, ameaças, conclusão) · T23b apresentação | T20 impacto + aba Impacto · T22c artigo (resultados, impacto) · T23c apresentação |

> Regras: em cada sprint, cada integrante é Assignee de ≥ 1 Issue com código commitado, e **todo commit
> referencia o número da Issue** (`#NN`).

### Quanto um integrante bloqueia o outro

As cadeias são **quase** ponta a ponta. Os bloqueios reais são poucos e têm mitigação:

- **Contrato no 1º dia (T01):** o schema de `runs.csv` e o `config.py` saem em **15/11**, com um CSV sintético.
  - Pedro (T08, T09, T10) e Luísa (T15) desenvolvem sobre esse CSV e não esperam a coleta.
  - É a mesma tática do Lab04, que publicou o schema da simulação no 1º dia.
- **Caminho crítico da S01:** T01 → **T03 (Luísa, até ~16/11)** → T05 piloto (Bernardo, até ~17/11) → T09 poder (Pedro).
  - O T04 é desenvolvido com um projeto mínimo de teste e não espera o T03.
  - O T09 é implementado com dados sintéticos e só recebe o piloto no fim.
- **S02:** a coleta de cada um (T12a/b/c) roda na própria máquina e é independente, assim que T05, T07 e T09 fecharem.
  - As abas (T14, T16, T18) usam os dados do piloto até a coleta completa chegar.
  - Único gargalo: o T13 espera os 3 CSVs → **prazo interno: coleta completa até 23/11**.
- **S03:** cada um escreve as próprias seções do artigo em paralelo. Só o T20 (impacto) espera o T18, que fecha na S02.

---

## Desenho do experimento

| Item | Proposta |
|---|---|
| **Tratamentos (6)** | npm (**controle**) · pnpm · Bun · Yarn Classic 1.22 · Yarn Berry 4 `node-modules` · Yarn Berry 4 PnP |
| **Cargas (3)** | API Express pequena · app React + Vite · app Next.js, gerados pelos templates oficiais com versões fixadas (sem usar repositório de terceiros como objeto) |
| **Cenários (4)** | **cold** (sem cache e sem lockfile) · **ci** (lockfile, sem cache e sem `node_modules`) · **warm-cache** (lockfile + cache) · **reinstall** (tudo presente), no esquema da página de benchmarks do pnpm |
| **Blocos** | As 3 máquinas Windows 11 do grupo, com o mesmo protocolo e as specs registradas |
| **Rede** | **Verdaccio local** com cache dos pacotes: isola o gerenciador da internet de cada casa e não sobrecarrega o registry público. Uma rodada pequena no registry real (T19) checa a validade externa |
| **Fixo** | Windows Defender no padrão (vira ameaça/limitação, não fator) · versões de Node e dos gerenciadores · perfil de energia · Windows Update pausado |
| **Métricas** | Tempo de relógio (s) · CPU · pico de RAM · disco (`node_modules` + cache/store, deduplicando hard links) · nº de arquivos · **instalação válida** (`build` passa) |
| **Ordem** | Aleatorizada por bloco e repetição (semente fixa); rodadas de aquecimento descartadas |
| **N de repetições** | Definido pela análise de poder sobre a variância do piloto (T09). Estimativa: 72 células × N = 10 ≈ 720 instalações por máquina |

**Hipóteses** (bicaudais, α = 0,05):
- **Todos × npm:** para cada gerenciador M e cenário, H₀: a mediana do tempo de M é igual à do npm.
  Wilcoxon pareado com correção de Holm (5 comparações contra o controle, em vez de 15 pares).
- **Yarn × Yarn:** H₀: Classic, Berry-nm e Berry-PnP não diferem. Friedman + post-hoc Wilcoxon com Holm.
- **Promessas dos fabricantes:** o speedup em relação ao npm, com IC 95% por bootstrap, comparado ao valor anunciado.
- **Adoção × desempenho:** análise descritiva (só 5 gerenciadores).
- **Tamanho do efeito:** Cliff's δ + speedup (razão das medianas) com IC.

**Teoria aplicada:**
- **GQM** (template de Basili).
- **Escalas:** tempo e disco são de razão; o cenário é nominal; `build_ok` é nominal binária. Como as distribuições são assimétricas, usar mediana e testes não paramétricos.
- **Goodhart:** o "tempo de instalação" pode ser jogado. O Bun não roda os scripts de pós-instalação por padrão e o PnP não cria `node_modules`, daí o `build_ok`.
- **7 categorias** e **ameaças dos 4 tipos**.

**Reaproveitamento:**
- Lab01: coleta via API.
- Lab03: DORA, com a instalação como parte do lead time de CI.
- Lab04: poder, escolha do teste, bootstrap, dashboard e deploy.

---

## Tarefas detalhadas

### S01 — Proposta, instrumentação e piloto (19/11)

#### T01 Estruturar Projeto + Schema dos Dados (#96, Bernardo)
- *Objetivo:* Criar a base do projeto Python do Lab05 e publicar, no 1º dia, o contrato de dados que destrava as outras cadeias.
- *Regras de negócio / restrições:*
  - Layout igual ao do Lab04: `src/`, `app.py`, `projects/`, `data/raw/`, `data/npm_downloads/`, `docs/`, `tests/`, `deploy/`.
  - Python 3.12 + uv; entry point `uv run lab05` em `[project.scripts]`; ruff + pytest com a mesma configuração do Lab04.
  - `src/config.py`: semente, tratamentos (npm, pnpm, bun, yarn-classic, yarn-berry-nm, yarn-berry-pnp), cenários (cold, ci, warm-cache, reinstall), projetos e versões fixadas de Node e dos gerenciadores.
  - **Schema de `runs.csv`** documentado em `docs/schema.md`: machine, run_id, timestamp, project, scenario, manager, manager_version, node_version, registry, rep, order, warmup, wall_s, cpu_s, peak_rss_mb, disk_mb, cache_mb, n_files, build_ok, exit_code.
  - Gerar um `runs.csv` sintético no schema (`data/raw/synthetic/`) para Pedro e Luísa desenvolverem sem esperar a coleta.
- *Critérios de aceitação:*
  - `uv sync`, `uv run pytest` e `uv run ruff check` passam.
  - Schema publicado e CSV sintético commitado até 15/11.
- *Implementação:* `pyproject.toml`, `src/config.py`, `src/synthetic.py`, `docs/schema.md`, `README.md`.
- *Dependências:* Nenhuma.

#### T02 Montar Registry Local (Verdaccio) (#97, Bernardo)
- *Objetivo:* Subir um registry npm local que faça cache dos pacotes, isolando o efeito do gerenciador da velocidade da internet.
- *Regras de negócio / restrições:*
  - Verdaccio com versão fixada, porta e storage configurados no repositório (`registry/config.yaml`).
  - Script para subir, checar (health) e pré-aquecer o cache com as dependências dos 3 projetos-carga.
  - Os 6 tratamentos apontam para o registry local (`.npmrc`, `.yarnrc.yml`, `bunfig.toml`), sem tocar na configuração global do usuário.
  - Ética: o pré-aquecimento baixa cada pacote do registry público uma única vez.
- *Critérios de aceitação:*
  - `uv run lab05 registry up` deixa o Verdaccio respondendo e com o cache cheio.
  - Uma instalação com a internet desligada funciona para os 6 tratamentos.
- *Implementação:* `src/registry.py`, `registry/config.yaml`.
- *Dependências:* #96 (T01)

#### T03 Criar Projetos-Carga e Lockfiles (#98, Luísa)
- *Objetivo:* Criar os 3 projetos Node usados como carga do experimento, com versões fixadas e um lockfile por gerenciador.
- *Regras de negócio / restrições:*
  - Projetos: API Express pequena, app React + Vite e app Next.js, gerados pelos templates oficiais (`create-vite`, `create-next-app`) e com versões exatas no `package.json`.
  - Não usar repositórios de terceiros como carga (regra do enunciado: o objeto é o gerenciador em funcionamento).
  - Cada projeto tem script `build` (critério de "instalação válida").
  - Gerar e versionar os lockfiles dos 6 tratamentos (`package-lock.json`, `pnpm-lock.yaml`, `bun.lock`, `yarn.lock` v1 e v4, com `.yarnrc.yml` para node-modules e PnP).
  - Registrar em `projects/README.md` o nº de dependências diretas e transitivas de cada projeto.
- *Critérios de aceitação:*
  - `projects/{express-api,react-vite,next-app}/` com os lockfiles.
  - O build passa nos 6 tratamentos para os 3 projetos.
  - Pronto até ~16/11 (caminho crítico do piloto).
- *Implementação:* `projects/`.
- *Dependências:* #96 (T01)

#### T04 Implementar Runner de Instalação (#99, Bernardo)
- *Objetivo:* Automatizar uma instalação medida: preparar o cenário, instalar, medir, validar com o build e gravar uma linha no CSV.
- *Regras de negócio / restrições:*
  - Preparação por cenário: cold (limpa cache, lockfile e `node_modules`), ci (lockfile, sem cache e sem `node_modules`), warm-cache (lockfile + cache), reinstall (tudo presente).
  - Métricas: tempo de relógio (`perf_counter`), CPU e pico de RSS da árvore de processos (`psutil`), disco do `node_modules` + cache/store deduplicando hard links por `st_ino`, nº de arquivos.
  - Depois de instalar, roda `build` e registra `build_ok`.
  - Ordem dos tratamentos aleatorizada por bloco e repetição, com a semente de `config.py`; rodadas de aquecimento descartadas.
  - Desenvolver com um projeto mínimo de teste (não depende do T03); retomável (pula as células já gravadas).
- *Critérios de aceitação:*
  - `uv run lab05 collect --pilot` gera linhas no schema do T01.
  - Teste com um gerenciador "fake" (comando que só dorme e cria arquivos) valida tempo, disco e o schema.
- *Implementação:* `src/runner.py`, `src/metrics.py`, `tests/test_runner.py`.
- *Dependências:* #96 (T01)

#### T05 Executar Coleta Piloto (#100, Bernardo)
- *Objetivo:* Rodar a coleta piloto para validar o protocolo e medir a variância que alimenta a análise de poder.
- *Regras de negócio / restrições:*
  - 1 máquina (Bernardo), 6 tratamentos × cenários cold e warm-cache × 3 projetos × 5 repetições.
  - Seguir o protocolo do T07 (energia, Windows Update pausado, specs registradas).
  - Anotar problemas encontrados (tratamento que falha, tempo total por célula) para ajustar o protocolo.
- *Critérios de aceitação:*
  - `data/raw/pilot/runs.csv` + `specs.json` commitados até ~17/11.
  - Todas as linhas com `build_ok = true`, ou a falha explicada.
  - Tempo total do piloto registrado (base para estimar a coleta completa).
- *Implementação:* Execução + `docs/piloto.md`.
- *Dependências:* #97 (T02), #98 (T03), #99 (T04), #102 (T07)

#### T06 Escrever Proposta do Estudo (#101, Luísa)
- *Objetivo:* Escrever a proposta da S01: software, pergunta, caminhos, GQM, hipóteses e a primeira versão das 7 categorias.
- *Regras de negócio / restrições:*
  - Os 3 critérios (real, em operação, alto impacto) com números e fontes com data de acesso: downloads no npm, versão e data do último release de cada gerenciador, State of JS, Stack Overflow Survey.
  - Pergunta de pesquisa + os 2 caminhos (experimento controlado + dados de operação da API de downloads do npm), com a justificativa da combinação.
  - GQM no template de Basili; hipóteses H₀/H₁ (Todos × npm, Yarn × Yarn, promessas dos fabricantes).
  - 7 categorias da Aula 8, cada uma com justificativa.
  - Plano de análise resumido (testes, tamanho do efeito, poder) junto com o Pedro.
- *Critérios de aceitação:*
  - `docs/proposta.md` completo, revisado pelo trio.
- *Implementação:* `docs/proposta.md`.
- *Dependências:* Nenhuma.

#### T07 Escrever Protocolo de Coleta + Coletor de Specs (#102, Luísa)
- *Objetivo:* Padronizar como cada integrante coleta na própria máquina e registrar automaticamente as specs de cada bloco.
- *Regras de negócio / restrições:*
  - Checklist: na tomada, perfil de energia "Alto desempenho", Windows Update pausado, apps fechados, Defender no padrão (fixo), temperatura inicial.
  - `specs.py` grava CPU, núcleos, RAM, tipo e espaço do disco, versão do Windows e do Node em `data/raw/<maquina>/specs.json`.
  - Passo a passo de instalação dos 6 tratamentos nas versões fixadas.
- *Critérios de aceitação:*
  - `docs/protocolo.md` + `uv run lab05 specs` funcionando no Windows.
  - Usado no piloto (T05).
- *Implementação:* `docs/protocolo.md`, `src/specs.py`.
- *Dependências:* #96 (T01)

#### T08 Implementar Testes Estatísticos (#103, Pedro)
- *Objetivo:* Implementar a análise estatística usada nas abas, desenvolvida sobre o CSV sintético do T01.
- *Regras de negócio / restrições:*
  - Descritiva por célula: mediana, IQR, p90.
  - Todos × npm: Wilcoxon pareado (por máquina e repetição) de cada gerenciador contra o npm, com correção de Holm.
  - Yarn × Yarn: Friedman + post-hoc Wilcoxon com Holm.
  - Tamanho do efeito: Cliff's δ + speedup (razão das medianas) com IC 95% por bootstrap (padrão do `bootstrap_ci` do Lab04).
  - Bicaudal, α = 0,05.
- *Critérios de aceitação:*
  - `src/stats.py` validado contra `scipy.stats.wilcoxon` e `friedmanchisquare` em `tests/test_stats.py`.
- *Implementação:* `src/stats.py`, `tests/test_stats.py`.
- *Dependências:* #96 (T01)

#### T09 Calcular Nº de Repetições por Poder (#104, Pedro)
- *Objetivo:* Definir quantas repetições por célula a coleta completa precisa, usando a variância do piloto.
- *Regras de negócio / restrições:*
  - Simulação de poder no estilo do `sample_size.py` do Lab04: reamostrar os tempos do piloto, aplicar um efeito (ex.: speedup de 10%, 20%, 30%) e estimar o poder do Wilcoxon com Holm.
  - Desenvolver com dados sintéticos e plugar o piloto quando o T05 fechar.
  - Cruzar com o tempo total estimado (piloto) para ver se cabe até 23/11; se não couber, propor o corte (cenário reinstall ou um projeto).
- *Critérios de aceitação:*
  - `src/power.py` + `docs/poder.md` com o N escolhido e a justificativa, até 19/11.
- *Implementação:* `src/power.py`, `docs/poder.md`.
- *Dependências:* #103 (T08), #100 (T05)

#### T10 Construir Dashboard Base (#105, Pedro)
- *Objetivo:* Montar o esqueleto do dashboard Streamlit com as 4 abas, lendo o schema do T01.
- *Regras de negócio / restrições:*
  - Abas: Todos × npm · Yarn × Yarn · Adoção × desempenho · Impacto (+ página de método/links).
  - Lê `data/raw/*/runs.csv`; enquanto não há coleta, usa o CSV sintético e mostra um aviso.
  - Cores fixas por gerenciador, iguais em todas as abas; Plotly.
  - Deploy fica no T11 (Bernardo).
- *Critérios de aceitação:*
  - `uv run lab05` abre o dashboard com as 4 abas preenchidas pelos dados sintéticos.
- *Implementação:* `app.py`, `src/figures.py`.
- *Dependências:* #96 (T01)

### S02 — Coleta completa e análise (26/11)

#### T11 Publicar Dashboard no Streamlit Cloud (#106, Bernardo)
- *Objetivo:* Publicar o dashboard a partir do repositório clone do Bernardo, via git subtree, como no Lab04.
- *Regras de negócio / restrições:*
  - `deploy/requirements.txt` gerado do `uv.lock` (mesmo esquema e teste de divergência do Lab04).
  - O caminho com espaço (`Enunciado 5/`) não funciona no Cloud: publicar pelo clone com o conteúdo na raiz (subtree).
  - Link do dashboard no README, no PLAN.md e no artigo.
- *Critérios de aceitação:*
  - App público funcionando com os dados versionados; passo a passo em `deploy/README.md`.
- *Implementação:* `deploy/`.
- *Dependências:* #105 (T10)

#### T12a Executar Coleta Completa (máquina do Bernardo) (#107, Bernardo)
- *Objetivo:* Rodar a coleta completa na máquina do Bernardo, seguindo o protocolo e o N do T09.
- *Regras de negócio / restrições:*
  - Todos os tratamentos × cenários × projetos × N repetições, em ordem aleatorizada.
  - Seguir `docs/protocolo.md`; registrar `specs.json` e as anomalias.
  - Prazo interno: 23/11 (o T13 depende das 3 coletas).
- *Critérios de aceitação:*
  - `data/raw/bernardo/runs.csv` + `specs.json` commitados.
- *Implementação:* Execução.
- *Dependências:* #100 (T05), #102 (T07), #104 (T09)

#### T12b Executar Coleta Completa (máquina da Luísa) (#108, Luísa)
- *Objetivo:* Rodar a coleta completa na máquina da Luísa, seguindo o protocolo e o N do T09.
- *Regras de negócio / restrições:*
  - Todos os tratamentos × cenários × projetos × N repetições, em ordem aleatorizada.
  - Seguir `docs/protocolo.md`; registrar `specs.json` e as anomalias.
  - Prazo interno: 23/11 (o T13 depende das 3 coletas).
- *Critérios de aceitação:*
  - `data/raw/luisa/runs.csv` + `specs.json` commitados.
- *Implementação:* Execução.
- *Dependências:* #100 (T05), #102 (T07), #104 (T09)

#### T12c Executar Coleta Completa (máquina do Pedro) (#109, Pedro)
- *Objetivo:* Rodar a coleta completa na máquina do Pedro, seguindo o protocolo e o N do T09.
- *Regras de negócio / restrições:*
  - Todos os tratamentos × cenários × projetos × N repetições, em ordem aleatorizada.
  - Seguir `docs/protocolo.md`; registrar `specs.json` e as anomalias.
  - Prazo interno: 23/11 (o T13 depende das 3 coletas).
- *Critérios de aceitação:*
  - `data/raw/pedro/runs.csv` + `specs.json` commitados.
- *Implementação:* Execução.
- *Dependências:* #100 (T05), #102 (T07), #104 (T09)

#### T13 Validar e Versionar os Dados (#110, Bernardo)
- *Objetivo:* Juntar as 3 coletas, checar a qualidade e congelar o dataset usado na análise.
- *Regras de negócio / restrições:*
  - Checagens: células faltando, `build_ok = false`, `exit_code ≠ 0`, versões divergentes entre máquinas, outliers extremos (registrar, não apagar).
  - Gerar `data/processed/runs_all.csv` + manifesto sha256 (padrão do `data.py` do Lab04).
  - Relatório de validação em `docs/validacao.md`.
- *Critérios de aceitação:*
  - `uv run lab05 validate` passa; o dataset final está commitado e é o que o dashboard lê.
- *Implementação:* `src/validate.py`, `docs/validacao.md`.
- *Dependências:* #107 (T12a), #108 (T12b), #109 (T12c)

#### T14 Construir Análise + Aba Yarn × Yarn (#111, Bernardo)
- *Objetivo:* Comparar Yarn Classic, Berry (node-modules) e Berry (PnP): a evolução do mesmo software e o trade-off do PnP.
- *Regras de negócio / restrições:*
  - Friedman + post-hoc (de `stats.py`), Cliff's δ, por cenário e projeto.
  - Mostrar também disco e nº de arquivos (o PnP não cria `node_modules`) e a compatibilidade (`build_ok`).
  - Usa os dados do piloto até a coleta completa chegar.
- *Critérios de aceitação:*
  - Aba Yarn × Yarn com gráficos + texto interpretando o resultado.
- *Implementação:* `app.py` (aba), `src/figures.py`.
- *Dependências:* #103 (T08), #105 (T10)

#### T15 Coletar Downloads do npm (#112, Luísa)
- *Objetivo:* Coletar as séries históricas de downloads dos gerenciadores (2º caminho: dados de operação).
- *Regras de negócio / restrições:*
  - API pública `api.npmjs.org/downloads/range` para `npm`, `pnpm`, `yarn`, `@yarnpkg/cli`, `bun`; janela de vários anos, em blocos permitidos pela API.
  - ≤ 1 requisição/s; cache em CSV; data da coleta registrada.
  - Documentar a ameaça de construto: download do pacote `npm` ≠ uso do npm (ele já vem com o Node).
- *Critérios de aceitação:*
  - `data/npm_downloads/*.csv` + `docs/fonte_downloads.md`; `uv run lab05 downloads` reproduz.
- *Implementação:* `src/npm_downloads.py`.
- *Dependências:* #96 (T01)

#### T16 Construir Aba Adoção × Desempenho (#113, Luísa)
- *Objetivo:* Cruzar a adoção (downloads) com o desempenho medido: o mercado escolhe o mais rápido?
- *Regras de negócio / restrições:*
  - Séries temporais de downloads (absolutos e participação) + crescimento no último ano.
  - Gráfico de adoção × speedup em relação ao npm; análise descritiva (só 5 gerenciadores).
  - Texto com as limitações dessa comparação.
- *Critérios de aceitação:*
  - Aba Adoção × desempenho no dashboard.
- *Implementação:* `app.py` (aba), `src/figures.py`.
- *Dependências:* #105 (T10), #112 (T15)

#### T17 Escrever Ameaças à Validade + Esqueleto do Artigo (#114, Luísa)
- *Objetivo:* Escrever as ameaças dos 4 tipos e montar o esqueleto do artigo SBC com a seção de Método.
- *Regras de negócio / restrições:*
  - Ameaças de conclusão, interna, construto e externa, cada uma com mitigação (ex.: Defender fixo, Verdaccio × registry real, só Windows, lockfiles diferentes, Goodhart no tempo de instalação).
  - Artigo a partir de `Templates/SBC`, com seções e responsáveis; Método redigido.
- *Critérios de aceitação:*
  - `docs/ameacas.md` + `article/` compilando com a seção de Método.
- *Implementação:* `docs/ameacas.md`, `article/`.
- *Dependências:* #101 (T06)

#### T18 Construir Análise + Aba Todos × npm (#115, Pedro)
- *Objetivo:* Comparar cada gerenciador com o npm (controle) e conferir as promessas dos fabricantes.
- *Regras de negócio / restrições:*
  - Wilcoxon contra o controle com Holm, Cliff's δ e speedup com IC por cenário, projeto e máquina (de `stats.py`).
  - Comparar o speedup observado com o anunciado (página de benchmarks do pnpm, "até 25×" do Bun), com as fontes.
  - Disco e nº de arquivos ao lado do tempo; usa o piloto até a coleta completa chegar.
- *Critérios de aceitação:*
  - Aba Todos × npm com gráficos, tabela de testes e texto interpretando o resultado.
- *Implementação:* `app.py` (aba), `src/figures.py`.
- *Dependências:* #103 (T08), #105 (T10)

### S03 + Final — Impacto, artigo e apresentação (03/12)

#### T19 Executar Checagem no Registry Real (#116, Bernardo)
- *Objetivo:* Rodar uma coleta pequena contra o registry público para checar se o ranking muda fora do Verdaccio (validade externa).
- *Regras de negócio / restrições:*
  - Subconjunto: cenário cold e ci, 1 projeto, poucas repetições, 1 máquina.
  - Comparar o ranking com o da coleta local e discutir no artigo.
- *Critérios de aceitação:*
  - `data/raw/registry_real/runs.csv` + parágrafo em `docs/ameacas.md`.
- *Implementação:* Execução + `src/runner.py --registry public`.
- *Dependências:* #99 (T04)

#### T20 Estimar Impacto + Aba Impacto (#117, Pedro)
- *Objetivo:* Traduzir o resultado para o mundo real: horas e dinheiro de CI, e disco na máquina do dev.
- *Regras de negócio / restrições:*
  - Conta: speedup × execuções de CI × preço do minuto do GitHub Actions, com fontes públicas e data de acesso.
  - Cenário de disco (pnpm × npm em N projetos).
  - Seção "o que não dá para afirmar" (Windows ≠ Linux de CI, só 3 projetos).
- *Critérios de aceitação:*
  - Aba Impacto + `src/impact.py` com os parâmetros ajustáveis no dashboard.
- *Implementação:* `src/impact.py`, `app.py` (aba).
- *Dependências:* #115 (T18)

#### T21 Revisar 7 Categorias + Conclusões e Limitações (#118, Luísa)
- *Objetivo:* Revisar as 7 categorias com o estudo pronto e escrever as conclusões e limitações.
- *Regras de negócio / restrições:*
  - Cada categoria com justificativa à luz do que foi feito de fato.
  - Responder às 2 perguntas do enunciado: o que o estudo mostrou e o que isso significa para quem usa.
- *Critérios de aceitação:*
  - `docs/proposta.md` atualizado + `docs/conclusoes.md`.
- *Implementação:* Documentação.
- *Dependências:* #114 (T17)

#### T22a Escrever Artigo: Instrumentação, Setup e Reaproveitamento (#119, Bernardo)
- *Objetivo:* Escrever as seções do artigo sobre o ambiente, a instrumentação e o que foi reaproveitado dos labs anteriores.
- *Regras de negócio / restrições:*
  - Verdaccio, runner, métricas, protocolo, specs das 3 máquinas.
  - Reaproveitamento: Lab01 (coleta via API), Lab03 (DORA/lead time), Lab04 (poder, testes, dashboard).
- *Critérios de aceitação:*
  - Seções no `article/`, compilando.
- *Implementação:* `article/`.
- *Dependências:* #110 (T13)

#### T22b Escrever Artigo: Introdução, Método, Ameaças e Conclusão (#120, Luísa)
- *Objetivo:* Escrever introdução, método, ameaças e conclusão do artigo.
- *Regras de negócio / restrições:*
  - Introdução com os 3 critérios e os números de impacto; método com GQM, hipóteses e 7 categorias; ameaças dos 4 tipos; conclusão.
- *Critérios de aceitação:*
  - Seções no `article/`, compilando.
- *Implementação:* `article/`.
- *Dependências:* #118 (T21)

#### T22c Escrever Artigo: Resultados e Impacto (#121, Pedro)
- *Objetivo:* Escrever os resultados e a estimativa de impacto do artigo.
- *Regras de negócio / restrições:*
  - Descritiva, testes, tamanho do efeito e promessas dos fabricantes; Yarn × Yarn; adoção × desempenho; impacto e o que não dá para afirmar.
  - Figuras exportadas do dashboard.
- *Critérios de aceitação:*
  - Seções no `article/`, compilando.
- *Implementação:* `article/`.
- *Dependências:* #115 (T18), #117 (T20)

#### T23a Preparar Apresentação (bloco do Bernardo) (#122, Bernardo)
- *Objetivo:* Preparar a parte do Bernardo na apresentação de 10 min: software, ambiente, coleta e reaproveitamento.
- *Regras de negócio / restrições:*
  - Roteiro curto; cada integrante domina o todo (o professor pode perguntar qualquer parte).
- *Critérios de aceitação:*
  - Roteiro em `APRESENTACAO.md`, ensaiado.
- *Implementação:* `APRESENTACAO.md`.
- *Dependências:* #119 (T22a)

#### T23b Preparar Apresentação (bloco da Luísa) (#123, Luísa)
- *Objetivo:* Preparar a parte da Luísa na apresentação de 10 min: pergunta, método, 7 categorias, ameaças e adoção.
- *Regras de negócio / restrições:*
  - Roteiro curto; cada integrante domina o todo (o professor pode perguntar qualquer parte).
- *Critérios de aceitação:*
  - Roteiro em `APRESENTACAO.md`, ensaiado.
- *Implementação:* `APRESENTACAO.md`.
- *Dependências:* #120 (T22b)

#### T23c Preparar Apresentação (bloco do Pedro) (#124, Pedro)
- *Objetivo:* Preparar a parte do Pedro na apresentação de 10 min: resultados, promessas dos fabricantes e impacto.
- *Regras de negócio / restrições:*
  - Roteiro curto; cada integrante domina o todo (o professor pode perguntar qualquer parte).
- *Critérios de aceitação:*
  - Roteiro em `APRESENTACAO.md`, ensaiado.
- *Implementação:* `APRESENTACAO.md`.
- *Dependências:* #121 (T22c)

---

## Decisões técnicas

| Decisão | Valor |
|---|---|
| Controle | npm, o padrão que vem com o Node |
| Rede | Verdaccio local com cache; registry real só na checagem T19 |
| Validade da instalação | `build` do projeto após cada instalação (`build_ok`) |
| Disco | `node_modules` + cache/store, deduplicando hard links por `st_ino` |
| Testes | Wilcoxon contra o controle + Holm; Friedman no Yarn × Yarn; validados contra o scipy |
| Efeito | Cliff's δ + speedup com IC 95% por bootstrap |
| Dashboard | Streamlit + Plotly; mesma cor por gerenciador; deploy pelo clone do Bernardo (git subtree), porque o Cloud não aceita espaço no caminho |
| Documento | Artigo SBC (`Templates/SBC`) + dashboard |
| Reprodutibilidade | `uv.lock`, versões fixadas, semente fixa, dados versionados com manifesto sha256, `uv run lab05` |

---

## Riscos e mitigação

| Risco | Mitigação |
|---|---|
| S01 curta (até 19/11) com piloto obrigatório | Schema + CSV sintético no 1º dia (T01); T03 até ~16/11 e T05 até ~17/11 |
| Coleta completa não cabe no prazo | Tempo total estimado no piloto; o T09 propõe o corte (cenário reinstall ou um projeto) se N × células não couber até 23/11 |
| Algum tratamento falha no Windows (ex.: PnP no Next.js) | Registrar `build_ok = false` em vez de descartar; é resultado (compatibilidade) |
| Pouco disco nas máquinas | Limpar `node_modules` e caches entre células (o runner já faz); medir o espaço livre no `specs.json` |
| Ruído (Defender, processos em segundo plano) | Protocolo (T07), ordem aleatorizada, repetições, blocos por máquina |
| Downloads ≠ uso | Declarar como ameaça de construto (T15, T17) |
| Desconto por uso do GitHub Projects | Cartões atualizados, commits com `#issue`, evolução semanal visível |

---

## Como começar (S01)

```bash
cd "Enunciado 5"
uv sync
uv run pytest
uv run lab05          # lê os dados versionados (ou o CSV sintético) e abre o dashboard
```

## Issues no GitHub (label `Enunciado 5`, board "Kanban Lab")

Todo commit deve citar o número da Issue (ex.: `feat(runner): métricas de disco #99`).

| Tarefa | Issue | Responsável | Milestone |
|---|---|---|---|
| T01 Estruturar Projeto + Schema dos Dados | #96 | Bernardo (alvimdev) | SPRINT 1 (E5) |
| T02 Montar Registry Local (Verdaccio) | #97 | Bernardo (alvimdev) | SPRINT 1 (E5) |
| T03 Criar Projetos-Carga e Lockfiles | #98 | Luísa (luisajardim) | SPRINT 1 (E5) |
| T04 Implementar Runner de Instalação | #99 | Bernardo (alvimdev) | SPRINT 1 (E5) |
| T05 Executar Coleta Piloto | #100 | Bernardo (alvimdev) | SPRINT 1 (E5) |
| T06 Escrever Proposta do Estudo | #101 | Luísa (luisajardim) | SPRINT 1 (E5) |
| T07 Escrever Protocolo de Coleta + Coletor de Specs | #102 | Luísa (luisajardim) | SPRINT 1 (E5) |
| T08 Implementar Testes Estatísticos | #103 | Pedro (pedroseabra27) | SPRINT 1 (E5) |
| T09 Calcular Nº de Repetições por Poder | #104 | Pedro (pedroseabra27) | SPRINT 1 (E5) |
| T10 Construir Dashboard Base | #105 | Pedro (pedroseabra27) | SPRINT 1 (E5) |
| T11 Publicar Dashboard no Streamlit Cloud | #106 | Bernardo (alvimdev) | SPRINT 2 (E5) |
| T12a Executar Coleta Completa (máquina do Bernardo) | #107 | Bernardo (alvimdev) | SPRINT 2 (E5) |
| T12b Executar Coleta Completa (máquina da Luísa) | #108 | Luísa (luisajardim) | SPRINT 2 (E5) |
| T12c Executar Coleta Completa (máquina do Pedro) | #109 | Pedro (pedroseabra27) | SPRINT 2 (E5) |
| T13 Validar e Versionar os Dados | #110 | Bernardo (alvimdev) | SPRINT 2 (E5) |
| T14 Construir Análise + Aba Yarn × Yarn | #111 | Bernardo (alvimdev) | SPRINT 2 (E5) |
| T15 Coletar Downloads do npm | #112 | Luísa (luisajardim) | SPRINT 2 (E5) |
| T16 Construir Aba Adoção × Desempenho | #113 | Luísa (luisajardim) | SPRINT 2 (E5) |
| T17 Escrever Ameaças à Validade + Esqueleto do Artigo | #114 | Luísa (luisajardim) | SPRINT 2 (E5) |
| T18 Construir Análise + Aba Todos × npm | #115 | Pedro (pedroseabra27) | SPRINT 2 (E5) |
| T19 Executar Checagem no Registry Real | #116 | Bernardo (alvimdev) | SPRINT 3 / FINAL (E5) |
| T20 Estimar Impacto + Aba Impacto | #117 | Pedro (pedroseabra27) | SPRINT 3 / FINAL (E5) |
| T21 Revisar 7 Categorias + Conclusões e Limitações | #118 | Luísa (luisajardim) | SPRINT 3 / FINAL (E5) |
| T22a Escrever Artigo: Instrumentação, Setup e Reaproveitamento | #119 | Bernardo (alvimdev) | SPRINT 3 / FINAL (E5) |
| T22b Escrever Artigo: Introdução, Método, Ameaças e Conclusão | #120 | Luísa (luisajardim) | SPRINT 3 / FINAL (E5) |
| T22c Escrever Artigo: Resultados e Impacto | #121 | Pedro (pedroseabra27) | SPRINT 3 / FINAL (E5) |
| T23a Preparar Apresentação (bloco do Bernardo) | #122 | Bernardo (alvimdev) | SPRINT 3 / FINAL (E5) |
| T23b Preparar Apresentação (bloco da Luísa) | #123 | Luísa (luisajardim) | SPRINT 3 / FINAL (E5) |
| T23c Preparar Apresentação (bloco do Pedro) | #124 | Pedro (pedroseabra27) | SPRINT 3 / FINAL (E5) |
