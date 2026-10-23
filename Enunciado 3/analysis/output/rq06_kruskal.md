# RQ06 — Características associadas ao desempenho DORA

Gerado por `analysis/rq06_kruskal.py`. Kruskal-Wallis (≥ 3 grupos) ou Mann-Whitney (2 grupos); p-valores corrigidos por Holm sobre os 20 testes; α = 0,05.

## Testes por fator × métrica

| Fator | Métrica | Teste | n | Grupos | p | p (Holm) | Efeito | Interpretação |
|---|---|---|---:|---:|---:|---:|---|---|
| linguagem | Deployment frequency (releases/semana) | Kruskal-Wallis | 315 | 6 | 0,002 | 0,025 **\*** | ε² = 0,061 | moderado |
| linguagem | Lead time (a) (horas) | Kruskal-Wallis | 272 | 6 | < 0,001 | 0,001 **\*** | ε² = 0,097 | moderado |
| linguagem | CFR (a) | Kruskal-Wallis | 315 | 6 | 0,004 | 0,056 | ε² = 0,055 | moderado |
| linguagem | CFR (b) | Kruskal-Wallis | 315 | 6 | < 0,001 | < 0,001 **\*** | ε² = 0,101 | moderado |
| linguagem | Tempo de recuperação (horas) | Kruskal-Wallis | 285 | 6 | 0,730 | 1,000 | ε² = 0,010 | desprezível |
| popularidade | Deployment frequency (releases/semana) | Kruskal-Wallis | 315 | 4 | 0,475 | 1,000 | ε² = 0,008 | desprezível |
| popularidade | Lead time (a) (horas) | Kruskal-Wallis | 272 | 4 | 0,273 | 1,000 | ε² = 0,014 | fraco |
| popularidade | CFR (a) | Kruskal-Wallis | 315 | 4 | 0,907 | 1,000 | ε² = 0,002 | desprezível |
| popularidade | CFR (b) | Kruskal-Wallis | 315 | 4 | 0,304 | 1,000 | ε² = 0,012 | fraco |
| popularidade | Tempo de recuperação (horas) | Kruskal-Wallis | 285 | 4 | 0,354 | 1,000 | ε² = 0,011 | fraco |
| idade | Deployment frequency (releases/semana) | Kruskal-Wallis | 315 | 4 | < 0,001 | < 0,001 **\*** | ε² = 0,120 | moderado |
| idade | Lead time (a) (horas) | Kruskal-Wallis | 272 | 4 | < 0,001 | < 0,001 **\*** | ε² = 0,266 | relativamente forte |
| idade | CFR (a) | Kruskal-Wallis | 315 | 4 | 0,026 | 0,317 | ε² = 0,029 | fraco |
| idade | CFR (b) | Kruskal-Wallis | 315 | 4 | < 0,001 | < 0,001 **\*** | ε² = 0,240 | relativamente forte |
| idade | Tempo de recuperação (horas) | Kruskal-Wallis | 285 | 4 | < 0,001 | 0,013 **\*** | ε² = 0,058 | moderado |
| tipo | Deployment frequency (releases/semana) | Kruskal-Wallis | 55 | 3 | 0,917 | 1,000 | ε² = 0,003 | desprezível |
| tipo | Lead time (a) (horas) | Kruskal-Wallis | 50 | 3 | 0,969 | 1,000 | ε² = 0,001 | desprezível |
| tipo | CFR (a) | Kruskal-Wallis | 55 | 3 | 0,143 | 1,000 | ε² = 0,072 | moderado |
| tipo | CFR (b) | Kruskal-Wallis | 55 | 3 | 0,477 | 1,000 | ε² = 0,027 | fraco |
| tipo | Tempo de recuperação (horas) | Kruskal-Wallis | 46 | 3 | 0,317 | 1,000 | ε² = 0,051 | moderado |

\* significativo após Holm (p < 0,05). ε²: Rea & Parker (1992); δ de Cliff: Romano et al. (2006).

## Dunn post-hoc (Kruskal-Wallis significativos)

