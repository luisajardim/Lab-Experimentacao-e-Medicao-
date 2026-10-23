# Histórico da heurística CFR(b) (T14)

Classificador de *release corretiva* usado na variante (b) do change failure
rate. Implementação em `src/metrics/cfr_release.py`; tuning em
`scripts/tune_cfr.py`, avaliado contra `data/gold/labels_consensus.csv` (T13),
com "corretiva = sim" como classe positiva. Meta: **F1 ≥ 0,70**.

## Versões

| Versão | Regra |
|---|---|
| v1 | Corretiva se, frente à release anterior (ordem cronológica), só o `PATCH` do SemVer aumentou (`MAJOR.MINOR` iguais). Tags sem versão reconhecível → não corretiva. |
| v2 | v1 **ou** pelo menos um commit desde a release anterior com mensagem contendo `fix`, `revert` ou `hotfix` (sem diferenciar maiúsculas). |
| v3 | Pontuação `1 · patch_only + 2 · (fração de commits com palavra-chave)`; corretiva se pontuação ≥ corte. |
| v4 | Pontuação `1 · (PATCH > 0 na própria tag) + 2 · (fração de commits com palavra-chave) − peso_feat · (há commit feat)`; corretiva se pontuação ≥ corte. |

O loop de tuning varia, para v2, v3 e v4:

- **conjunto de palavras-chave:** `base` (`fix`, `revert`, `hotfix`) ou
  `ampliado` (+ `bug`, `patch`, `regression`, `crash`);
- **casamento:** `substring` (o enunciado literal; `prefix` casa com `fix`) ou
  `palavra` (início de palavra: `fixes`/`fixed` casam, `prefix` não);
- **corte da v3/v4:** 0,25 a 3,00 em passos de 0,25;
- **peso_feat da v4:** 0, 1 ou 2.

A combinação escolhida é a de maior F1; em empate, vale a mais simples
(v1 → v2 → v3 → v4).

### Por que a v4

Com os commits recoletados (289 de 300 releases), a melhor v3 parou em
F1 = 0,633. A análise dos erros contra o consenso mostrou dois problemas:

1. **Release anterior cronológica ≠ antecessora SemVer.** Em backports a
   release publicada logo antes é de outra linha (ex.: `aeron 1.45.1` depois de
   `1.46.6`; `cakephp 3.9.10` depois de `4.2.6`), e a v1 deixa de reconhecer o
   patch. Usar `PATCH > 0` da própria tag cobre 68 das 71 corretivas do
   consenso (v1: 52), e só 3 das 123 releases com `PATCH = 0` são corretivas.
2. **Commits `feat` indicam release de funcionalidade.** Só 6 das 71
   corretivas têm algum commit `feat`/`feat(...)`, contra 78 das 229 não
   corretivas.

### Ressalvas sobre o F1

- **Otimismo do tuning.** O corte e os pesos são escolhidos na própria
  amostra-ouro. Para estimar o F1 fora da amostra, o script faz validação
  cruzada 5-fold **por repositório** (20 repetições): escolhe a combinação nos
  repositórios de treino e avalia nos demais. Esse número aparece em cada
  execução abaixo e em `cfr_metrics.json` (`cross_validation`).
- **Avaliador B não humano.** O consenso inclui os rótulos do Claude
  (`labels_B.csv`, ver `docs/consensus_protocol.md`). Contra cada avaliador
  isolado, a v4 escolhida obteve F1 = 0,630 (A), 0,695 (B) e 0,632 (C); a v1,
  0,490, 0,611 e 0,469. A v4 melhora sobre a v1 contra os humanos também, mas
  concorda um pouco mais com o avaliador B, o que deve constar como limitação.

## Execuções

A seção abaixo é reescrita por `python scripts/tune_cfr.py`.

<!-- tuning:start -->
## Execução de 2026-10-23T00:40:30+00:00

Gerado por `scripts/tune_cfr.py`; o texto entre os marcadores é reescrito a cada execução.

- Itens (releases com consenso): 300 (104 corretivas)
- Com commits coletados: 188; com release anterior: 294
- Palavras-chave: `base` = fix, revert, hotfix; `ampliado` = fix, revert, hotfix, bug, patch, regression, crash
- **Melhor: v4 kw=base match=palavra feat=-0 corte=0.75** — precisão 0.437, recall 0.837, F1 0.574 (NÃO atinge a meta de 0.70)
- F1 fora da amostra (5-fold por repositório, 20 repetições): média 0.528 (mín. 0.500, máx. 0.556)

