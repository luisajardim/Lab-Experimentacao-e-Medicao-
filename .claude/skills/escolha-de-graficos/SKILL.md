---
name: escolha-de-graficos
description: Decide qual gráfico usar (e por quê) para qualquer análise de dados, métricas ou estatísticas, em qualquer área (engenharia de software, produto e negócio, experimentos científicos, machine learning, operações, saúde, finanças), e gera o código. Use quando o usuário pedir para escolher, comparar, criar, revisar ou corrigir gráficos, dashboards, figuras de artigo ou slides, ao apresentar resultados de uma análise, ou quando houver dúvida entre barras, histograma, boxplot, violino, dispersão, heatmap, pizza, linhas, Sankey, Pareto, forest plot, ROC, etc. Decide o QUÊ mostrar; para o acabamento visual (paleta, tema), combine com a skill dataviz, se disponível.
---

# Escolha de gráficos

Princípio central: **um gráfico responde a uma pergunta específica sobre os dados.** Nunca escolha o tipo antes de saber a pergunta, o público e o tipo das variáveis. Funciona para qualquer domínio; os mapeamentos por área estão em `references/dominios.md`.

## Fluxo

1. **Pergunta.** Qual mensagem o gráfico precisa passar? Classifique: comparação, tendência no tempo, distribuição, relação entre variáveis, composição, ranking, desvio de uma meta, incerteza, fluxo/processo, hierarquia, geográfico, multidimensional, priorização, estabilidade. Se estiver ambígua, faça no máximo uma pergunta ao usuário.
2. **Dados.** Tipo de cada variável (categórica nominal/ordinal, numérica contínua/discreta, temporal, relacional, hierárquica, geoespacial), quantidade de categorias, séries e pontos, e se há agrupamento ou repetição (medidas repetidas, mesma unidade ao longo do tempo).
3. **Destino.** Artigo (colunas, P&B, impressão), slide (uma mensagem, fonte grande), dashboard (leitura rápida, interação) ou notebook/exploração. Veja `references/destinos.md`.
4. **Distribuição antes do resumo.** Dados reais costumam ser assimétricos, com cauda longa e outliers (tempos, tamanhos, receitas, contagens). Se média >> mediana, mostre a distribuição e reporte mediana, IQR e percentis, não só a média.
5. **Escolha** na tabela abaixo, confira limitações em `references/catalogo.md` e escolha também uma alternativa.
6. **Implemente** com título, eixos com unidade, n, fonte e data dos dados (`references/codigo.md`). Depois de salvar, **abra a imagem final e olhe**: rótulos sobrepostos, texto cortado e legenda tapando dados só aparecem vendo a figura.
7. **Justifique** em 2 a 3 linhas: por que esse tipo, qual alternativa foi descartada e qual armadilha foi evitada.

## Pergunta → gráfico

| Pergunta | Primeira escolha | Alternativas |
|---|---|---|
| Comparar categorias | Barras ordenadas | Lollipop, dumbbell (antes/depois) |
| Comparar muitas categorias | Barras horizontais, top N + "outros" | Treemap |
| Evolução no tempo | Linhas | Área (acumulado), small multiples, sparkline |
| Distribuição de uma variável | Histograma ou ECDF | KDE, Q-Q plot (checar normalidade) |
| Distribuição por grupo | Boxplot, violino ou raincloud | Beeswarm/strip (n pequeno), ridgeline |
| Relação entre duas numéricas | Dispersão | Hexbin/2D density (muitos pontos), bolhas (3ª variável) |
| Correlação entre várias | Heatmap de correlação (Spearman se assimétrico) | Matriz de dispersão |
| Composição (partes do todo) | Barras empilhadas (100%) | Pizza (até 5 fatias), treemap, waterfall (variação) |
| Incerteza / efeito com intervalo | Ponto com intervalo de confiança | Forest plot, faixa de confiança em linha |
| Desvio de uma meta | Bullet chart, linha de referência | Control chart (estabilidade) |
| Priorizar causas | Pareto | Barras ordenadas |
| Fluxo com volume | Sankey | Funil (etapas), fluxograma (sem volume) |
| Padrão em grade (dia × hora, coorte × período) | Heatmap | Calendar heatmap |
| Perfil multivariado | Parallel coordinates | Radar (poucos eixos, normalizado) |
| Relações / dependências | Grafo | Matriz de adjacência (muitos nós) |
| Hierarquia | Treemap | Sunburst, árvore |
| Geográfico | Choropleth (normalizado), mapa de pontos | Cartograma |
| Tempo até evento | Kaplan-Meier | Curva de risco acumulado |
| Desempenho de classificador | Curva ROC / precisão-revocação, matriz de confusão | Calibração |

