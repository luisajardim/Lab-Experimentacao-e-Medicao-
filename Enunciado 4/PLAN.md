# PLAN.md — Lab04: Testes de Hipótese por Dentro (Pearson × Spearman)

> Protótipo de kanban e documento de referência para o grupo (Alvim, Luísa, Pedro).
> **Status:** passível de mudanças — editar via Issues do GitHub Projects.

---

## Visão geral

| Item | Valor |
|---|---|
| **Grupo** | Bernardo Alvim (A), Luísa Jardim (B), Pedro Seabra (C) |
| **Par de testes** | **P5 — Pearson × Spearman** |
| **Pergunta** | Em um sistema C++ da NASA, classes maiores tendem a ter mais defeitos de modo geral, ou a associação observada é puxada por poucas classes gigantes? |
| **Hipóteses** | H₀: ρ = 0 (não há associação entre LOC e nº de defeitos da classe) · H₁: ρ ≠ 0 (há associação) — **bicaudal**, α = 0,05. O grupo espera ρ > 0. |
| **Como a pergunta é respondida** | O teste de hipótese diz se há associação; a parte "tendência geral × poucas classes gigantes" é respondida comparando Pearson (sensível a valores extremos) com Spearman (baseado em postos) nos dados reais e na simulação |
| **Dados reais** | NASA MDP **KC1 por classe (C++)**, OpenML id 1070 (`kc1-numeric`), colunas `sumLOC_TOTAL` × `NUMDEFECTS`, 145 classes; **amostra de 30 classes** sorteada com `numpy.random.default_rng(42)` |
| **Stack** | Python 3.12 + uv · numpy/scipy/pandas · Plotly · Streamlit · pytest + ruff |
| **Repositório** | `Enunciado 4/` |
| **Entrada única** | `uv run lab04` → prepara dados → ajusta parâmetros → simula (com cache) → abre o dashboard |
| **Dashboard** | Streamlit, local (`uv run lab04`) + publicado no Streamlit Community Cloud |
| **Prazos** | **S01: 05/11/2026** · **S02 + Entrega final (dashboard + apresentação): 12/11/2026** |

### Por que KC1?

Benchmark feito na escolha do dataset (2.000 amostras de n = 30, semente 42):

| Dataset | n | % classes com 0 defeitos | máx. defeitos | r (Pearson) | ρ (Spearman) | % amostras n=30 significativas (Pearson / Spearman) |
|---|---|---|---|---|---|---|
| **KC1 (C++)** | 145 | 59% | 101 | 0,69 | 0,57 | 85% / 95% |
| AEEEM Equinox (Java) | 324 | 60% | 13 | 0,64 | 0,52 | 89% / 85% |
| AEEEM Eclipse JDT (Java) | 997 | 79% | 9 | 0,59 | 0,41 | 75% / 62% |
| AEEEM PDE / Mylyn / Lucene | 691–1862 | 86–91% | 9–28 | 0,20–0,28 | 0,16–0,27 | 19–39% / 11–30% |

KC1 tem assimetria forte, outliers e muitos empates em zero: no dataset inteiro o Pearson dá o maior
coeficiente (puxado pelos outliers), mas em amostras de 30 o Spearman detecta mais. É exatamente o
contraste que o lab quer investigar. Limitações (vão para o dashboard): dados de 2004, críticas
conhecidas à qualidade dos dados da NASA (Shepperd et al., 2013) e LOC da classe = soma do LOC dos métodos.

---

## Kanban por sprint (S01 → Final)