### Melhor combinação de cada versão

| Versão | Combinação | F1 |
|---|---|---:|
| v1 | v1 | 0.530 |
| v2 | v2 kw=base match=palavra | 0.539 |
| v3 | v3 kw=base match=palavra corte=0.75 | 0.561 |
| v4 | v4 kw=base match=palavra feat=-0 corte=0.75 | 0.574 |

### Todas as combinações

| Combinação | Precisão | Recall | F1 | TP | FP | FN | TN |
|---|---:|---:|---:|---:|---:|---:|---:|
| v1 | 0.450 | 0.644 | 0.530 | 67 | 82 | 37 | 114 |
| v2 kw=base match=substring | 0.406 | 0.788 | 0.536 | 82 | 120 | 22 | 76 |
| v2 kw=base match=palavra | 0.410 | 0.788 | 0.539 | 82 | 118 | 22 | 78 |
| v2 kw=ampliado match=substring | 0.404 | 0.788 | 0.534 | 82 | 121 | 22 | 75 |
| v2 kw=ampliado match=palavra | 0.406 | 0.788 | 0.536 | 82 | 120 | 22 | 76 |
| v3 kw=base match=substring corte=0.25 | 0.411 | 0.779 | 0.538 | 81 | 116 | 23 | 80 |
| v3 kw=base match=substring corte=0.50 | 0.434 | 0.760 | 0.552 | 79 | 103 | 25 | 93 |
| v3 kw=base match=substring corte=0.75 | 0.452 | 0.731 | 0.559 | 76 | 92 | 28 | 104 |
| v3 kw=base match=substring corte=1.00 | 0.459 | 0.702 | 0.555 | 73 | 86 | 31 | 110 |
| v3 kw=base match=substring corte=1.25 | 0.612 | 0.500 | 0.550 | 52 | 33 | 52 | 163 |
| v3 kw=base match=substring corte=1.50 | 0.600 | 0.433 | 0.503 | 45 | 30 | 59 | 166 |
| v3 kw=base match=substring corte=1.75 | 0.679 | 0.346 | 0.459 | 36 | 17 | 68 | 179 |
| v3 kw=base match=substring corte=2.00 | 0.684 | 0.250 | 0.366 | 26 | 12 | 78 | 184 |
| v3 kw=base match=substring corte=2.25 | 0.696 | 0.154 | 0.252 | 16 | 7 | 88 | 189 |
| v3 kw=base match=substring corte=2.50 | 0.714 | 0.144 | 0.240 | 15 | 6 | 89 | 190 |
| v3 kw=base match=substring corte=2.75 | 0.667 | 0.096 | 0.168 | 10 | 5 | 94 | 191 |
| v3 kw=base match=substring corte=3.00 | 0.615 | 0.077 | 0.137 | 8 | 5 | 96 | 191 |
| v3 kw=base match=palavra corte=0.25 | 0.413 | 0.779 | 0.540 | 81 | 115 | 23 | 81 |
| v3 kw=base match=palavra corte=0.50 | 0.434 | 0.760 | 0.552 | 79 | 103 | 25 | 93 |
| v3 kw=base match=palavra corte=0.75 | 0.455 | 0.731 | 0.561 | 76 | 91 | 28 | 105 |
| v3 kw=base match=palavra corte=1.00 | 0.459 | 0.692 | 0.552 | 72 | 85 | 32 | 111 |
| v3 kw=base match=palavra corte=1.25 | 0.619 | 0.500 | 0.553 | 52 | 32 | 52 | 164 |
| v3 kw=base match=palavra corte=1.50 | 0.608 | 0.433 | 0.506 | 45 | 29 | 59 | 167 |
| v3 kw=base match=palavra corte=1.75 | 0.667 | 0.327 | 0.439 | 34 | 17 | 70 | 179 |
| v3 kw=base match=palavra corte=2.00 | 0.694 | 0.240 | 0.357 | 25 | 11 | 79 | 185 |
| v3 kw=base match=palavra corte=2.25 | 0.682 | 0.144 | 0.238 | 15 | 7 | 89 | 189 |
| v3 kw=base match=palavra corte=2.50 | 0.700 | 0.135 | 0.226 | 14 | 6 | 90 | 190 |
| v3 kw=base match=palavra corte=2.75 | 0.667 | 0.096 | 0.168 | 10 | 5 | 94 | 191 |
| v3 kw=base match=palavra corte=3.00 | 0.615 | 0.077 | 0.137 | 8 | 5 | 96 | 191 |
| v3 kw=ampliado match=substring corte=0.25 | 0.407 | 0.779 | 0.535 | 81 | 118 | 23 | 78 |
| v3 kw=ampliado match=substring corte=0.50 | 0.425 | 0.760 | 0.545 | 79 | 107 | 25 | 89 |
| v3 kw=ampliado match=substring corte=0.75 | 0.450 | 0.731 | 0.557 | 76 | 93 | 28 | 103 |
| v3 kw=ampliado match=substring corte=1.00 | 0.453 | 0.702 | 0.551 | 73 | 88 | 31 | 108 |
| v3 kw=ampliado match=substring corte=1.25 | 0.602 | 0.510 | 0.552 | 53 | 35 | 51 | 161 |
| v3 kw=ampliado match=substring corte=1.50 | 0.603 | 0.452 | 0.516 | 47 | 31 | 57 | 165 |
| v3 kw=ampliado match=substring corte=1.75 | 0.679 | 0.365 | 0.475 | 38 | 18 | 66 | 178 |
| v3 kw=ampliado match=substring corte=2.00 | 0.667 | 0.269 | 0.384 | 28 | 14 | 76 | 182 |
| v3 kw=ampliado match=substring corte=2.25 | 0.708 | 0.163 | 0.266 | 17 | 7 | 87 | 189 |
| v3 kw=ampliado match=substring corte=2.50 | 0.727 | 0.154 | 0.254 | 16 | 6 | 88 | 190 |
| v3 kw=ampliado match=substring corte=2.75 | 0.667 | 0.096 | 0.168 | 10 | 5 | 94 | 191 |
| v3 kw=ampliado match=substring corte=3.00 | 0.615 | 0.077 | 0.137 | 8 | 5 | 96 | 191 |
| v3 kw=ampliado match=palavra corte=0.25 | 0.409 | 0.779 | 0.536 | 81 | 117 | 23 | 79 |
| v3 kw=ampliado match=palavra corte=0.50 | 0.429 | 0.760 | 0.549 | 79 | 105 | 25 | 91 |
| v3 kw=ampliado match=palavra corte=0.75 | 0.450 | 0.731 | 0.557 | 76 | 93 | 28 | 103 |
| v3 kw=ampliado match=palavra corte=1.00 | 0.450 | 0.692 | 0.545 | 72 | 88 | 32 | 108 |
| v3 kw=ampliado match=palavra corte=1.25 | 0.609 | 0.510 | 0.555 | 53 | 34 | 51 | 162 |
| v3 kw=ampliado match=palavra corte=1.50 | 0.597 | 0.442 | 0.508 | 46 | 31 | 58 | 165 |
| v3 kw=ampliado match=palavra corte=1.75 | 0.673 | 0.356 | 0.465 | 37 | 18 | 67 | 178 |
| v3 kw=ampliado match=palavra corte=2.00 | 0.692 | 0.260 | 0.378 | 27 | 12 | 77 | 184 |
| v3 kw=ampliado match=palavra corte=2.25 | 0.682 | 0.144 | 0.238 | 15 | 7 | 89 | 189 |
| v3 kw=ampliado match=palavra corte=2.50 | 0.714 | 0.144 | 0.240 | 15 | 6 | 89 | 190 |
| v3 kw=ampliado match=palavra corte=2.75 | 0.667 | 0.096 | 0.168 | 10 | 5 | 94 | 191 |
| v3 kw=ampliado match=palavra corte=3.00 | 0.615 | 0.077 | 0.137 | 8 | 5 | 96 | 191 |
| v4 kw=base match=substring feat=-0 corte=0.25 | 0.404 | 0.865 | 0.550 | 90 | 133 | 14 | 63 |
| v4 kw=base match=substring feat=-0 corte=0.50 | 0.421 | 0.846 | 0.562 | 88 | 121 | 16 | 75 |
| v4 kw=base match=substring feat=-0 corte=0.75 | 0.435 | 0.837 | 0.572 | 87 | 113 | 17 | 83 |
| v4 kw=base match=substring feat=-0 corte=1.00 | 0.438 | 0.817 | 0.570 | 85 | 109 | 19 | 87 |
| v4 kw=base match=substring feat=-0 corte=1.25 | 0.589 | 0.538 | 0.563 | 56 | 39 | 48 | 157 |
| v4 kw=base match=substring feat=-0 corte=1.50 | 0.583 | 0.471 | 0.521 | 49 | 35 | 55 | 161 |
| v4 kw=base match=substring feat=-0 corte=1.75 | 0.667 | 0.365 | 0.472 | 38 | 19 | 66 | 177 |
| v4 kw=base match=substring feat=-0 corte=2.00 | 0.692 | 0.260 | 0.378 | 27 | 12 | 77 | 184 |
| v4 kw=base match=substring feat=-0 corte=2.25 | 0.696 | 0.154 | 0.252 | 16 | 7 | 88 | 189 |
| v4 kw=base match=substring feat=-0 corte=2.50 | 0.714 | 0.144 | 0.240 | 15 | 6 | 89 | 190 |
| v4 kw=base match=substring feat=-0 corte=2.75 | 0.667 | 0.096 | 0.168 | 10 | 5 | 94 | 191 |
| v4 kw=base match=substring feat=-0 corte=3.00 | 0.615 | 0.077 | 0.137 | 8 | 5 | 96 | 191 |
| v4 kw=base match=substring feat=-1 corte=0.25 | 0.419 | 0.817 | 0.554 | 85 | 118 | 19 | 78 |
| v4 kw=base match=substring feat=-1 corte=0.50 | 0.430 | 0.798 | 0.559 | 83 | 110 | 21 | 86 |
| v4 kw=base match=substring feat=-1 corte=0.75 | 0.443 | 0.740 | 0.554 | 77 | 97 | 27 | 99 |
| v4 kw=base match=substring feat=-1 corte=1.00 | 0.427 | 0.673 | 0.522 | 70 | 94 | 34 | 102 |
| v4 kw=base match=substring feat=-1 corte=1.25 | 0.629 | 0.423 | 0.506 | 44 | 26 | 60 | 170 |
| v4 kw=base match=substring feat=-1 corte=1.50 | 0.623 | 0.365 | 0.461 | 38 | 23 | 66 | 173 |
| v4 kw=base match=substring feat=-1 corte=1.75 | 0.711 | 0.308 | 0.430 | 32 | 13 | 72 | 183 |
| v4 kw=base match=substring feat=-1 corte=2.00 | 0.743 | 0.250 | 0.374 | 26 | 9 | 78 | 187 |
| v4 kw=base match=substring feat=-1 corte=2.25 | 0.727 | 0.154 | 0.254 | 16 | 6 | 88 | 190 |
| v4 kw=base match=substring feat=-1 corte=2.50 | 0.714 | 0.144 | 0.240 | 15 | 6 | 89 | 190 |
| v4 kw=base match=substring feat=-1 corte=2.75 | 0.667 | 0.096 | 0.168 | 10 | 5 | 94 | 191 |
| v4 kw=base match=substring feat=-1 corte=3.00 | 0.615 | 0.077 | 0.137 | 8 | 5 | 96 | 191 |
| v4 kw=base match=substring feat=-2 corte=0.25 | 0.410 | 0.702 | 0.518 | 73 | 105 | 31 | 91 |
| v4 kw=base match=substring feat=-2 corte=0.50 | 0.424 | 0.692 | 0.526 | 72 | 98 | 32 | 98 |
| v4 kw=base match=substring feat=-2 corte=0.75 | 0.438 | 0.683 | 0.534 | 71 | 91 | 33 | 105 |
| v4 kw=base match=substring feat=-2 corte=1.00 | 0.431 | 0.663 | 0.523 | 69 | 91 | 35 | 105 |
| v4 kw=base match=substring feat=-2 corte=1.25 | 0.638 | 0.423 | 0.509 | 44 | 25 | 60 | 171 |
| v4 kw=base match=substring feat=-2 corte=1.50 | 0.623 | 0.365 | 0.461 | 38 | 23 | 66 | 173 |
| v4 kw=base match=substring feat=-2 corte=1.75 | 0.711 | 0.308 | 0.430 | 32 | 13 | 72 | 183 |
| v4 kw=base match=substring feat=-2 corte=2.00 | 0.743 | 0.250 | 0.374 | 26 | 9 | 78 | 187 |
| v4 kw=base match=substring feat=-2 corte=2.25 | 0.727 | 0.154 | 0.254 | 16 | 6 | 88 | 190 |
| v4 kw=base match=substring feat=-2 corte=2.50 | 0.714 | 0.144 | 0.240 | 15 | 6 | 89 | 190 |
| v4 kw=base match=substring feat=-2 corte=2.75 | 0.667 | 0.096 | 0.168 | 10 | 5 | 94 | 191 |
| v4 kw=base match=substring feat=-2 corte=3.00 | 0.615 | 0.077 | 0.137 | 8 | 5 | 96 | 191 |
| v4 kw=base match=palavra feat=-0 corte=0.25 | 0.405 | 0.865 | 0.552 | 90 | 132 | 14 | 64 |
| v4 kw=base match=palavra feat=-0 corte=0.50 | 0.421 | 0.846 | 0.562 | 88 | 121 | 16 | 75 |
| v4 kw=base match=palavra feat=-0 corte=0.75 | 0.437 | 0.837 | 0.574 | 87 | 112 | 17 | 84 |
| v4 kw=base match=palavra feat=-0 corte=1.00 | 0.438 | 0.808 | 0.568 | 84 | 108 | 20 | 88 |
| v4 kw=base match=palavra feat=-0 corte=1.25 | 0.596 | 0.538 | 0.566 | 56 | 38 | 48 | 158 |
| v4 kw=base match=palavra feat=-0 corte=1.50 | 0.590 | 0.471 | 0.524 | 49 | 34 | 55 | 162 |
| v4 kw=base match=palavra feat=-0 corte=1.75 | 0.655 | 0.346 | 0.453 | 36 | 19 | 68 | 177 |
| v4 kw=base match=palavra feat=-0 corte=2.00 | 0.703 | 0.250 | 0.369 | 26 | 11 | 78 | 185 |
| v4 kw=base match=palavra feat=-0 corte=2.25 | 0.682 | 0.144 | 0.238 | 15 | 7 | 89 | 189 |
| v4 kw=base match=palavra feat=-0 corte=2.50 | 0.700 | 0.135 | 0.226 | 14 | 6 | 90 | 190 |
| v4 kw=base match=palavra feat=-0 corte=2.75 | 0.667 | 0.096 | 0.168 | 10 | 5 | 94 | 191 |
| v4 kw=base match=palavra feat=-0 corte=3.00 | 0.615 | 0.077 | 0.137 | 8 | 5 | 96 | 191 |
| v4 kw=base match=palavra feat=-1 corte=0.25 | 0.423 | 0.817 | 0.557 | 85 | 116 | 19 | 80 |
| v4 kw=base match=palavra feat=-1 corte=0.50 | 0.430 | 0.798 | 0.559 | 83 | 110 | 21 | 86 |
| v4 kw=base match=palavra feat=-1 corte=0.75 | 0.445 | 0.740 | 0.556 | 77 | 96 | 27 | 100 |
| v4 kw=base match=palavra feat=-1 corte=1.00 | 0.429 | 0.673 | 0.524 | 70 | 93 | 34 | 103 |
| v4 kw=base match=palavra feat=-1 corte=1.25 | 0.629 | 0.423 | 0.506 | 44 | 26 | 60 | 170 |
| v4 kw=base match=palavra feat=-1 corte=1.50 | 0.633 | 0.365 | 0.463 | 38 | 22 | 66 | 174 |
| v4 kw=base match=palavra feat=-1 corte=1.75 | 0.698 | 0.288 | 0.408 | 30 | 13 | 74 | 183 |
| v4 kw=base match=palavra feat=-1 corte=2.00 | 0.758 | 0.240 | 0.365 | 25 | 8 | 79 | 188 |
| v4 kw=base match=palavra feat=-1 corte=2.25 | 0.714 | 0.144 | 0.240 | 15 | 6 | 89 | 190 |
| v4 kw=base match=palavra feat=-1 corte=2.50 | 0.700 | 0.135 | 0.226 | 14 | 6 | 90 | 190 |
| v4 kw=base match=palavra feat=-1 corte=2.75 | 0.667 | 0.096 | 0.168 | 10 | 5 | 94 | 191 |
| v4 kw=base match=palavra feat=-1 corte=3.00 | 0.615 | 0.077 | 0.137 | 8 | 5 | 96 | 191 |
| v4 kw=base match=palavra feat=-2 corte=0.25 | 0.412 | 0.702 | 0.520 | 73 | 104 | 31 | 92 |
| v4 kw=base match=palavra feat=-2 corte=0.50 | 0.424 | 0.692 | 0.526 | 72 | 98 | 32 | 98 |
| v4 kw=base match=palavra feat=-2 corte=0.75 | 0.441 | 0.683 | 0.536 | 71 | 90 | 33 | 106 |
| v4 kw=base match=palavra feat=-2 corte=1.00 | 0.434 | 0.663 | 0.525 | 69 | 90 | 35 | 106 |
| v4 kw=base match=palavra feat=-2 corte=1.25 | 0.638 | 0.423 | 0.509 | 44 | 25 | 60 | 171 |
| v4 kw=base match=palavra feat=-2 corte=1.50 | 0.633 | 0.365 | 0.463 | 38 | 22 | 66 | 174 |
| v4 kw=base match=palavra feat=-2 corte=1.75 | 0.698 | 0.288 | 0.408 | 30 | 13 | 74 | 183 |
| v4 kw=base match=palavra feat=-2 corte=2.00 | 0.758 | 0.240 | 0.365 | 25 | 8 | 79 | 188 |
| v4 kw=base match=palavra feat=-2 corte=2.25 | 0.714 | 0.144 | 0.240 | 15 | 6 | 89 | 190 |
| v4 kw=base match=palavra feat=-2 corte=2.50 | 0.700 | 0.135 | 0.226 | 14 | 6 | 90 | 190 |
| v4 kw=base match=palavra feat=-2 corte=2.75 | 0.667 | 0.096 | 0.168 | 10 | 5 | 94 | 191 |
| v4 kw=base match=palavra feat=-2 corte=3.00 | 0.615 | 0.077 | 0.137 | 8 | 5 | 96 | 191 |
| v4 kw=ampliado match=substring feat=-0 corte=0.25 | 0.400 | 0.865 | 0.547 | 90 | 135 | 14 | 61 |
| v4 kw=ampliado match=substring feat=-0 corte=0.50 | 0.413 | 0.846 | 0.555 | 88 | 125 | 16 | 71 |
| v4 kw=ampliado match=substring feat=-0 corte=0.75 | 0.433 | 0.837 | 0.570 | 87 | 114 | 17 | 82 |
| v4 kw=ampliado match=substring feat=-0 corte=1.00 | 0.438 | 0.817 | 0.570 | 85 | 109 | 19 | 87 |
| v4 kw=ampliado match=substring feat=-0 corte=1.25 | 0.588 | 0.548 | 0.567 | 57 | 40 | 47 | 156 |
| v4 kw=ampliado match=substring feat=-0 corte=1.50 | 0.593 | 0.490 | 0.537 | 51 | 35 | 53 | 161 |
| v4 kw=ampliado match=substring feat=-0 corte=1.75 | 0.667 | 0.385 | 0.488 | 40 | 20 | 64 | 176 |
| v4 kw=ampliado match=substring feat=-0 corte=2.00 | 0.644 | 0.279 | 0.389 | 29 | 16 | 75 | 180 |
| v4 kw=ampliado match=substring feat=-0 corte=2.25 | 0.680 | 0.163 | 0.264 | 17 | 8 | 87 | 188 |
| v4 kw=ampliado match=substring feat=-0 corte=2.50 | 0.696 | 0.154 | 0.252 | 16 | 7 | 88 | 189 |
| v4 kw=ampliado match=substring feat=-0 corte=2.75 | 0.667 | 0.096 | 0.168 | 10 | 5 | 94 | 191 |
| v4 kw=ampliado match=substring feat=-0 corte=3.00 | 0.615 | 0.077 | 0.137 | 8 | 5 | 96 | 191 |
| v4 kw=ampliado match=substring feat=-1 corte=0.25 | 0.422 | 0.827 | 0.558 | 86 | 118 | 18 | 78 |
| v4 kw=ampliado match=substring feat=-1 corte=0.50 | 0.430 | 0.798 | 0.559 | 83 | 110 | 21 | 86 |
| v4 kw=ampliado match=substring feat=-1 corte=0.75 | 0.446 | 0.750 | 0.559 | 78 | 97 | 26 | 99 |
| v4 kw=ampliado match=substring feat=-1 corte=1.00 | 0.424 | 0.673 | 0.520 | 70 | 95 | 34 | 101 |
| v4 kw=ampliado match=substring feat=-1 corte=1.25 | 0.620 | 0.423 | 0.503 | 44 | 27 | 60 | 169 |
| v4 kw=ampliado match=substring feat=-1 corte=1.50 | 0.635 | 0.385 | 0.479 | 40 | 23 | 64 | 173 |
| v4 kw=ampliado match=substring feat=-1 corte=1.75 | 0.702 | 0.317 | 0.437 | 33 | 14 | 71 | 182 |
| v4 kw=ampliado match=substring feat=-1 corte=2.00 | 0.700 | 0.269 | 0.389 | 28 | 12 | 76 | 184 |
| v4 kw=ampliado match=substring feat=-1 corte=2.25 | 0.708 | 0.163 | 0.266 | 17 | 7 | 87 | 189 |
| v4 kw=ampliado match=substring feat=-1 corte=2.50 | 0.696 | 0.154 | 0.252 | 16 | 7 | 88 | 189 |
| v4 kw=ampliado match=substring feat=-1 corte=2.75 | 0.667 | 0.096 | 0.168 | 10 | 5 | 94 | 191 |
| v4 kw=ampliado match=substring feat=-1 corte=3.00 | 0.615 | 0.077 | 0.137 | 8 | 5 | 96 | 191 |
| v4 kw=ampliado match=substring feat=-2 corte=0.25 | 0.410 | 0.702 | 0.518 | 73 | 105 | 31 | 91 |
| v4 kw=ampliado match=substring feat=-2 corte=0.50 | 0.424 | 0.692 | 0.526 | 72 | 98 | 32 | 98 |
| v4 kw=ampliado match=substring feat=-2 corte=0.75 | 0.438 | 0.683 | 0.534 | 71 | 91 | 33 | 105 |
| v4 kw=ampliado match=substring feat=-2 corte=1.00 | 0.431 | 0.663 | 0.523 | 69 | 91 | 35 | 105 |
| v4 kw=ampliado match=substring feat=-2 corte=1.25 | 0.629 | 0.423 | 0.506 | 44 | 26 | 60 | 170 |
| v4 kw=ampliado match=substring feat=-2 corte=1.50 | 0.635 | 0.385 | 0.479 | 40 | 23 | 64 | 173 |
| v4 kw=ampliado match=substring feat=-2 corte=1.75 | 0.702 | 0.317 | 0.437 | 33 | 14 | 71 | 182 |
| v4 kw=ampliado match=substring feat=-2 corte=2.00 | 0.700 | 0.269 | 0.389 | 28 | 12 | 76 | 184 |
| v4 kw=ampliado match=substring feat=-2 corte=2.25 | 0.708 | 0.163 | 0.266 | 17 | 7 | 87 | 189 |
| v4 kw=ampliado match=substring feat=-2 corte=2.50 | 0.696 | 0.154 | 0.252 | 16 | 7 | 88 | 189 |
| v4 kw=ampliado match=substring feat=-2 corte=2.75 | 0.667 | 0.096 | 0.168 | 10 | 5 | 94 | 191 |
| v4 kw=ampliado match=substring feat=-2 corte=3.00 | 0.615 | 0.077 | 0.137 | 8 | 5 | 96 | 191 |
| v4 kw=ampliado match=palavra feat=-0 corte=0.25 | 0.402 | 0.865 | 0.549 | 90 | 134 | 14 | 62 |
| v4 kw=ampliado match=palavra feat=-0 corte=0.50 | 0.417 | 0.846 | 0.559 | 88 | 123 | 16 | 73 |
| v4 kw=ampliado match=palavra feat=-0 corte=0.75 | 0.433 | 0.837 | 0.570 | 87 | 114 | 17 | 82 |
| v4 kw=ampliado match=palavra feat=-0 corte=1.00 | 0.435 | 0.808 | 0.566 | 84 | 109 | 20 | 87 |
| v4 kw=ampliado match=palavra feat=-0 corte=1.25 | 0.594 | 0.548 | 0.570 | 57 | 39 | 47 | 157 |
| v4 kw=ampliado match=palavra feat=-0 corte=1.50 | 0.588 | 0.481 | 0.529 | 50 | 35 | 54 | 161 |
| v4 kw=ampliado match=palavra feat=-0 corte=1.75 | 0.661 | 0.375 | 0.479 | 39 | 20 | 65 | 176 |
| v4 kw=ampliado match=palavra feat=-0 corte=2.00 | 0.667 | 0.269 | 0.384 | 28 | 14 | 76 | 182 |
| v4 kw=ampliado match=palavra feat=-0 corte=2.25 | 0.652 | 0.144 | 0.236 | 15 | 8 | 89 | 188 |
| v4 kw=ampliado match=palavra feat=-0 corte=2.50 | 0.682 | 0.144 | 0.238 | 15 | 7 | 89 | 189 |
| v4 kw=ampliado match=palavra feat=-0 corte=2.75 | 0.667 | 0.096 | 0.168 | 10 | 5 | 94 | 191 |
| v4 kw=ampliado match=palavra feat=-0 corte=3.00 | 0.615 | 0.077 | 0.137 | 8 | 5 | 96 | 191 |
| v4 kw=ampliado match=palavra feat=-1 corte=0.25 | 0.424 | 0.827 | 0.560 | 86 | 117 | 18 | 79 |
| v4 kw=ampliado match=palavra feat=-1 corte=0.50 | 0.430 | 0.798 | 0.559 | 83 | 110 | 21 | 86 |
| v4 kw=ampliado match=palavra feat=-1 corte=0.75 | 0.446 | 0.750 | 0.559 | 78 | 97 | 26 | 99 |
| v4 kw=ampliado match=palavra feat=-1 corte=1.00 | 0.424 | 0.673 | 0.520 | 70 | 95 | 34 | 101 |
| v4 kw=ampliado match=palavra feat=-1 corte=1.25 | 0.620 | 0.423 | 0.503 | 44 | 27 | 60 | 169 |
| v4 kw=ampliado match=palavra feat=-1 corte=1.50 | 0.629 | 0.375 | 0.470 | 39 | 23 | 65 | 173 |
| v4 kw=ampliado match=palavra feat=-1 corte=1.75 | 0.696 | 0.308 | 0.427 | 32 | 14 | 72 | 182 |
| v4 kw=ampliado match=palavra feat=-1 corte=2.00 | 0.730 | 0.260 | 0.383 | 27 | 10 | 77 | 186 |
| v4 kw=ampliado match=palavra feat=-1 corte=2.25 | 0.682 | 0.144 | 0.238 | 15 | 7 | 89 | 189 |
| v4 kw=ampliado match=palavra feat=-1 corte=2.50 | 0.682 | 0.144 | 0.238 | 15 | 7 | 89 | 189 |
| v4 kw=ampliado match=palavra feat=-1 corte=2.75 | 0.667 | 0.096 | 0.168 | 10 | 5 | 94 | 191 |
| v4 kw=ampliado match=palavra feat=-1 corte=3.00 | 0.615 | 0.077 | 0.137 | 8 | 5 | 96 | 191 |
| v4 kw=ampliado match=palavra feat=-2 corte=0.25 | 0.410 | 0.702 | 0.518 | 73 | 105 | 31 | 91 |
| v4 kw=ampliado match=palavra feat=-2 corte=0.50 | 0.424 | 0.692 | 0.526 | 72 | 98 | 32 | 98 |
| v4 kw=ampliado match=palavra feat=-2 corte=0.75 | 0.438 | 0.683 | 0.534 | 71 | 91 | 33 | 105 |
| v4 kw=ampliado match=palavra feat=-2 corte=1.00 | 0.431 | 0.663 | 0.523 | 69 | 91 | 35 | 105 |
| v4 kw=ampliado match=palavra feat=-2 corte=1.25 | 0.629 | 0.423 | 0.506 | 44 | 26 | 60 | 170 |
| v4 kw=ampliado match=palavra feat=-2 corte=1.50 | 0.629 | 0.375 | 0.470 | 39 | 23 | 65 | 173 |
| v4 kw=ampliado match=palavra feat=-2 corte=1.75 | 0.696 | 0.308 | 0.427 | 32 | 14 | 72 | 182 |
| v4 kw=ampliado match=palavra feat=-2 corte=2.00 | 0.730 | 0.260 | 0.383 | 27 | 10 | 77 | 186 |
| v4 kw=ampliado match=palavra feat=-2 corte=2.25 | 0.682 | 0.144 | 0.238 | 15 | 7 | 89 | 189 |
| v4 kw=ampliado match=palavra feat=-2 corte=2.50 | 0.682 | 0.144 | 0.238 | 15 | 7 | 89 | 189 |
| v4 kw=ampliado match=palavra feat=-2 corte=2.75 | 0.667 | 0.096 | 0.168 | 10 | 5 | 94 | 191 |
| v4 kw=ampliado match=palavra feat=-2 corte=3.00 | 0.615 | 0.077 | 0.137 | 8 | 5 | 96 | 191 |
<!-- tuning:end -->
