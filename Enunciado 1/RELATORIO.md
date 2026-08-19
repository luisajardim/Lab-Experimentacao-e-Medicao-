# Relatório — Lab01: Características de Repositórios Populares

> Documento único do grupo (trio). Cada integrante escreve a hipótese, os
> resultados e a discussão da própria parte, seguindo a mesma estrutura usada
> abaixo para RQ01 e RQ04. Não crie um relatório separado por pessoa — edite
> este arquivo mesmo, substituindo os trechos marcados como `[preencher]`.
>
> Status atual: estamos na Sprint 2 (Lab01S02). Já temos o dataset final de
> 1.000 repositórios (`Miner/data/1000_popular_repos.csv`, Issue #8), e RQ01 e
> RQ04 já foram checadas em cima dele, com validação de consistência e
> outliers (Issue #9).

## Sumário

- [1. Introdução e hipóteses informais](#1-introdução-e-hipóteses-informais)
- [2. Metodologia de coleta](#2-metodologia-de-coleta)
- [3. Resultados e discussão por RQ](#3-resultados-e-discussão-por-rq)
- [4. Configuração do processo (GitHub Projects)](#4-configuração-do-processo-github-projects)

Link do repositório/GitHub Projects do grupo: `[preencher]`

---

## 1. Introdução e hipóteses informais

As hipóteses abaixo foram escritas antes de olharmos qualquer dado coletado —
a ideia é justamente poder comparar depois o que a gente imaginava com o que
os números de fato mostraram.

**RQ01 — Sistemas populares são maduros/antigos?**
A gente acha que sim. É difícil um repositório juntar milhares de estrelas de
um dia pro outro; isso normalmente vem de anos ganhando visibilidade e sendo
recomendado dentro da comunidade. Por isso esperamos ver poucos repositórios
com menos de um ou dois anos entre os mais estrelados, e bastante coisa
concentrada na faixa de 5 a 15 anos. Quando aparecer algum caso recente no
topo, imaginamos que seja algo que viralizou rápido ou pegou muita divulgação
de uma vez.

*Depois do dataset completo (Issues #8 e #9):* a hipótese se sustentou quase
sem ajuste. A única coisa que mudaria na redação é chamar os repositórios
jovens de "exceção" — os 13,9% com menos de 2 anos não aparecem como outlier
em nenhum teste estatístico (critério IQR), então não são um caso anômalo
isolado, são só a ponta mais nova de uma distribuição contínua, puxada
provavelmente pela onda de ferramentas de IA/agentes de código que surgiu em
2025-2026.

**RQ02 — Sistemas populares recebem muita contribuição externa?**
Hipótese: `[preencher — responsável pela RQ02]`

**RQ03 — Sistemas populares lançam releases com frequência?**
Hipótese: `[preencher — responsável pela RQ03]`

**RQ04 — Sistemas populares são atualizados com frequência?**
Achamos que sim, na maioria dos casos — mais visibilidade costuma trazer mais
gente contribuindo e, com isso, mais manutenção acontecendo. Mas também
esperamos um grupo menor de repositórios que continuam populares mesmo sem
receber atualização recente: coisas como listas `awesome-*`, materiais
educacionais ou ferramentas que já chegaram num ponto de maturidade e não
precisam mudar com frequência.

*Depois do dataset completo (Issues #8 e #9):* a parte da frequência se
confirmou até mais forte do que a gente esperava — a mediana real é de 2 dias,
bem mais rápido que o "dias/semanas" que tínhamos chutado. Já o segundo grupo
precisou de correção: não é principalmente lista `awesome-*` ou material
educacional como imaginamos. Olhando os 196 outliers (critério IQR, 19,6% do
dataset), os casos mais extremos são sobretudo ferramentas de software
descontinuadas oficialmente — `atom/atom`, que o GitHub parou de manter em
2022, e `adobe/brackets`, encerrado pela Adobe, são bons exemplos. Ou seja: o
grupo "estagnado" tem mais a ver com produto abandonado pelos mantenedores do
que com conteúdo que naturalmente não muda.

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

**RQ01 e RQ04** — usa a spec [`Miner/specs/github-rq1-rq4-v1.yaml`](Miner/specs/github-rq1-rq4-v1.yaml),
que extrai `createdAt` e `pushedAt` de cada repositório. Em cima disso,
`Miner/src/index.ts` calcula, no momento da coleta:
- `idade_anos` (RQ01): tempo entre `createdAt` e a data da coleta, em anos;
- `dias_desde_ultima_atualizacao` (RQ04): tempo entre `pushedAt` e a data da
  coleta, em dias.

Como rodar, como validamos manualmente e os detalhes da checagem de outliers
estão em [`Miner/docs/rq01-rq04.md`](Miner/docs/rq01-rq04.md).

**RQ05 / RQ06 / RQ07** — spec [`Miner/specs/github-search-v1.yaml`](Miner/specs/github-search-v1.yaml).
Extrai a linguagem primária (`primaryLanguage.name`) e a contagem de issues (`closed` e `total`).
- A métrica da **RQ05** é extraída e será cruzada com os dados do GitHub Octoverse;
- A métrica da **RQ06** e **RQ07** (`ratio_closed_issues`) é calculada dividindo `closed_issues` por `total_issues`.
Detalhes de execução e validação técnica individual da amostra (Sprint 1) estão em [`Miner/docs/rq05-rq07.md`](Miner/docs/rq05-rq07.md).

**RQ02 / RQ03** — `[preencher: spec usada, campos extraídos e como a métrica é calculada pelo Alvim]`

---

## 3. Resultados e discussão por RQ

### RQ01 — Idade do repositório

Números calculados em cima do dataset completo, os 1.000 repositórios de
`Miner/data/1000_popular_repos.csv`:

| Métrica | Valor |
|---|---|
| Repositórios | 1.000 (0 valores ausentes em `idade_anos`) |
| Mínimo | 0,02 anos |
| 1º quartil (Q1) | 3,50 anos |
| Mediana | 7,74 anos |
| 3º quartil (Q3) | 11,35 anos |
| Máximo | 18,36 anos |
| Média | 7,66 anos |

Por faixa etária:

| Faixa | Repositórios |
|---|---|
| até 1 ano | 82 (8,2%) |
| 1-2 anos | 57 (5,7%) |
| 2-5 anos | 185 (18,5%) |
| 5-10 anos | 331 (33,1%) |
| 10-15 anos | 296 (29,6%) |
| 15+ anos | 49 (4,9%) |

Pra checar outliers usamos o critério de Tukey: `Q1 - 1,5×IQR` e
`Q3 + 1,5×IQR`, com IQR = 7,85 anos, dá uma faixa de aceitação de mais ou
menos −8,3 a 23,1 anos. Como a idade não passa de ~18 anos em nenhum caso (o
GitHub existe desde 2008) e não tem como ser negativa, nenhum repositório
ficou fora dessa faixa — zero outliers.

**Discussão:** a hipótese se confirma. Mediana em 7,74 anos e média bem
próxima (7,66) indicam uma distribuição sem grande distorção, com a maior
parte dos repositórios concentrada entre 5 e 15 anos (62,7% do total). Só
13,9% têm menos de 2 anos, o que reforça que popularidade no GitHub costuma
levar tempo pra se construir. E como não apareceu nenhum outlier, essa
maturidade parece ser mesmo a regra entre os repositórios mais populares, não
um efeito puxado por um punhado de projetos muito antigos.

### RQ02 — Contribuição externa

**Resultado:** `[preencher — responsável pela RQ02]`

**Discussão:** `[preencher]`

### RQ03 — Frequência de releases

**Resultado:** `[preencher — responsável pela RQ03]`

**Discussão:** `[preencher]`

### RQ04 — Tempo desde a última atualização

Mesma base, os 1.000 repositórios:

| Métrica | Valor |
|---|---|
| Repositórios | 1.000 (0 valores ausentes em `dias_desde_ultima_atualizacao`) |
| Mínimo | 0 dias |
| 1º quartil (Q1) | 0 dias |
| Mediana | 2 dias |
| 3º quartil (Q3) | 48,25 dias |
| Máximo | 2.452 dias (~6,7 anos) |
| Média | 113,8 dias |

Por faixa:

| Faixa | Repositórios |
|---|---|
| até 1 dia | 477 (47,7%) |
| 2-7 dias | 132 (13,2%) |
| 8-30 dias | 118 (11,8%) |
| 31-90 dias | 64 (6,4%) |
| 91-365 dias | 94 (9,4%) |
| mais de 365 dias | 115 (11,5%) |

Aqui o IQR é 48,25 dias, o que dá um limite superior de aproximadamente 120,6
dias (`Q3 + 1,5×IQR`). Passando disso, 196 repositórios (19,6% do dataset)
entram como outliers — todos pra cima, já que não tem como um repositório
ficar "menos que zero" dias sem push. Os casos mais extremos:

| Repositório | Dias sem push |
|---|---|
| exacity/deeplearningbook-chinese | 2.452 |
| GitSquared/edex-ui | 1.765 |
| lib-pku/libpku | 1.688 |
| adobe/brackets | 1.529 |
| atom/atom | 1.324 |

Vale destacar `atom/atom` e `adobe/brackets`: são editores de código que o
GitHub e a Adobe descontinuaram oficialmente, mas que seguem com muitas
estrelas acumuladas mesmo sem receber commit há anos.

**Discussão:** a hipótese se confirma, e o segundo grupo previsto também
apareceu. A mediana de 2 dias mostra que quase metade dos repositórios
(47,7%) recebeu push no último dia — atividade praticamente diária. Mas a
média (113,8 dias) fica bem acima da mediana, o que denuncia uma distribuição
puxada por uma cauda longa de repositórios populares que pararam de ser
mantidos — os mesmos 19,6% que aparecem como outliers. Faz sentido: acumular
estrelas é algo que fica registrado, então um projeto pode continuar
"relevante" no GitHub muito tempo depois de os mantenedores terem abandonado
ele.

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