| Sprint | Membro A — Bernardo | Membro B — Luísa | Membro C — Pedro |
|---|---|---|---|
| **S01** (7 pt) | T01 scaffold + comando único · T04 gerador de dados simulados (cópula) · T07 dashboard base (7 seções) + deploy no Streamlit Cloud | T02 coleta do KC1 + amostra 30 + proveniência · T03 cenário (pergunta, H₀/H₁, parâmetros, expectativa) · T06a **G1** | T05 Pearson/Spearman vetorizados + aplicação a um dataset simulado com interpretação · T06b **G2** |
| **S02** (7 pt) | T08 motor de simulação (10.000 réplicas × 3 situações × 7 efeitos) · T14 extra: tamanho da amostra (opcional) | T10 poder (Q2/Q3) + **G4** · T11 seção 6: tabela dos dados reais | T09 erro tipo I (Q1/Q3) + **G3** · T12 seção 7: conclusão + seletor de α + revisão dos textos |
| **Final** (6 pt) | T13 apresentação: perguntas 9, 10, 11, 13, 15 | T13 apresentação: perguntas 1, 2, 3, 4, 14 | T13 apresentação: perguntas 5, 6, 7, 8, 12 |

> Papéis são uma **proposta**. Ajustes via Issues com `Assignee` por integrante.
> Regra do enunciado: em cada sprint, cada integrante é Assignee de ≥ 1 Issue com código commitado,
> e **todo commit referencia o número da Issue** (`#NN`).

**Risco de dependência na S02:** G3 e G4 dependem do motor de simulação (T08). Para não travar B e C,
T08 publica o **schema dos resultados no 1º dia da S02** e entrega uma rodada pequena (500 réplicas)
para os gráficos serem construídos em paralelo.

---

## Desenho da simulação

| Situação | Como os dados são gerados | n | Papel |
|---|---|---|---|
| **S-base** (bem-comportada) | Normal bivariada com correlação ρ | 30 | Cenário ideal para o Pearson |
| **S-real** (realista) | Cópula gaussiana com correlação latente ρ → LOC ~ lognormal e defeitos ~ binomial negativa, parâmetros ajustados no KC1 inteiro | 30 | "Dados como os reais": assimetria, outliers, zeros/empates (viola pressupostos do Pearson) |
| **S-real-n10** (amostra pequena) | Mesmo gerador da S-real | 10 | Violação por amostra pequena |

- **Tamanho do efeito (eixo do G4):** ρ latente da cópula ∈ {0; 0,1; 0,2; 0,3; 0,4; 0,5; 0,6}. Para cada valor,
  reportar também o r de Pearson e o ρ de Spearman populacionais resultantes (estimados numa amostra grande).
- **Réplicas:** 10.000 por (situação × efeito) → margem de Monte Carlo ≈ ±0,43 pp em torno de 5%.
- **Testes:** Pearson e Spearman bicaudais; p-valor pela distribuição t com n − 2 g.l. (implementação vetorizada,
  validada contra `scipy.stats.pearsonr`/`spearmanr`). Todos os p-valores são salvos, o que permite trocar α
  (0,05 ↔ 0,01) no dashboard sem re-simular.
- **Reprodutibilidade:** `numpy.random.default_rng(42)` com streams independentes por situação (`SeedSequence.spawn`).

---

## Tarefas detalhadas

### S01 — Dados reais, cenário, gerador, G1 e G2

#### T01 Estruturar Projeto
- *Objetivo:* Criar a estrutura base do projeto Python do Lab04 com dependências, testes e comando único.
- *Regras de negócio / restrições:*
  - Layout: `src/lab04/` (`data.py`, `fit.py`, `generate.py`, `stat_tests.py`, `simulate.py`, `figures.py`, `cli.py`), `app.py`, `data/real/`, `data/sim/`, `docs/`, `tests/`.
  - Python 3.12 mínimo; `uv` como gerenciador de ambiente e lock file.
  - Entrada única `uv run lab04` (entry point em `[project.scripts]`).
  - Semente fixa centralizada (ex.: `SEED = 42` em `src/lab04/config.py`).
- *Critérios de aceitação:*
  - `uv sync` instala sem erros; `uv run pytest` e `uv run ruff check` passam.
  - `README.md` com pré-requisitos e o comando único.
