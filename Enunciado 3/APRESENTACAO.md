# Mineração de métricas DORA em repositórios open-source

## O quanto podemos confiar nos proxies?

**Grupo:** Bernardo Souza Alvim · Luísa Oliveira Jardim · Pedro Augusto Santos Seabra  
**Disciplina:** Laboratório de Experimentação de Software  
**Professor:** Danilo Maia  
**Repositório:** [Lab-Experimentacao-e-Medicao-](https://github.com/luisajardim/Lab-Experimentacao-e-Medicao-) · artigo completo em `Enunciado 3/RELATORIO.pdf`

---

# 1. O problema e o método

> O GitHub não registra deploy nem falha em produção. Medimos por **proxies** e testamos o quanto dá para confiar neles.

As quatro métricas DORA medem velocidade e estabilidade da entrega:

| Métrica DORA | Proxy usado |
| :--- | :--- |
| Deployment frequency | releases publicadas por semana |
| Lead time for changes | release − data do commit |
| Change failure rate | (a) runs de CI com falha · (b) release seguida de correção em até 7 dias |
| Tempo de recuperação | da primeira falha de CI até o próximo sucesso |

## Como medimos

- **Coleta própria:** usamos as APIs REST e GraphQL do GitHub, sem bibliotecas prontas.
- **Amostra:** 12.000 resultados de busca → 761 elegíveis (≥ 5 releases e ≥ 50 runs em 12 meses) → **315 repositórios**, sorteados com semente fixa.
- **Janela:** de out/2025 a set/2026, só no *default branch*, só runs disparados por `push`.
- **O que conta como falha:** `failure`, `timed_out` e `startup_failure`. Os runs `cancelled` e `skipped` são ignorados.
- **Censura:** um episódio de falha que não termina dentro da janela é contado como **censurado**, e não descartado. Descartá-lo faria a recuperação parecer mais rápida.
- **Estatística:** reportamos mediana e IQR, e usamos só testes não paramétricos:
  - **Spearman** na RQ05;
  - **Kruskal-Wallis** com **correção de Holm** e tamanho de efeito na RQ06;
  - **κ de Cohen ponderado** na RQ07.

## Como testamos os proxies

- **Amostra-ouro:** três avaliadores rotularam, de forma independente, 300 releases de 60 repositórios.
  - A concordância (κ de Fleiss) foi de 0,95 para o tipo do projeto e de 0,60 para "release corretiva". Ou seja, a classe é ambígua até para humanos.
- **Heurística de release corretiva:** testamos 4 versões e 197 combinações. A melhor ficou em **F1 = 0,57**.
- **Análise de sensibilidade:** classificamos cada repositório em 3 combinações de definições (release × release + tags, lead time por release × por commit).

## Nossos extras (além do enunciado)

| Extra | Para que serve |
| :--- | :--- |
| **Kaplan-Meier** na recuperação | usa os episódios censurados em vez de ignorá-los |
| **Bootstrap BCa** (2.000 reamostragens) | intervalo de confiança de 95% para todas as medianas |
| **Post-hoc de Dunn + δ de Cliff** | mostra *quais* grupos diferem na RQ06, e com que força |
| **As duas opções do bônus** (RQ08) | *rework rate* e Mann-Kendall, este também em escala mensal, porque o trimestral (4 pontos) não tem poder estatístico |
| **Cache SQLite + pool de tokens + GraphQL em lote** | coleta retomável após rate limit ou Ctrl+C, sem repetir chamadas |
| **Reprodução exata sem token** | o manifesto e os JSONs versionados regeneram todos os números e o artigo (`build_report.py`) |

---

# 2. Como os repositórios entregam

> O repositório típico publica **uma release a cada 3 semanas**, leva **cerca de 1 semana** do commit à release e recupera falhas de CI em **cerca de 3 horas**.

| RQ | Métrica | Mediana | IQR |
| :--- | :--- | ---: | :--- |
| RQ01 | Deployment frequency | **0,35 release/semana** | 0,19–0,77 |
| RQ02 | Lead time (a) por release | **166 h** (≈ 7 dias) | 23–626 h |
| RQ02 | Lead time (b) por commit | **152 h** (≈ 6 dias) | 25–404 h |
| RQ03 | CFR (a), proxy de CI | **5,3%** | 2,0–11,6% |
| RQ03 | CFR (b), proxy de entrega | **42,9%** | 16,7–71,0% |
| RQ04 | Tempo de recuperação | **3,3 h** | 0,6–17,7 h |

![Classificação DORA C1](analysis/output/figures/fig03_rq01_dora_c1.png)

**Classificação geral:** a maioria fica em **High (36%) e Medium (31%)**, só 7% são Elite, e 22% não podem ser classificados porque falta alguma métrica.

![RQ03 — CFR (a) × (b)](analysis/output/figures/fig05_rq03_cfr.png)

**Dois proxies, duas histórias:** os dois proxies contam histórias opostas, com 5% de falha no CI e 43% na entrega. O valor de 43% é um **limite superior**: a heurística de release corretiva tem **F1 = 0,57** (precisão 0,44), e nem os avaliadores concordaram bem (κ = 0,60).

---

# 3. Velocidade × estabilidade e robustez

## RQ05 — Quem entrega mais falha mais?

> **Sim:** entre repositórios, quem entrega mais também falha mais, ao contrário do que o DORA afirma.

![RQ05 — Deployment frequency × CFR](analysis/output/figures/rq05_scatter.png)

- CFR (a): ρ = **0,13** (fraca, p = 0,018)
- CFR (b): ρ = **0,69** (forte, p < 0,001), com uma parte mecânica: mais releases significam mais chance de uma correção em até 7 dias.

## RQ06 — O que explica? A idade do projeto.

![RQ06 — Métricas por quartil de idade](analysis/output/figures/fig08_rq06_idade.png)

Projetos **jovens** entregam mais, com lead time de 18 h (contra 556 h nos antigos), recuperam mais rápido e corrigem mais. Projetos **maduros** são lentos e estáveis. Popularidade e tipo do projeto não fizeram diferença (Kruskal-Wallis + Holm).

## RQ07 — A classificação depende da definição?

> **Em parte:** ao trocar a definição operacional, de **11% a 24%** dos repositórios mudam de categoria DORA.

| Comparação | O que mudou | Mudaram de categoria | κ ponderado |
| :--- | :--- | ---: | ---: |
| C1 × C2 | contar tags como deploy | **14,6%** | 0,80 |
| C1 × C3 | tags + lead time por commit | **23,6%** | 0,67 |
| C2 × C3 | lead time por release × por commit | **11,0%** | 0,84 |

- Contar tags como deploy **só melhora** categorias: 36 sobem e nenhum desce.
- Comparar "nível DORA" entre estudos só faz sentido com a **mesma definição**.

## RQ08 (bônus) — Rework e tendência no tempo

> Ao longo do ano, **mais repositórios melhoram do que pioram**. Dentro de cada repositório, o *trade-off* da RQ05 **não se repete**.

| Tendência mensal (Mann-Kendall) | Melhora | Piora | Estável |
| :--- | ---: | ---: | ---: |
| Deployment frequency | **15,2%** sobe | 6,7% cai | 78,1% |
| CFR de CI | **7,3%** cai | 4,4% sobe | 88,3% |

- *Rework rate* mediano de **0,77**: a proporção de releases corretivas, que é um limite superior, pela mesma heurística da CFR (b).
- Na escala trimestral pedida (4 pontos), nenhum repositório tem tendência significativa: o teste não tem poder estatístico com tão poucos pontos.

---

# Síntese final

- Releases a cada ~3 semanas, ~1 semana de lead time, recuperação em horas: a maioria fica em **High/Medium**.
- A taxa de falha **depende do proxy**: 5% no CI e 43% na entrega, sendo este um limite superior.
- Entre repositórios, entregar mais se associa a falhar mais, e a **idade do projeto** está por trás disso.
- A classificação DORA é **razoavelmente robusta**, mas não neutra à definição operacional.

**Principais limitações:** release não é deploy; a heurística de release corretiva ficou abaixo da meta (F1 = 0,57); um dos três avaliadores foi um modelo de linguagem.

## Mensagem principal

> **Dá para minerar métricas DORA de repositórios abertos, mas o número só tem sentido junto com a definição usada para medi-lo: o proxy escolhido muda a taxa de falha de 5% para 43%.**

