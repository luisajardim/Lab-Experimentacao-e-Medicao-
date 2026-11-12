# Estatística que acompanha o gráfico

## Escolha do teste (comparação de grupos)

| Situação | Teste | Tamanho de efeito |
|---|---|---|
| 2 grupos independentes, dados assimétricos | Mann-Whitney | Cliff's δ ou A12 |
| 2 grupos independentes, ~normais | t de Welch | Cohen's d (Hedges g) |
| 2 medidas pareadas | Wilcoxon (ou t pareado se ~normal) | r de postos, d pareado |
| 3+ grupos independentes | Kruskal-Wallis (+ Dunn) ou ANOVA (+ Tukey) | ε², η² |
| Associação entre duas numéricas | Spearman (assimétricos) ou Pearson (lineares, ~normais) | o próprio ρ ou r |
| Duas categóricas | Qui-quadrado ou Fisher (n pequeno) | V de Cramér, razão de chances |
| Dados agrupados (vários itens por repositório, sujeito etc.) | Modelo misto ou erro padrão agrupado | coeficiente padronizado |

Roteiro: tipo de variável → nº de grupos e estrutura (independentes, pareados, agrupados) → pressupostos → teste → reportar p **e** tamanho de efeito.

Pressupostos a checar antes de testes paramétricos: normalidade (Shapiro-Wilk, Q-Q plot) e homocedasticidade (Levene ou Bartlett, antes da ANOVA).

Checar normalidade: histograma + Q-Q plot primeiro; Shapiro-Wilk com n grande rejeita qualquer desvio ínfimo, então não decida só pelo p.

## Regras

- **Significância não é relevância.** Com n enorme, efeitos desprezíveis têm p minúsculo. Reporte o tamanho de efeito com intervalo e, se possível, defina antes o menor efeito que importaria (SESOI) e use testes de equivalência para afirmar "sem efeito relevante".
- **Ausência de significância não é ausência de efeito.** Só afirme "sem efeito" se o intervalo de confiança excluir efeitos relevantes.
- **Comparações múltiplas:** corrija (Bonferroni, Holm, Benjamini-Hochberg) e diga qual.
- **Mostre a incerteza no gráfico:** IC 95% (bootstrap se a distribuição for assimétrica), e diga na legenda o que a barra representa (DP, EP ou IC).
- **Barras de erro não substituem os dados.** Com n pequeno, mostre os pontos.
- **Dados agrupados violam independência:** não trate 10.000 PRs de 50 repositórios como 10.000 observações independentes.
- **Correlação não é causalidade;** use verbos de associação nos títulos.
- **Poder:** com n pequeno, um teste não significativo é inconclusivo. Diga o menor efeito detectável.