- *Implementação:* `pyproject.toml` com `[project]`, `[tool.ruff]`, `[tool.pytest.ini_options]`; `.gitignore`.
- *Dependências:* Nenhuma.

#### T02 Coletar Dados Reais (KC1)
- *Objetivo:* Obter a amostra real de LOC × defeitos e registrar a proveniência.
- *Regras de negócio / restrições:*
  - Fonte: OpenML id 1070 (`kc1-numeric`, PROMISE/NASA MDP), arquivo ARFF.
  - Colunas usadas: `sumLOC_TOTAL` (LOC da classe) e `NUMDEFECTS` (nº de defeitos da classe).
  - Salvar o dataset completo (145 classes) e a amostra de 30 classes sorteada com `default_rng(42)`.
  - Não é preciso pipeline: um script curto + CSV bastam.
- *Critérios de aceitação:*
  - `data/real/kc1_full.csv` e `data/real/kc1_sample30.csv`; rodar de novo gera a mesma amostra.
  - `docs/fonte_dados.md`: origem, URL, citação PROMISE, data da coleta, como foi coletado, descrição das colunas e limitações.
- *Implementação:* `src/lab04/data.py`.
- *Dependências:* T01.

#### T03 Definir Cenário
- *Objetivo:* Escrever o cenário completo do item (c) do enunciado.
- *Regras de negócio / restrições:*
  - Pergunta em uma frase (definida: "Em um sistema C++ da NASA, classes maiores tendem a ter mais defeitos de modo geral, ou a associação observada é puxada por poucas classes gigantes?"); H₀ e H₁ (bicaudal) em palavras simples.
  - Ajustar no KC1 inteiro: LOC ~ lognormal (média e desvio do log) e defeitos ~ binomial negativa (média e dispersão).
  - Justificar cada parâmetro com estatísticas dos dados reais (assimetria, % de zeros, mediana).
  - Registrar, **antes de simular**, qual teste o grupo espera que se saia melhor e por quê.
- *Critérios de aceitação:*
  - `docs/cenario.md` completo; parâmetros ajustados salvos em `data/real/params.json`.
- *Implementação:* `src/lab04/fit.py` + documentação.
- *Dependências:* T02.

#### T04 Implementar Gerador de Dados Simulados
- *Objetivo:* Gerar conjuntos de dados simulados para as três situações.
- *Regras de negócio / restrições:*
  - S-base: normal bivariada com correlação ρ.
  - S-real: cópula gaussiana (correlação latente ρ) → marginais lognormal (LOC) e binomial negativa (defeitos) com os parâmetros de `params.json`.
  - Assinatura vetorizada: `generate(situacao, rho, n, reps, rng) -> (x[reps, n], y[reps, n])`.
- *Critérios de aceitação:*
  - Testes: com ρ = 0 a correlação média é ≈ 0; marginais simuladas batem com os parâmetros ajustados; mesma semente ⇒ mesmos dados.
- *Implementação:* `src/lab04/generate.py` + `tests/test_generate.py`.
- *Dependências:* T01, T03.

#### T05 Implementar Testes de Pearson e Spearman
- *Objetivo:* Aplicar os dois testes de forma vetorizada e interpretar um exemplo.
- *Regras de negócio / restrições:*
  - Pearson: r, t = r·√((n−2)/(1−r²)), p bicaudal pela t com n−2 g.l.
  - Spearman: Pearson sobre os postos (empates por posto médio), mesmo cálculo de p.
  - Funcionar em lote (`[reps, n]`) para a simulação.
- *Critérios de aceitação:*
  - Testes comparam com `scipy.stats.pearsonr` e `spearmanr` (tolerância numérica).
  - Os dois testes aplicados a **um** conjunto simulado (S-real, ρ escolhido) com texto de interpretação do resultado.
- *Implementação:* `src/lab04/stat_tests.py` + `tests/test_stat_tests.py`.
- *Dependências:* T01.