| Fator | Métrica | Grupo A | Grupo B | z | p (Holm) | δ de Cliff | Interpretação |
|---|---|---|---|---:|---:|---:|---|
| linguagem | Deployment frequency (releases/semana) | Go (n=47) | JavaScript (n=20) | -1,23 | 1,000 | -0,224 | pequeno |
| linguagem | Deployment frequency (releases/semana) | Go (n=47) | Outras (n=86) | -0,67 | 1,000 | -0,075 | desprezível |
| linguagem | Deployment frequency (releases/semana) | Go (n=47) | Python (n=53) | -0,48 | 1,000 | -0,058 | desprezível |
| linguagem | Deployment frequency (releases/semana) | Go (n=47) | Rust (n=29) | -2,89 | 0,052 | -0,380 | médio |
| linguagem | Deployment frequency (releases/semana) | Go (n=47) | TypeScript (n=80) | -3,11 | 0,028 **\*** | -0,320 | pequeno |
| linguagem | Deployment frequency (releases/semana) | JavaScript (n=20) | Outras (n=86) | 0,84 | 1,000 | 0,131 | desprezível |
| linguagem | Deployment frequency (releases/semana) | JavaScript (n=20) | Python (n=53) | 0,89 | 1,000 | 0,129 | desprezível |
| linguagem | Deployment frequency (releases/semana) | JavaScript (n=20) | Rust (n=29) | -1,21 | 1,000 | -0,224 | pequeno |
| linguagem | Deployment frequency (releases/semana) | JavaScript (n=20) | TypeScript (n=80) | -0,97 | 1,000 | -0,161 | pequeno |
| linguagem | Deployment frequency (releases/semana) | Outras (n=86) | Python (n=53) | 0,14 | 1,000 | 0,013 | desprezível |
| linguagem | Deployment frequency (releases/semana) | Outras (n=86) | Rust (n=29) | -2,61 | 0,099 | -0,322 | pequeno |
| linguagem | Deployment frequency (releases/semana) | Outras (n=86) | TypeScript (n=80) | -2,90 | 0,052 | -0,261 | pequeno |
| linguagem | Deployment frequency (releases/semana) | Python (n=53) | Rust (n=29) | -2,53 | 0,113 | -0,331 | médio |
| linguagem | Deployment frequency (releases/semana) | Python (n=53) | TypeScript (n=80) | -2,68 | 0,087 | -0,281 | pequeno |
| linguagem | Deployment frequency (releases/semana) | Rust (n=29) | TypeScript (n=80) | 0,51 | 1,000 | 0,073 | desprezível |
| linguagem | Lead time (a) (horas) | Go (n=41) | JavaScript (n=18) | 2,52 | 0,130 | 0,420 | médio |
| linguagem | Lead time (a) (horas) | Go (n=41) | Outras (n=73) | -0,25 | 1,000 | -0,032 | desprezível |
| linguagem | Lead time (a) (horas) | Go (n=41) | Python (n=48) | 0,82 | 1,000 | 0,107 | desprezível |
| linguagem | Lead time (a) (horas) | Go (n=41) | Rust (n=29) | 1,85 | 0,514 | 0,265 | pequeno |
| linguagem | Lead time (a) (horas) | Go (n=41) | TypeScript (n=63) | 3,43 | 0,009 **\*** | 0,392 | médio |
| linguagem | Lead time (a) (horas) | JavaScript (n=18) | Outras (n=73) | -2,89 | 0,050 | -0,458 | médio |
| linguagem | Lead time (a) (horas) | JavaScript (n=18) | Python (n=48) | -1,95 | 0,463 | -0,310 | pequeno |
| linguagem | Lead time (a) (horas) | JavaScript (n=18) | Rust (n=29) | -0,88 | 1,000 | -0,119 | desprezível |
| linguagem | Lead time (a) (horas) | JavaScript (n=18) | TypeScript (n=63) | -0,09 | 1,000 | -0,004 | desprezível |
| linguagem | Lead time (a) (horas) | Outras (n=73) | Python (n=48) | 1,20 | 1,000 | 0,134 | desprezível |
| linguagem | Lead time (a) (horas) | Outras (n=73) | Rust (n=29) | 2,27 | 0,233 | 0,290 | pequeno |
| linguagem | Lead time (a) (horas) | Outras (n=73) | TypeScript (n=63) | 4,28 | < 0,001 **\*** | 0,414 | médio |
| linguagem | Lead time (a) (horas) | Python (n=48) | Rust (n=29) | 1,17 | 1,000 | 0,158 | pequeno |
| linguagem | Lead time (a) (horas) | Python (n=48) | TypeScript (n=63) | 2,68 | 0,088 | 0,308 | pequeno |
| linguagem | Lead time (a) (horas) | Rust (n=29) | TypeScript (n=63) | 1,06 | 1,000 | 0,152 | pequeno |
| linguagem | CFR (b) | Go (n=47) | JavaScript (n=20) | -1,18 | 1,000 | -0,214 | pequeno |
| linguagem | CFR (b) | Go (n=47) | Outras (n=86) | 0,27 | 1,000 | 0,038 | desprezível |
| linguagem | CFR (b) | Go (n=47) | Python (n=53) | -1,16 | 1,000 | -0,127 | desprezível |
| linguagem | CFR (b) | Go (n=47) | Rust (n=29) | -2,86 | 0,051 | -0,404 | médio |
| linguagem | CFR (b) | Go (n=47) | TypeScript (n=80) | -3,81 | 0,002 **\*** | -0,407 | médio |
| linguagem | CFR (b) | JavaScript (n=20) | Outras (n=86) | 1,46 | 1,000 | 0,217 | pequeno |
| linguagem | CFR (b) | JavaScript (n=20) | Python (n=53) | 0,31 | 1,000 | 0,042 | desprezível |
| linguagem | CFR (b) | JavaScript (n=20) | Rust (n=29) | -1,25 | 1,000 | -0,200 | pequeno |
| linguagem | CFR (b) | JavaScript (n=20) | TypeScript (n=80) | -1,55 | 0,974 | -0,251 | pequeno |
| linguagem | CFR (b) | Outras (n=86) | Python (n=53) | -1,61 | 0,958 | -0,166 | pequeno |
| linguagem | CFR (b) | Outras (n=86) | Rust (n=29) | -3,37 | 0,010 **\*** | -0,395 | médio |
| linguagem | CFR (b) | Outras (n=86) | TypeScript (n=80) | -4,82 | < 0,001 **\*** | -0,431 | médio |
| linguagem | CFR (b) | Python (n=53) | Rust (n=29) | -1,92 | 0,554 | -0,255 | pequeno |
| linguagem | CFR (b) | Python (n=53) | TypeScript (n=80) | -2,64 | 0,091 | -0,271 | pequeno |
| linguagem | CFR (b) | Rust (n=29) | TypeScript (n=80) | -0,11 | 1,000 | 0,005 | desprezível |
| idade | Deployment frequency (releases/semana) | Q1 (menor) (n=79) | Q2 (n=79) | 2,09 | 0,109 | 0,169 | pequeno |
| idade | Deployment frequency (releases/semana) | Q1 (menor) (n=79) | Q3 (n=78) | 4,17 | < 0,001 **\*** | 0,384 | médio |
| idade | Deployment frequency (releases/semana) | Q1 (menor) (n=79) | Q4 (maior) (n=79) | 5,77 | < 0,001 **\*** | 0,556 | grande |
| idade | Deployment frequency (releases/semana) | Q2 (n=79) | Q3 (n=78) | 2,09 | 0,109 | 0,180 | pequeno |
| idade | Deployment frequency (releases/semana) | Q2 (n=79) | Q4 (maior) (n=79) | 3,67 | < 0,001 **\*** | 0,326 | pequeno |
| idade | Deployment frequency (releases/semana) | Q3 (n=78) | Q4 (maior) (n=79) | 1,58 | 0,115 | 0,132 | desprezível |
| idade | Lead time (a) (horas) | Q1 (menor) (n=74) | Q2 (n=70) | -4,04 | < 0,001 **\*** | -0,411 | médio |
| idade | Lead time (a) (horas) | Q1 (menor) (n=74) | Q3 (n=67) | -6,65 | < 0,001 **\*** | -0,643 | grande |
| idade | Lead time (a) (horas) | Q1 (menor) (n=74) | Q4 (maior) (n=61) | -7,72 | < 0,001 **\*** | -0,754 | grande |
| idade | Lead time (a) (horas) | Q2 (n=70) | Q3 (n=67) | -2,62 | 0,018 **\*** | -0,270 | pequeno |
| idade | Lead time (a) (horas) | Q2 (n=70) | Q4 (maior) (n=61) | -3,78 | < 0,001 **\*** | -0,396 | médio |
| idade | Lead time (a) (horas) | Q3 (n=67) | Q4 (maior) (n=61) | -1,21 | 0,225 | -0,131 | desprezível |
| idade | CFR (b) | Q1 (menor) (n=79) | Q2 (n=79) | 4,90 | < 0,001 **\*** | 0,461 | médio |
| idade | CFR (b) | Q1 (menor) (n=79) | Q3 (n=78) | 6,82 | < 0,001 **\*** | 0,627 | grande |
| idade | CFR (b) | Q1 (menor) (n=79) | Q4 (maior) (n=79) | 8,04 | < 0,001 **\*** | 0,731 | grande |
| idade | CFR (b) | Q2 (n=79) | Q3 (n=78) | 1,94 | 0,106 | 0,187 | pequeno |
| idade | CFR (b) | Q2 (n=79) | Q4 (maior) (n=79) | 3,14 | 0,005 **\*** | 0,290 | pequeno |
| idade | CFR (b) | Q3 (n=78) | Q4 (maior) (n=79) | 1,19 | 0,233 | 0,116 | desprezível |
| idade | Tempo de recuperação (horas) | Q1 (menor) (n=77) | Q2 (n=72) | -1,57 | 0,349 | -0,158 | pequeno |
| idade | Tempo de recuperação (horas) | Q1 (menor) (n=77) | Q3 (n=69) | -3,06 | 0,011 **\*** | -0,290 | pequeno |
| idade | Tempo de recuperação (horas) | Q1 (menor) (n=77) | Q4 (maior) (n=67) | -3,71 | 0,001 **\*** | -0,352 | médio |
| idade | Tempo de recuperação (horas) | Q2 (n=72) | Q3 (n=69) | -1,49 | 0,349 | -0,148 | pequeno |
| idade | Tempo de recuperação (horas) | Q2 (n=72) | Q4 (maior) (n=67) | -2,13 | 0,132 | -0,217 | pequeno |
| idade | Tempo de recuperação (horas) | Q3 (n=69) | Q4 (maior) (n=67) | -0,65 | 0,517 | -0,063 | desprezível |

