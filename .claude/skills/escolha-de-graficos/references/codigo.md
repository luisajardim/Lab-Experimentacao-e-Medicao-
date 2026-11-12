# Ferramentas e padrões de código

Prefira o que o projeto já usa. Sem preferência: Python com matplotlib e seaborn para figuras estáticas, plotly para interativas.

## Escolha rápida

| Necessidade | Ferramenta |
|---|---|
| Controle total, figura de artigo | matplotlib |
| Boxplot, violino, KDE, heatmap, estética refinada | seaborn |
| Interativo, Sankey, treemap, sunburst, choropleth | plotly |
| Grafos | networkx (+ graphviz ou pyvis) |
| Estatística | scipy.stats, statsmodels, pingouin (tamanho de efeito) |
| R | ggplot2; rstatix e effsize para testes e efeito |
| Figura dentro do LaTeX | TikZ / pgfplots |

## Padrão de qualquer script

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)          # seed fixa se houver amostragem
df = pd.read_csv("dados/brutos.csv")      # leia dos dados brutos, não de números digitados

fig, ax = plt.subplots(figsize=(3.4, 2.4))   # tamanho final (ex.: coluna de artigo)
ax.hist(df["valor"], bins=50)
ax.set_xscale("log")                          # só se a cauda for longa, e rotule
ax.set_xlabel("Tempo até merge (horas, escala log)")
ax.set_ylabel("Número de PRs")
ax.axvline(df["valor"].median(), ls="--", color="k", lw=0.8)
ax.set_title(f"Distribuição do tempo até merge (n = {len(df):,})".replace(",", "."))
fig.savefig("figures/tempo_merge.pdf", bbox_inches="tight")   # vetorial; PNG com dpi=300 se preciso
fig.savefig("figures/tempo_merge.png", dpi=300, bbox_inches="tight")
```

Sempre informe ao usuário o caminho dos arquivos gerados.

## Checklist antes de entregar

- Título, eixos com unidade, n, fonte e data dos dados.
- Abri a imagem final e conferi: nada sobreposto, cortado ou ilegível.
- Escala log declarada; barras começam em zero.
- Incerteza mostrada e definida na legenda.
- Legível em escala de cinza e no tamanho final.
- A figura responde à pergunta do passo 1 do fluxo, e só a ela.

## R (ggplot2)

Comum em estudos empíricos de ES (replication packages de ESEM e ICSE). Pacotes úteis: `ggplot2`, `dplyr`, `rstatix` e `effsize` (testes e tamanho de efeito), `lme4` (modelos mistos).

```r
library(ggplot2)
df <- read.csv("dados/brutos.csv")
p <- ggplot(df, aes(x = grupo, y = valor)) +
  geom_violin(fill = "grey85") +
  geom_boxplot(width = 0.15, outlier.alpha = 0.3) +
  scale_y_log10() +
  labs(x = "Grupo", y = "Tempo até merge (horas, escala log)",
       title = paste0("n = ", nrow(df))) +
  theme_minimal(base_size = 9)
ggsave("figures/valor_por_grupo.pdf", p, width = 3.4, height = 2.4)
```

Ferramentas sem código (Tableau, Power BI, JASP) servem para exploração; para figura de artigo, prefira código versionado, que se reproduz.

## pgfplots (LaTeX)

Use quando o documento já está em LaTeX: a fonte e o tamanho acompanham o texto e a figura fica versionada no `.tex`.

```latex
\usepackage{pgfplots}\pgfplotsset{compat=1.18}
\begin{tikzpicture}
\begin{axis}[width=\columnwidth, height=4.5cm, ybar, xlabel={Linguagem},
  ylabel={Repositórios}, symbolic x coords={Python,TypeScript}, xtick=data,
  nodes near coords, ymin=0]
\addplot coordinates {(Python,532) (TypeScript,468)};
\end{axis}
\end{tikzpicture}
```

Para dados grandes, gere o gráfico em Python, salve em PDF e use `\includegraphics`.
