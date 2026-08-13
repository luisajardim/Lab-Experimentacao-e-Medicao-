# Relatório — Lab01: Características de Repositórios Populares

> Documento único do grupo (trio). Cada integrante escreve a hipótese, os
> resultados e a discussão da própria parte, seguindo a mesma estrutura usada
> abaixo para RQ01 e RQ04. Não crie um relatório separado por pessoa — edite
> este arquivo mesmo, substituindo os trechos marcados como `[preencher]`.
>
> Status atual: rascunho da Sprint 1 (Lab01S01). RQ01 e RQ04 têm hipótese e um
> resultado preliminar, calculado sobre uma amostra individual de 100
> repositórios usada só para testar e validar a extração — não é ainda o
> dataset final de 1.000 repositórios (isso é entregável da Sprint 2).

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

**Resultado preliminar** (amostra individual de 100 repositórios, Sprint 1 —
não é o dataset final):

| Métrica | Valor |
|---|---|
| Repositórios na amostra | 100 |
| Idade mínima | 0,37 anos (~4 meses) |
| Idade mediana | 8,27 anos |
| Idade máxima | 16,96 anos |
| Repositórios com menos de 2 anos | 18 (18%) |

**Discussão:** os dados preliminares favorecem a hipótese. Uma mediana de
cerca de 8 anos e 3 meses mostra que a maior parte dos repositórios populares
já é razoavelmente madura, e apenas 18% da amostra tem menos de dois anos —
em geral, casos ligados a ferramentas de IA/agentes de código, que ganharam
popularidade muito rapidamente em 2025-2026. Ainda assim, a amplitude é grande
(de ~4 meses a quase 17 anos), então a conclusão definitiva depende da
distribuição completa com os 1.000 repositórios da Sprint 2.

### RQ02 — Contribuição externa

**Resultado:** `[preencher — responsável pela RQ02]`

**Discussão:** `[preencher]`

### RQ03 — Frequência de releases

**Resultado:** `[preencher — responsável pela RQ03]`

**Discussão:** `[preencher]`

### RQ04 — Tempo desde a última atualização

**Resultado preliminar** (mesma amostra de 100 repositórios):

| Métrica | Valor |
|---|---|
| Repositórios na amostra | 100 |
| Dias desde o último push — mínimo | 0 |
| Dias desde o último push — mediana | 1 |
| Dias desde o último push — máximo | 778 (~2 anos e 2 meses) |
| Repositórios sem push há mais de 90 dias | 13 (13%) |

**Discussão:** os dados também favorecem a hipótese. Uma mediana de apenas 1
dia sem push indica que a esmagadora maioria dos repositórios populares recebe
atividade quase diária. Ainda assim, 13% da amostra passa de 90 dias sem
atualização, o que sustenta a existência do segundo grupo previsto na
hipótese — repositórios populares porém estáveis, como material educacional e
listas `awesome-*`.

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
