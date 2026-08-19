# Relatório — Lab01: Características de Repositórios Populares

> Documento único do grupo (trio). Cada integrante escreve a hipótese, os
> resultados e a discussão da própria parte, seguindo a mesma estrutura usada
> abaixo para RQ01 e RQ04. Não crie um relatório separado por pessoa — edite
> este arquivo mesmo, substituindo os trechos marcados como `[preencher]`.
>
> Status atual: Sprint 2 (Lab01S02). O dataset final de 1.000 repositórios foi
> coletado (`Miner/data/1000_popular_repos.csv`, Issue #8). RQ01 e RQ04 já têm
> resultado final sobre esse dataset completo, com validação de consistência e
> outliers (Issue #9).

## Sumário

- [1. Introdução e hipóteses informais](#1-introdução-e-hipóteses-informais)
- [2. Metodologia de coleta](#2-metodologia-de-coleta)
- [3. Resultados e discussão por RQ](#3-resultados-e-discussão-por-rq)
- [4. Configuração do processo (GitHub Projects)](#4-configuração-do-processo-github-projects)

Link do repositório/GitHub Projects do grupo: `[preencher]`

---

## 1. Introdução e hipóteses informais

Estas hipóteses foram escritas antes de qualquer análise dos dados coletados,
como ponto de partida para depois compararmos com o que os números realmente
mostram.

**RQ01 — Sistemas populares são maduros/antigos?**
Nossa expectativa é que sim. Um repositório dificilmente acumula milhares de
estrelas da noite para o dia: normalmente essa popularidade se constrói ao
longo de anos, conforme o projeto ganha visibilidade, uso recorrente e
recomendações dentro da comunidade. Por isso esperamos encontrar poucos
repositórios com menos de um ou dois anos de vida entre os mais estrelados, e
uma concentração maior na faixa de 5 a 15 anos. Os casos recentes que ainda
assim aparecem no topo provavelmente são exceções — algo que viralizou muito
rápido ou recebeu forte divulgação externa.

**RQ02 — Sistemas populares recebem muita contribuição externa?**
Hipótese: `[preencher — responsável pela RQ02]`

**RQ03 — Sistemas populares lançam releases com frequência?**
Hipótese: `[preencher — responsável pela RQ03]`

**RQ04 — Sistemas populares são atualizados com frequência?**
Acreditamos que a maioria está sim sendo atualizada com frequência, já que
mais visibilidade tende a atrair mais colaboradores e, consequentemente, mais
atividade de manutenção. Ao mesmo tempo, esperamos um grupo menor — mas não
desprezível — de repositórios que continuam populares sem receber atualizações
recentes: normalmente listas de recursos (`awesome-*`), materiais educacionais
ou ferramentas que já atingiram um estado de maturidade e não precisam de
mudanças constantes.

**RQ05 — Sistemas populares são escritos nas linguagens mais populares?**
Hipótese: Sim. Baseando-se no **GitHub Octoverse**, linguagens como JavaScript, Python e TypeScript dominam o ecossistema. Esperamos que a maior parte dos repositórios populares utilize essas tecnologias, visto que comunidades grandes impulsionam projetos massivos.

**RQ06 — Sistemas populares possuem um alto percentual de issues fechadas?**
Hipótese: Sim. Sistemas muito populares costumam ter ferramentas de CI/CD bem estabelecidas, automações de triagem e muitos colaboradores (mantenedores e comunidade), o que acelera a resolução de bugs e fechamento de issues.

**RQ07 — Sistemas em linguagens mais populares recebem mais contribuição, lançam mais releases e são atualizados com mais frequência?**
Hipótese: Sim. Ecossistemas consolidados (como JS/TS e Python) possuem um fluxo de desenvolvimento muito dinâmico. Repositórios nessas linguagens tendem a ter mais PRs (contribuições externas) e serem atualizados com maior constância do que sistemas escritos em linguagens menos populares ou legadas.

---

## 2. Metodologia de coleta

A coleta é feita pelo subprojeto `Miner`, que consulta a API GraphQL do
GitHub a partir de especificações declarativas (arquivos `.yaml` em
`Miner/specs/`), sem depender de bibliotecas de terceiros para acessar a API —
a query é escrita e consumida por um script próprio do grupo, conforme exigido
no enunciado.

Nesta sprint (S01), cada integrante criou uma spec pequena, focada apenas nos
campos da sua parte, para implementar e validar a extração antes de integrar
ao script único do grupo (essa integração final, com paginação para os 1.000
repositórios, é entregável da Sprint 2).

**RQ01 e RQ04** — spec [`Miner/specs/github-rq1-rq4-v1.yaml`](Miner/specs/github-rq1-rq4-v1.yaml).
Extrai `createdAt` e `pushedAt` de cada repositório e calcula, no momento da
coleta (`Miner/src/index.ts`):
- `idade_anos` (RQ01) = tempo entre `createdAt` e a data da coleta, em anos;
- `dias_desde_ultima_atualizacao` (RQ04) = tempo entre `pushedAt` e a data da
  coleta, em dias.

Detalhes de execução e validação técnica estão em
[`Miner/docs/rq01-rq04.md`](Miner/docs/rq01-rq04.md).

**RQ05 / RQ06 / RQ07** — spec [`Miner/specs/github-search-v1.yaml`](Miner/specs/github-search-v1.yaml).
Extrai a linguagem primária (`primaryLanguage.name`) e a contagem de issues (`closed` e `total`).
- A métrica da **RQ05** é extraída e será cruzada com os dados do GitHub Octoverse;
- A métrica da **RQ06** e **RQ07** (`ratio_closed_issues`) é calculada dividindo `closed_issues` por `total_issues`.
Detalhes de execução e validação técnica individual da amostra (Sprint 1) estão em [`Miner/docs/rq05-rq07.md`](Miner/docs/rq05-rq07.md).

**RQ02 / RQ03** — `[preencher: spec usada, campos extraídos e como a métrica é calculada pelo Alvim]`

---

## 3. Resultados e discussão por RQ

### RQ01 — Idade do repositório

**Resultado final** (dataset completo, 1.000 repositórios —
`Miner/data/1000_popular_repos.csv`):

| Métrica | Valor |
|---|---|
| Repositórios | 1.000 (0 valores ausentes em `idade_anos`) |
| Mínimo | 0,02 anos |
| 1º quartil (Q1) | 3,50 anos |
| Mediana | 7,74 anos |
| 3º quartil (Q3) | 11,35 anos |
| Máximo | 18,36 anos |
| Média | 7,66 anos |

Distribuição por faixa etária:

| Faixa | Repositórios |
|---|---|
| até 1 ano | 82 (8,2%) |
| 1-2 anos | 57 (5,7%) |
| 2-5 anos | 185 (18,5%) |
| 5-10 anos | 331 (33,1%) |
| 10-15 anos | 296 (29,6%) |
| 15+ anos | 49 (4,9%) |

**Outliers (método IQR/Tukey):** limites calculados como `Q1 - 1,5×IQR` e
`Q3 + 1,5×IQR` (IQR = Q3 − Q1 = 7,85 anos), resultando em uma faixa aceitável
de aproximadamente −8,3 a 23,1 anos. Como nenhum repositório do GitHub pode
ter mais de ~18 anos (a plataforma foi lançada em 2008) e o mínimo teórico é
0, **nenhum repositório caiu fora desses limites — zero outliers**. A
distribuição de idade é bem comportada, sem valores extremos anômalos.

**Discussão:** o dataset completo confirma a hipótese. A mediana de 7,74 anos
e média muito próxima (7,66) mostram uma distribuição sem grande assimetria —
a maioria dos repositórios populares está concentrada nas faixas de 5 a 15
anos (62,7% do total). Apenas 13,9% têm menos de 2 anos, o que sustenta a
ideia de que popularidade no GitHub se constrói ao longo de vários anos, não
da noite para o dia. A ausência de outliers estatísticos reforça que essa
maturidade é a norma entre os repositórios mais populares, não uma tendência
distorcida por alguns poucos projetos muito antigos.

### RQ02 — Contribuição externa

**Resultado:** `[preencher — responsável pela RQ02]`

**Discussão:** `[preencher]`

### RQ03 — Frequência de releases

**Resultado:** `[preencher — responsável pela RQ03]`

**Discussão:** `[preencher]`

### RQ04 — Tempo desde a última atualização

**Resultado final** (dataset completo, 1.000 repositórios):

| Métrica | Valor |
|---|---|
| Repositórios | 1.000 (0 valores ausentes em `dias_desde_ultima_atualizacao`) |
| Mínimo | 0 dias |
| 1º quartil (Q1) | 0 dias |
| Mediana | 2 dias |
| 3º quartil (Q3) | 48,25 dias |
| Máximo | 2.452 dias (~6,7 anos) |
| Média | 113,8 dias |

Distribuição por faixa:

| Faixa | Repositórios |
|---|---|
| até 1 dia | 477 (47,7%) |
| 2-7 dias | 132 (13,2%) |
| 8-30 dias | 118 (11,8%) |
| 31-90 dias | 64 (6,4%) |
| 91-365 dias | 94 (9,4%) |
| mais de 365 dias | 115 (11,5%) |

**Outliers (método IQR/Tukey):** IQR = Q3 − Q1 = 48,25 dias, limite superior
= `Q3 + 1,5×IQR` ≈ **120,6 dias**. **196 repositórios (19,6%) são outliers**
por esse critério — todos no lado superior (não há outliers baixos, já que o
valor mínimo possível é 0). Os casos mais extremos são projetos populares e
conhecidamente abandonados ou descontinuados:

| Repositório | Dias sem push |
|---|---|
| exacity/deeplearningbook-chinese | 2.452 |
| GitSquared/edex-ui | 1.765 |
| lib-pku/libpku | 1.688 |
| adobe/brackets | 1.529 |
| atom/atom | 1.324 |

`atom/atom` e `adobe/brackets` são particularmente ilustrativos: são editores
de código que o GitHub e a Adobe descontinuaram oficialmente, mas que
continuam populares (muitas estrelas herdadas) mesmo sem receber commits há
anos.

**Discussão:** o dataset completo confirma a hipótese, incluindo o segundo
grupo previsto. A mediana de apenas 2 dias mostra que quase metade dos
repositórios (47,7%) foi atualizada no último dia — atividade quase contínua.
Mas a média (113,8 dias) muito acima da mediana revela uma distribuição
fortemente assimétrica à direita: existe uma cauda longa de repositórios
populares e abandonados, confirmada pelos 19,6% classificados como outliers
estatísticos. Isso é coerente com a hipótese original — popularidade não
implica manutenção contínua; um repositório pode acumular estrelas ao longo
dos anos e continuar relevante/referenciado mesmo depois de abandonado pelos
mantenedores.

### RQ05 — Linguagem primária

**Resultado preliminar** (amostra de 80 repositórios processados com sucesso antes do timeout do GitHub):

| Linguagem | Contagem |
|---|---|
| Python | 22 |
| TypeScript | 14 |
| Não definida (N/A) | 11 |
| JavaScript | 7 |
| Shell | 4 |

**Discussão:** A hipótese se provou verdadeira nesta amostra. Python, TypeScript e JavaScript compõem a imensa maioria dos projetos populares, batendo perfeitamente com a tendência mundial do *GitHub Octoverse*. Projetos em C/C++ ou Java apareceram, mas em menor escala.

### RQ06 — Percentual de issues fechadas

**Resultado preliminar** (amostra de 80 repositórios):
- Razão Mínima: 0.0 (repositórios sem aba de issues ativa, ex: torvalds/linux)
- Razão Mediana: **0.887 (88,7%)**
- Razão Máxima: 1.0 (100% de issues fechadas)

**Discussão:** A hipótese também foi confirmada fortemente. Uma mediana de ~89% demonstra que as equipes que mantêm repositórios altamente populares são extremamente ativas na triagem e no fechamento de issues (sejam por meio de correções, PRs linkadas, ou arquivamento de *stale issues*).

### RQ07 — Cruzamento por linguagem (RQ02, RQ03 e RQ04 por linguagem)

**Resultado:** `[preencher na Sprint 2 — depende do CSV final contendo os cruzamentos de RQ02, RQ03 e RQ04 que serão integrados no script único do grupo]`

**Discussão:** Esta métrica complexa será discutida na próxima Sprint, quando o volume de 1.000 repositórios estiver disponível para cruzamento de dados sem sofrer com timeouts da API.

---

## 4. Configuração do processo (GitHub Projects)

`[preencher: colunas do board (Status), política e justificativa do limite de
WIP, e ao final do laboratório um print do board mostrando o fluxo completo.]`
