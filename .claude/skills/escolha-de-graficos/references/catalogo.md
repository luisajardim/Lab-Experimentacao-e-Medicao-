# Catálogo de gráficos

| Gráfico | Dado | Use quando | Evite / cuidado |
|---|---|---|---|
| Barras | categórico × numérico | comparar valores entre até ~10 categorias | muitas categorias; proporções; eixo truncado |
| Barras agrupadas | categórico × numérico × grupo | 2 a 4 séries lado a lado | denso com muitas séries |
| Barras empilhadas | categórico × parte | total e partes importam | segmentos do meio são difíceis de comparar |
| Lollipop / dumbbell | categórico × numérico (ou par antes/depois) | muitas categorias, menos tinta que barras; mudança entre dois momentos | exige ordenação clara |
| Linhas | temporal × numérico | tendência e padrões no tempo | dados categóricos; muitas séries sobrepostas |
| Área | temporal × numérico | volume acumulado | sobreposição esconde séries |
| Small multiples | grupos × mesma escala | comparar muitas séries sem poluição | manter eixos iguais |
| Sparkline | série curta | tendência em linha de tabela ou KPI | sem eixos: não serve para leitura exata |
| Histograma | numérico contínuo | forma, simetria, outliers | sensível à largura dos bins: teste mais de um |
| ECDF | numérico contínuo | comparar distribuições sem escolher bins; ler percentis | menos intuitivo para leigos |
| KDE | numérico contínuo | sobrepor distribuições | bandwidth pode suavizar demais; não use com poucos pontos |
| Boxplot | numérico por grupos | comparação compacta (mediana, IQR, outliers) | esconde bimodalidade; mostre os pontos se n for pequeno |
| Violino / raincloud | numérico por grupos | a forma importa | menos intuitivo; raincloud junta densidade, caixa e pontos |
| Beeswarm / strip | numérico por grupo, n pequeno | mostrar todos os pontos | ilegível com milhares de pontos |
| Ridgeline | distribuição por muitos grupos ordenados | comparar formas ao longo de uma ordem | exige sobreposição moderada |
| Q-Q plot | numérico | checar normalidade ou outra distribuição | pede alguma prática para ler |
| Dispersão | numérico × numérico | correlação, clusters, outliers | overplotting: alpha, hexbin, escala log |
| Bolhas | 3 numéricos | 3ª variável no tamanho | a área engana a percepção |
| Heatmap | grade numérica 2D | padrões em matrizes densas (dia × hora, coorte × período) | a paleta altera a leitura; rotule valores se poucos |
| Heatmap de correlação | numérico multivariado | exploração; multicolinearidade antes de regressão | não indica causalidade; Pearson só mede linear |
| Pizza / donut | categórico proporcional | até 5 fatias, diferenças grandes | fatias parecidas; muitas categorias |
| Treemap | hierárquico × numérico | muitas categorias hierárquicas | áreas semelhantes são difíceis de comparar |
| Sunburst | hierárquico + valor | parte/todo em vários níveis | muitos níveis ou fatias pequenas |
| Waterfall | variação acumulada | como parcelas levam do valor inicial ao final | exige ordem lógica das parcelas |
| Funil | etapas sequenciais | perda entre etapas | só vale se as etapas forem estritamente sequenciais |
| Sankey | fluxo origem → destino com peso | gargalos, caminhos dominantes | ilegível com muitos nós e cruzamentos |
| Fluxograma | qualitativo sequencial | etapas e decisões | sem dimensão quantitativa |
| Ponto com IC / forest plot | estimativa + intervalo por grupo | comparar efeitos e incerteza (meta-análise, regressão) | definir o IC na legenda |
| Bullet chart | valor × meta × faixas | desempenho contra meta | pouco conhecido: explique |
| Control chart (SPC) | temporal × numérico + limites | separar ruído de causa especial (±3σ) | pressupõe processo estável |
| Pareto | categórico × contagem + % acumulada | priorizar causas (80/20) | categorias mal definidas; só frequência |
| Burndown / burnup | temporal × trabalho | progresso contra linha ideal | burndown esconde mudança de escopo (burnup mostra) |
| CFD | temporal × contagem por estado | WIP, lead time, gargalos | exige histórico consistente de transições |
| Gantt | tarefas × tempo | cronogramas e dependências | cresce rápido |
| Kaplan-Meier | tempo até evento + censura | sobrevivência, tempo até falha ou churn | exige tratar censura |
| Grafo | relacional | dependências, ciclos, nós centrais | "prato de espaguete" com muitos nós; use matriz |
| Radar | numérico (5 a 10 métricas) | perfil de pontos fortes e fracos | área engana; ordem dos eixos importa; normalize |
| Parallel coordinates | alta dimensão | clusters e outliers multivariados | overplotting |
| ROC / precisão-revocação | classificador | comparar limiares e modelos | ROC engana com classes muito desbalanceadas: prefira precisão-revocação |
| Matriz de confusão | classificação | ver quais classes se confundem | normalize por linha se as classes forem desbalanceadas |
| Curva de calibração | probabilidades previstas × observadas | confiabilidade das probabilidades | precisa de bins com n suficiente |
| Gráfico de resíduos | resíduo × ajustado | validar um modelo de regressão | padrão em funil indica heterocedasticidade |
| Bland-Altman | duas medidas do mesmo fenômeno | concordância entre métodos | não substitui a correlação |
| Mapa / choropleth | geoespacial | localização é variável relevante | normalize (per capita); a área da região distorce |
| Calendar heatmap | atividade por dia | sazonalidade semanal e anual | ruim para comparar anos distantes |
