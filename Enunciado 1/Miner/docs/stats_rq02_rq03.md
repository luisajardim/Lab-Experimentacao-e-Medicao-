# Análise Estatística de Engajamento e Releases (RQ02 / RQ03)

**Fonte:** `/home/alvim/Development/Lab-Experimentacao-e-Medicao-/Enunciado 1/Miner/data/github-rq2-rq3-v2_1787148677023.csv`
**Gerado em:** 2026-08-27T00:32:55.697Z
**Repositórios analisados:** 1000
**Critério de outlier:** limite superior de Tukey, `Q3 + 1,5 × IQR`.

## 1. Hipótese e objetivo

- **RQ02 — contribuição externa:** repositórios populares devem apresentar um volume relevante de PRs aceitas, mesmo que a distribuição seja muito desigual por causa de projetos grandes.
- **RQ03 — releases:** uma parte expressiva da amostra deve publicar releases, embora alguns projetos optem por distribuir versões por tags, pacotes ou imagens de container em vez de usar a funcionalidade de Releases do GitHub.

## 2. Resumo estatístico

### RQ02 — total de PRs aceitas

| Mínimo | Q1 | Mediana | Média | Q3 | Máximo | IQR | Limite superior |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 175 | 768 | 4236.77 | 3415.75 | 103349 | 3240.75 | 8276.88 |

**Outliers acima do limite superior:** 124

Distribuição por faixa de PRs aceitas:

| Faixa | Repositórios | % |
|---|---:|---:|
| até 100 | 182 | 18.2% |
| 101-500 | 235 | 23.5% |
| 501-1.000 | 133 | 13.3% |
| 1.001-5.000 | 264 | 26.4% |
| 5.001-10.000 | 87 | 8.7% |
| 10.001+ | 99 | 9.9% |

Top repositórios por PRs aceitas:

| Repositório | PRs aceitas |
|---|---:|
| firstcontributions/first-contributions | 103349 |
| llvm/llvm-project | 97096 |
| elastic/elasticsearch | 95522 |
| getsentry/sentry | 91170 |
| home-assistant/core | 90122 |

### RQ03 — total de releases

| Mínimo | Q1 | Mediana | Média | Q3 | Máximo | IQR | Limite superior |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 39 | 126.61 | 147 | 1000 | 147 | 367.5 |

**Outliers acima do limite superior:** 93
**Repositórios sem releases (total = 0):** 286 (28.6%)

Distribuição por faixa de releases:

| Faixa | Repositórios | % |
|---|---:|---:|
| 0 | 286 | 28.6% |
| 1 | 24 | 2.4% |
| 2-10 | 52 | 5.2% |
| 11-50 | 177 | 17.7% |
| 51-100 | 118 | 11.8% |
| 101-500 | 274 | 27.4% |
| 501+ | 69 | 6.9% |

Top repositórios por releases:

| Repositório | Releases |
|---|---:|
| langchain-ai/langchain | 1000 |
| vercel/next.js | 1000 |
| ggml-org/llama.cpp | 1000 |
| electron/electron | 1000 |
| storybookjs/storybook | 1000 |

## 3. Interpretação

A mediana é a medida mais robusta para estas duas métricas porque a distribuição é fortemente assimétrica: a média é puxada para cima por repositórios muito grandes e ativos, enquanto a mediana mostra o comportamento central da maioria dos projetos populares.

Para **RQ02**, a mediana de 768 PRs aceitas mostra que a maioria dos repositórios populares tem fluxo contínuo de integração de contribuições, mas há uma cauda longa de projetos extraordinariamente ativos. Isso é consistente com ecossistemas grandes e bem mantidos, como kernels, bibliotecas de uso geral e ferramentas amplamente adotadas.

Para **RQ03**, a mediana de 39 releases mostra que há uma parcela relevante de projetos com histórico de publicação de versões, mas também existe uma parte importante que não usa Releases no GitHub. O fato de 286 repositórios (aproximadamente 28.6%) terem zero releases reforça que a ausência de releases não é necessariamente erro de coleta — pode refletir uma estratégia de distribuição alternativa.

## 4. Conclusão

A hipótese das RQs 02 e 03 se sustenta em termos de tendência central: repositórios populares recebem contribuições relevantes e, em muitos casos, também têm histórico de lançamentos. Porém, a distribuição é muito heterogênea e a comparação deve priorizar mediana, quartis e outliers em vez de médias isoladas.