δ > 0: o grupo A tende a ter valores maiores que o grupo B.

## Grupos (n e mediana)

| Fator | Grupo | n | Deployment frequency (releases/semana) | Lead time (a) (horas) | CFR (a) | CFR (b) | Tempo de recuperação (horas) |
|---|---|---:|---:|---:|---:|---:|---:|
| linguagem | Go | 47 | 0,307 | 314,831 | 0,054 | 0,333 | 6,117 |
| linguagem | JavaScript | 20 | 0,365 | 88,371 | 0,036 | 0,441 | 2,462 |
| linguagem | Outras | 86 | 0,326 | 409,774 | 0,051 | 0,286 | 3,706 |
| linguagem | Python | 53 | 0,288 | 207,582 | 0,030 | 0,412 | 2,434 |
| linguagem | Rust | 29 | 0,537 | 91,900 | 0,087 | 0,583 | 3,520 |
| linguagem | TypeScript | 80 | 0,537 | 72,804 | 0,064 | 0,620 | 2,684 |
| popularidade | Q1 (menor) | 79 | 0,345 | 101,252 | 0,062 | 0,444 | 2,015 |
| popularidade | Q2 | 79 | 0,326 | 199,748 | 0,050 | 0,333 | 3,159 |
| popularidade | Q3 | 78 | 0,403 | 157,783 | 0,054 | 0,449 | 3,030 |
| popularidade | Q4 (maior) | 79 | 0,326 | 186,361 | 0,042 | 0,400 | 5,988 |
| idade | Q1 (menor) | 79 | 0,614 | 17,994 | 0,067 | 0,769 | 1,518 |
| idade | Q2 | 79 | 0,403 | 153,385 | 0,046 | 0,400 | 2,917 |
| idade | Q3 | 78 | 0,288 | 437,500 | 0,053 | 0,286 | 7,718 |
| idade | Q4 (maior) | 79 | 0,250 | 556,261 | 0,040 | 0,250 | 10,841 |
| tipo | aplicação/serviço | 25 | 0,307 | 390,023 | 0,090 | 0,429 | 3,002 |
| tipo | biblioteca/framework | 20 | 0,336 | 229,876 | 0,040 | 0,361 | 4,292 |
| tipo | ferramenta CLI | 10 | 0,326 | 437,500 | 0,031 | 0,573 | 1,506 |
