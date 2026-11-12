# Perguntas típicas por área

Use como ponto de partida; a pergunta real do usuário sempre manda.

## Engenharia de software (PRs, issues, código, processo)

| Pergunta | Gráfico |
|---|---|
| Como se distribui o tempo até merge ou a latência? | Histograma (log se cauda longa) + P50, P90, P95 |
| O tempo difere entre repositórios, linguagens ou tamanhos? | Boxplot, violino ou raincloud + Mann-Whitney ou Kruskal-Wallis + tamanho de efeito |
| Tamanho do PR afeta o tempo de revisão? | Dispersão em escala log (alpha), bolhas para 3ª variável |
| Quais métricas se correlacionam? | Heatmap de Spearman |
| Evolução de PRs ou issues por semana ou mês | Linhas; área empilhada por estado |
| Quando os PRs são abertos ou mesclados (dia × hora) | Heatmap |
| Por onde os PRs passam | Sankey (volume) ou fluxograma (política) |
| Gargalo, WIP | CFD |
| Quais causas, labels ou tipos concentram os casos | Pareto |
| Quantos PRs por autor, revisor ou módulo | Barras ordenadas (top N + outros) |
| Onde se concentram as mudanças no código | Treemap |
| Dependências ou acoplamento entre módulos | Grafo (poucos nós) ou matriz de adjacência (muitos) |
| Quem revisa o código de quem | Grafo autor → revisor |
| O processo está estável entre releases | Control chart |
| O backlog está sendo consumido | Burndown ou burnup |
| Defeitos por componente e severidade | Barras empilhadas ordenadas, Pareto |

## Produto, negócio e marketing

| Pergunta | Gráfico |
|---|---|
| Onde os usuários desistem no fluxo | Funil ou Sankey |
| Retenção por coorte | Heatmap de coortes (coorte × período) |
| Receita ao longo do tempo e por segmento | Linhas, área empilhada, small multiples |
| De onde veio a variação do resultado | Waterfall |
| Meta contra realizado | Bullet chart |
| Teste A/B: qual variante vence | Ponto com IC da diferença (não duas barras sem intervalo) |
| Concentração de clientes ou receita | Pareto, curva de Lorenz |
| Participação por região | Choropleth normalizado ou barras ordenadas |

## Experimentos e ciência

| Pergunta | Gráfico |
|---|---|
| Comparar tratamentos | Pontos de dados individuais + média e IC (strip ou raincloud) |
| Efeito e incerteza em vários estudos | Forest plot |
| A distribuição é normal | Histograma + Q-Q plot |
| Medidas repetidas no mesmo sujeito | Linhas ligando os pares (slopegraph) |
| Dose-resposta ou relação contínua | Dispersão + curva ajustada com faixa de confiança |
| Tempo até evento | Kaplan-Meier |
| Concordância entre dois métodos | Bland-Altman |

## Machine learning

| Pergunta | Gráfico |
|---|---|
| Desempenho de um classificador | ROC, precisão-revocação, matriz de confusão |
| Probabilidades confiáveis | Curva de calibração |
| Modelo está sub ou superajustado | Curva de aprendizado (erro × tamanho de treino ou época) |
| Comparar modelos | Pontos com IC (validação cruzada) por modelo, não só a média |
| Quais variáveis importam | Barras ordenadas de importância (com variação entre execuções) |
| Erros de regressão | Resíduos × previsto, previsto × real |
| Drift de dados | Duas densidades sobrepostas ou ECDFs |

## Operações e confiabilidade (SRE, infraestrutura)

| Pergunta | Gráfico |
|---|---|
| Latência de um serviço | Histograma + percentis; nunca só a média |
| SLO cumprido ao longo do tempo | Linha com a meta e orçamento de erro |
| Incidentes: causas | Pareto |
| Capacidade e utilização | Linhas com limite; heatmap por hora e dia |
| Estabilidade da taxa de erros | Control chart |

## Saúde, finanças e outras

| Pergunta | Gráfico |
|---|---|
| Sobrevivência ou tempo até recaída | Kaplan-Meier |
| Retorno e risco de ativos | Dispersão (risco × retorno), linhas normalizadas na base 100 |
| Distribuição de retornos e perdas | Histograma com cauda destacada |
| Orçamento: parcelas até o total | Waterfall |
| Indicadores por unidade (hospital, filial) | Funnel plot (taxa × tamanho da amostra) |

## Quando a área não está aqui

Volte ao fluxo do `SKILL.md`: pergunta, tipos de variáveis, destino. Os tipos de variáveis decidem o gráfico mesmo sem um mapeamento de domínio.