#### T06a Construir Gráfico G1
- *Objetivo:* Mostrar os dados reais ao lado dos simulados.
- *Regras de negócio / restrições:*
  - Histograma de cada variável (LOC em escala log; defeitos), real (n = 30, e o KC1 inteiro como referência) × simulado (S-real).
  - Título, eixos com nome e unidade, legenda.
  - Texto de 2–4 frases: forma dos dados (assimetria, outliers, zeros) e por que os parâmetros foram escolhidos assim.
- *Critérios de aceitação:* G1 renderizado na seção 2 do dashboard.
- *Implementação:* `src/lab04/figures.py` (`fig_g1`).
- *Dependências:* T04, T07.

#### T06b Construir Gráfico G2
- *Objetivo:* Mostrar como os testes funcionam por dentro.
- *Regras de negócio / restrições:*
  - Distribuição da estatística t sob H₀ (curva teórica t(n−2) + histograma da nula simulada de cada teste).
  - Região de rejeição bicaudal sombreada (|t| > t crítico) e p-valor do exemplo (T05) marcado como área.
  - Mesma cor para cada teste em todos os gráficos.
  - Texto: o que cada teste compara, onde fica a região de rejeição e o que significa (e o que não significa) o p-valor.
- *Critérios de aceitação:* G2 renderizado na seção 3 do dashboard.
- *Implementação:* `src/lab04/figures.py` (`fig_g2`).
- *Dependências:* T05, T07.

#### T07 Construir Dashboard Base + Deploy
- *Objetivo:* Esqueleto do dashboard com as 7 seções na ordem do enunciado, publicado desde a S01.
- *Regras de negócio / restrições:*
  - Seções: 1 Cenário · 2 Os dados (G1) · 3 Como os testes funcionam (G2) · 4 Erro tipo I (G3) · 5 Poder (G4) · 6 Dados reais (tabela) · 7 Conclusão.
  - Link do dashboard e do repositório/GitHub Projects no topo.
  - Paleta fixa: uma cor para Pearson e outra para Spearman, compartilhada por todos os gráficos.
  - Deploy no Streamlit Community Cloud cedo, para validar o caminho `Enunciado 4/app.py` (há espaço no nome da pasta).
- *Critérios de aceitação:*
  - `uv run lab04` abre o dashboard localmente; URL pública funcionando; G1 e G2 visíveis ao fim da S01.
- *Implementação:* `app.py`, `src/lab04/cli.py`.
- *Dependências:* T01.

### S02 — Simulações Q1–Q3, G3, G4 e entrega final

#### T08 Implementar Motor de Simulação
- *Objetivo:* Rodar as simulações de Monte Carlo das perguntas Q1, Q2 e Q3.
- *Regras de negócio / restrições:*
  - 10.000 réplicas × 3 situações × 7 efeitos (ρ = 0; 0,1; …; 0,6); semente fixa com streams por situação.
  - Salvar todos os p-valores (para trocar α no dashboard) em `data/sim/` e commitar (o Cloud não re-simula).
  - Cache: não re-simular se parâmetros e semente não mudaram.
  - **Publicar o schema dos resultados no 1º dia** e uma rodada de 500 réplicas para T09/T10.
  - Estimar r e ρ_s populacionais para cada ρ latente (amostra grande).
- *Critérios de aceitação:*
  - `uv run lab04` regenera os mesmos resultados; tempo total de simulação documentado no README.
- *Implementação:* `src/lab04/simulate.py`.
- *Dependências:* T04, T05.

#### T09 Avaliar Erro Tipo I + Gráfico G3
- *Objetivo:* Responder Q1 (e a parte de Q3 sobre erro tipo I).
- *Regras de negócio / restrições:*
  - Proporção de p < α com ρ = 0 em cada situação, para os dois testes.
  - Linha em 5% e faixa de Monte Carlo (±0,43 pp).
  - Texto: se cada teste ficou perto de 5% em cada situação, qual se desviou, se ficou liberal ou conservador e por quê.
