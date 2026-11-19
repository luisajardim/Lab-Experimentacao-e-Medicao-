# Análise de Poder e Escolha de $N$ (T09, #104)

> **Decisão:** **$N = 10$ repetições por máquina** (total de **30 blocos pareados** somando Bernardo, Luísa e Pedro), mantendo todos os **6 tratamentos × 4 cenários × 3 projetos** (720 instalações medidas + 2 aquecimentos = **722 instalações**, ~**4,8 horas** por máquina).

---

## 1. Método (baseado no piloto `data/raw/pilot/runs.csv`)

A simulação de poder em [`src/power.py`](../src/power.py) (`uv run lab05 power`) segue a lógica de reamostragem empírica sobre a variância real observada no piloto do Bernardo (180 instalações medidas nos cenários `cold` e `warm-cache`, 5 repetições):

1. **Ruído empírico pareado:** Para cada `(projeto, cenário)` e gerenciador $M \neq \text{npm}$, calcula-se a diferença pareada em escala logarítmica $d_i = \ln(t_{M,i}) - \ln(t_{\text{npm},i})$ e subtrai-se a mediana de cada gerenciador para isolar apenas a variabilidade entre repetições (sem efeito de tratamento).
2. **Mapeamento de cenários sem piloto:** Os cenários `ci` e `reinstall` (não executados no piloto) herdam o ruído dos cenários equivalentes em cache (`cold` para `ci`; `warm-cache` para `reinstall`).
3. **Simulação de Monte Carlo:** Para cada tamanho de amostra $N \in \{3, 4, 5, 6, 8, 10, 12, 15\}$ por máquina ($n_{\text{pares}} = 3N$ blocos) e *speedup* alvo $s \in \{1{,}1;\; 1{,}2;\; 1{,}3;\; 1{,}5\}$, sorteiam-se 2.000 amostras bootstrap com reposição deslocadas por $-\ln(s)$ e aplica-se o **teste de Wilcoxon pareado bicaudal** com $\alpha_{\text{ef}} = 0{,}05 / 5 = 0{,}01$ (o degrau mais exigente da correção de Holm para as 5 comparações contra o controle `npm`).

---

## 2. Resultados do Poder Simulado ($\alpha_{\text{ef}} = 0{,}01$, 3 máquinas)

Para um efeito de **speedup = 1,2×** (20% mais rápido que o `npm`):

| Projeto | Cenário | Ruído ($\sigma_{\ln}$) | $N = 5$ (15 pares) | $N = 8$ (24 pares) | **$N = 10$ (30 pares)** | $N = 12$ (36 pares) | $N = 15$ (45 pares) |
|---|---|---|---|---|---|---|---|
| `next-app` | `cold` / `ci` | 0,057 | 100% | 100% | **100%** | 100% | 100% |
| `next-app` | `warm-cache` / `reinstall` | 0,211 | 49% | 81% | **91%** | 96% | 98% |
| `react-vite` | `cold` / `ci` | 0,140 | 100% | 100% | **100%** | 100% | 100% |
| `react-vite` | `warm-cache` / `reinstall` | 0,471 | 38% | 57% | **74%** | 80% | 91% |
| `express-api` | `warm-cache` / `reinstall` | 0,185 | 62% | 90% | **97%** | 99% | 100% |
| `express-api` | `cold` / `ci` *(outlier no npm)* | 1,016 | 1% | 2% | **2%** | 1% | 2% |

### Achado importante no piloto (`express-api cold`)
No piloto, o `npm` em `express-api cold` apresentou variância extrema entre repetições (`1,91 s`, `2,99 s`, `11,04 s`, `13,01 s`, `31,24 s`), elevando $\sigma_{\ln}$ para `1,016` — enquanto `pnpm` (`1,36–2,07 s`) e `bun` (`5,49–6,71 s`) permaneceram estáveis. Por isso, diferenças pequenas (1,2×) nessa célula específica ficam mascaradas pelo ruído do próprio `npm`, embora diferenças reais maiores (ex.: `pnpm` sendo ~8× mais rápido no `cold` do piloto) sejam detectáveis. Em `react-vite warm-cache`, para speedup de **1,3×**, $N = 10$ já atinge **92%** de poder.

---

## 3. Viabilidade de Tempo até 23/11

No piloto (182 instalações em ~1,2 h de coleta efetiva, sem contar a pausa de 19 min antes da recoleta do pnpm), a duração média completa — incluindo preparação do cenário, limpeza de cache e `build` — foi de **24,0 s por instalação**:

| $N$ (por máquina) | Pares totais (3 máquinas) | Instalações / máquina (+2 aquec.) | Tempo estimado / máquina | Cabe até 23/11? |
|---|---|---|---|---|
| 5 | 15 | 362 | 2,4 h | Sim (mas poder < 65% em `warm-cache`) |
| 8 | 24 | 578 | 3,9 h | Sim |
| **10 (escolhido)** | **30** | **722** | **4,8 h** | **Sim (sem cortar cenários/projetos)** |
| 12 | 36 | 866 | 5,8 h | Apertado |
| 15 | 45 | 1.082 | 7,2 h | Arriscado para rodar em 1 dia |

### Conclusão da escolha
Adotar **$N = 10$** garante:
- **Poder ≥ 90%** para speedup 1,2× na maior parte das células (e **92% a 100%** para speedup 1,3× em todas as células estáveis);
- **30 blocos pareados** no total (tamanho amostral robusto para o Wilcoxon pareado e IC bootstrap);
- **Viabilidade de execução (~4,8 h por máquina)** até o prazo interno de **23/11**, mantendo o desenho completo (4 cenários × 3 projetos) sem necessidade de cortes.