## Regras e armadilhas (aplique sempre)

- **Visualize os dados antes de resumir.** Resumos idênticos podem esconder formas opostas (quarteto de Anscombe).
- **Média sozinha engana** em dados assimétricos ou bimodais. Use percentis (P50, P90, P95, P99) e mostre a forma. Prefira violino ou histograma ao boxplot quando a forma importa.
- **Mostre a incerteza**: intervalos de confiança ou barras de erro com a definição na legenda (DP, EP ou IC 95%). Efeito sem intervalo não diz se é relevante.
- **Normalize antes de comparar** entidades de portes diferentes (per capita, por mil, por KLOC, por usuário).
- **Eixos:** barras começam em zero; linhas podem não começar, mas diga. Use escala log para cauda longa e rotule. Evite eixo duplo (cada escala sugere uma relação diferente) e 3D.
- **Pizza e donut:** no máximo 5 fatias bem diferentes; senão, barras ordenadas.
- **Overplotting:** com muitos pontos use transparência, hexbin ou amostragem declarada.
- **Muitas séries:** em vez de 12 linhas coloridas, use small multiples ou destaque uma e deixe o resto cinza.
- **Ordene** categorias por valor (exceto ordinais e tempo). Rotule direto nas barras e linhas, quando couber, em vez de legenda distante.
- **Cor:** divergente centrada no zero para valores com sinal; sequencial para magnitude; qualitativa só para categorias; nunca só cor (acessibilidade e P&B).
- **Correlação não é causalidade.** Em dados observacionais, o título descreve associação, não efeito.
- **Significância não é relevância.** Ao comparar grupos, junte teste e tamanho de efeito (`references/estatistica.md`).
- **Um gráfico, uma mensagem.** Se precisar de duas, faça duas figuras. Título que afirme o achado quando o destino for apresentação.
- **Rotule tudo:** título, unidade nos eixos, n, fonte e data de captura.

## Formato da resposta

1. **Pergunta** que o gráfico responde.
2. **Dados** (tipos, n, agrupamento) e **destino**.
3. **Gráfico recomendado** e uma alternativa.
4. **Por quê** e qual armadilha foi evitada.
5. **Código** reproduzível, se pedido: leia dos dados brutos, fixe a seed se houver amostragem, salve em vetorial (SVG/PDF) ou PNG 300 dpi em `figures/` e informe o caminho.

Se já houver gráficos prontos, revise cada um contra o catálogo e as regras: aponte os que não respondem a nenhuma pergunta, escondem a distribuição ou a incerteza, e diga o que manter, trocar ou cortar.

## Referências (leia só o que precisar)

- `references/catalogo.md`: cada tipo de gráfico, quando usar e quando evitar.
- `references/dominios.md`: perguntas típicas por área e o gráfico para cada uma.
- `references/estatistica.md`: testes, tamanho de efeito, incerteza e correção de comparações múltiplas.
- `references/destinos.md`: artigo, slides, dashboard e acessibilidade.
- `references/codigo.md`: ferramentas e padrões de código (Python, R, pgfplots/TikZ).
