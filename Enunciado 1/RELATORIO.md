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
Hipótese: `[preencher — responsável pela RQ05]`
*(lembrem de definir e citar a fonte usada para "linguagens mais populares" —
ex.: TIOBE Index, GitHut ou Octoverse do GitHub — e manter a mesma referência
no restante do laboratório.)*

**RQ06 — Sistemas populares possuem um alto percentual de issues fechadas?**
Hipótese: `[preencher — responsável pela RQ06]`

**RQ07 — Sistemas em linguagens mais populares recebem mais contribuição, lançam mais releases e são atualizados com mais frequência?**
Hipótese: `[preencher — responsável pela RQ07]`

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

**RQ02 / RQ03 / RQ05 / RQ06 / RQ07** — `[preencher: spec usada, campos extraídos e como a métrica é calculada]`

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

**Resultado:** `[preencher — responsável pela RQ05]`

**Discussão:** `[preencher]`

### RQ06 — Percentual de issues fechadas

**Resultado:** `[preencher — responsável pela RQ06]`

**Discussão:** `[preencher]`

### RQ07 — Cruzamento por linguagem (RQ02, RQ03 e RQ04 por linguagem)

**Resultado:** `[preencher — depende dos resultados de RQ02, RQ03 e RQ04]`

**Discussão:** `[preencher]`

---

## 4. Configuração do processo (GitHub Projects)

`[preencher: colunas do board (Status), política e justificativa do limite de
WIP, e ao final do laboratório um print do board mostrando o fluxo completo.]`