- *Critérios de aceitação:* G3 renderizado na seção 4.
- *Implementação:* `src/lab04/figures.py` (`fig_g3`).
- *Dependências:* T08.

#### T10 Avaliar Poder + Gráfico G4
- *Objetivo:* Responder Q2 (e a parte de Q3 sobre poder).
- *Regras de negócio / restrições:*
  - Curvas de poder dos dois testes no mesmo gráfico: proporção de rejeições × ρ latente (≥ 5 efeitos começando em 0), uma curva por situação.
  - Anotar r e ρ_s populacionais correspondentes a cada ρ latente.
  - Texto: qual teste detecta melhor o efeito e em que situações a vantagem muda de lado.
- *Critérios de aceitação:* G4 renderizado na seção 5.
- *Implementação:* `src/lab04/figures.py` (`fig_g4`).
- *Dependências:* T08.

#### T11 Aplicar Testes aos Dados Reais
- *Objetivo:* Seção 6 do dashboard.
- *Regras de negócio / restrições:*
  - Na amostra de 30: estatística (r, ρ_s, t), p-valor, tamanho do efeito com IC 95% (Fisher z para r; bootstrap para ρ_s) e conclusão de cada teste.
  - Comentar a importância prática do efeito (pergunta 14).
- *Critérios de aceitação:* Tabela renderizada na seção 6.
- *Implementação:* `src/lab04/stat_tests.py` + `app.py`.
- *Dependências:* T02, T05.

#### T12 Escrever Conclusão + Seletor de α
- *Objetivo:* Fechar o dashboard.
- *Regras de negócio / restrições:*
  - Seção 7: o que o grupo esperava (T03) × o que encontrou; recomendação de qual teste usar e quando a escolha mudaria; principal limitação.
  - Seletor α ∈ {0,05; 0,01} afetando G3 e G4 (pergunta 12).
  - Revisar todos os textos (2–4 frases por gráfico) e a checagem visual: título, eixos com unidade, legenda, mesma cor por teste.
- *Critérios de aceitação:* Dashboard completo se explicando sozinho, sem relatório.
- *Implementação:* `app.py`.
- *Dependências:* T09, T10, T11.

#### T13 Preparar Apresentação (uma Issue por membro)
- *Objetivo:* Responder às 15 perguntas em até 7 minutos usando o dashboard.
- *Regras de negócio / restrições:*
  - Respostas curtas (~30 s cada); cada integrante responde ≥ 4 perguntas, mas todos devem saber responder qualquer uma.
  - Divisão: **A** 9, 10, 11, 13, 15 · **B** 1, 2, 3, 4, 14 · **C** 5, 6, 7, 8, 12.
  - Pelo menos um ensaio cronometrado antes de 12/11.
- *Critérios de aceitação:* `APRESENTACAO.md` com o roteiro (pergunta → seção/gráfico do dashboard → resposta curta).
- *Dependências:* T12.

#### T14 Discutir Tamanho da Amostra (opcional)
- *Objetivo:* Enriquecer o dashboard com a seção 6 do enunciado ("Para discutir").
- *Regras de negócio / restrições:*
  - Poder de cada teste com n = 30 para o efeito observado nos dados reais.
  - n necessário para 80% de poder (simulação variando n) e se isso é viável no cenário real.
- *Critérios de aceitação:* Bloco extra no dashboard, sem atrasar T08–T12.
- *Dependências:* T08.

---

## Decisões técnicas

| Decisão | Valor |
|---|---|
| Dados reais | KC1 por classe (OpenML 1070); amostra de 30 com `default_rng(42)`; parâmetros ajustados no dataset inteiro |
| Gerador | Cópula gaussiana → lognormal (LOC) + binomial negativa (defeitos); S-base normal bivariada |
| Efeito | ρ latente ∈ {0; 0,1; …; 0,6}, com r e ρ_s populacionais reportados |
| Testes | Bicaudais, α = 0,05 (seletor 0,01); p pela t(n−2), validado contra scipy |
| Simulação | 10.000 réplicas por célula, vetorizada, p-valores salvos em `data/sim/` |
| Dashboard | Streamlit + Plotly; mesma cor por teste; links no topo; Streamlit Community Cloud |
| Reprodutibilidade | `uv.lock`, semente fixa, comando único `uv run lab04` |

---

## Riscos e mitigação

| Risco | Mitigação |
|---|---|
| S01 curta (até 05/11) | T02/T05/T01 começam em paralelo no 1º dia; T04 só depende de `params.json` (T03) |
| G3/G4 travados pelo motor (T08) | Schema + rodada de 500 réplicas no 1º dia da S02 |
| Deploy no Cloud falhar por causa do caminho com espaço | Deploy já na S01 (T07); se falhar, usar `requirements.txt` na pasta e/ou ajustar o caminho do app |
| Efeito no eixo X favorecer um teste | ρ latente comum aos dois testes, com r e ρ_s populacionais anotados |
| Qualidade dos dados NASA | Citar Shepperd et al. (2013) nas limitações; os dados reais só calibram a simulação |
| Desconto por uso do GitHub Projects | WIP respeitado, cartões atualizados, commits com `#issue`, evolução semanal visível |

---

## Como começar (S01)

```bash
cd "/home/alvim/github/Lab-Experimentacao-e-Medicao-/Enunciado 4"
uv sync
uv run pytest
uv run lab04          # prepara dados, simula (com cache) e abre o dashboard
```

## Issues no GitHub (label `Enunciado 4`, board "Kanban Lab")

Todo commit deve citar o número da Issue (ex.: `feat(generate): cópula gaussiana #78`).

| Tarefa | Issue | Responsável | Milestone |
|---|---|---|---|
| T01 Estruturar Projeto | #75 | A (alvimdev) | SPRINT 1 (E4) |
| T02 Coletar Dados Reais (KC1) | #76 | B (luisajardim) | SPRINT 1 (E4) |
| T03 Definir Cenário | #77 | B (luisajardim) | SPRINT 1 (E4) |
| T04 Implementar Gerador de Dados Simulados | #78 | A (alvimdev) | SPRINT 1 (E4) |
| T05 Implementar Testes de Pearson e Spearman | #79 | C (pedroseabra27) | SPRINT 1 (E4) |
| T06a Construir Gráfico G1 | #80 | B (luisajardim) | SPRINT 1 (E4) |
| T06b Construir Gráfico G2 | #81 | C (pedroseabra27) | SPRINT 1 (E4) |
| T07 Construir Dashboard Base + Deploy | #82 | A (alvimdev) | SPRINT 1 (E4) |
| T08 Implementar Motor de Simulação | #83 | A (alvimdev) | SPRINT 2 / FINAL (E4) |
| T09 Avaliar Erro Tipo I + Gráfico G3 | #84 | C (pedroseabra27) | SPRINT 2 / FINAL (E4) |
| T10 Avaliar Poder + Gráfico G4 | #85 | B (luisajardim) | SPRINT 2 / FINAL (E4) |
| T11 Aplicar Testes aos Dados Reais | #86 | B (luisajardim) | SPRINT 2 / FINAL (E4) |
| T12 Escrever Conclusão + Seletor de α | #87 | C (pedroseabra27) | SPRINT 2 / FINAL (E4) |
| T13 Preparar Apresentação (9, 10, 11, 13, 15) | #88 | A (alvimdev) | SPRINT 2 / FINAL (E4) |
| T13 Preparar Apresentação (1, 2, 3, 4, 14) | #89 | B (luisajardim) | SPRINT 2 / FINAL (E4) |
| T13 Preparar Apresentação (5, 6, 7, 8, 12) | #90 | C (pedroseabra27) | SPRINT 2 / FINAL (E4) |
| T14 Discutir Tamanho da Amostra (opcional) | #91 | A (alvimdev) | SPRINT 2 / FINAL (E4) |
