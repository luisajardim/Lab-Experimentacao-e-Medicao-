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
## Execução de 2026-10-15T19:52:26+00:00

Gerado por `scripts/tune_cfr.py`; o texto entre os marcadores é reescrito a cada execução.

- Itens (releases com consenso): 300 (71 corretivas)
- Com commits coletados: 289; com release anterior: 289
- Palavras-chave: `base` = fix, revert, hotfix; `ampliado` = fix, revert, hotfix, bug, patch, regression, crash
- **Melhor: v4 kw=base match=palavra feat=-1 corte=1.50** — precisão 0.644, recall 0.789, F1 0.709 (atinge a meta de 0.70)
- F1 fora da amostra (5-fold por repositório, 20 repetições): média 0.693 (mín. 0.657, máx. 0.709)

### Melhor combinação de cada versão

| Versão | Combinação | F1 |
|---|---|---:|
| v1 | v1 | 0.528 |
| v2 | v2 kw=base match=palavra | 0.419 |
| v3 | v3 kw=base match=palavra corte=1.50 | 0.633 |
| v4 | v4 kw=base match=palavra feat=-1 corte=1.50 | 0.709 |

### Todas as combinações

| Combinação | Precisão | Recall | F1 | TP | FP | FN | TN |
|---|---:|---:|---:|---:|---:|---:|---:|
| v1 | 0.413 | 0.732 | 0.528 | 52 | 74 | 19 | 155 |
| v2 kw=base match=substring | 0.263 | 1.000 | 0.416 | 71 | 199 | 0 | 30 |
| v2 kw=base match=palavra | 0.265 | 1.000 | 0.419 | 71 | 197 | 0 | 32 |
| v2 kw=ampliado match=substring | 0.262 | 1.000 | 0.415 | 71 | 200 | 0 | 29 |
| v2 kw=ampliado match=palavra | 0.262 | 1.000 | 0.415 | 71 | 200 | 0 | 29 |
| v3 kw=base match=substring corte=0.25 | 0.279 | 0.986 | 0.435 | 70 | 181 | 1 | 48 |
| v3 kw=base match=substring corte=0.50 | 0.306 | 0.930 | 0.460 | 66 | 150 | 5 | 79 |
| v3 kw=base match=substring corte=0.75 | 0.350 | 0.873 | 0.500 | 62 | 115 | 9 | 114 |
| v3 kw=base match=substring corte=1.00 | 0.391 | 0.859 | 0.537 | 61 | 95 | 10 | 134 |
| v3 kw=base match=substring corte=1.25 | 0.442 | 0.746 | 0.555 | 53 | 67 | 18 | 162 |
| v3 kw=base match=substring corte=1.50 | 0.554 | 0.718 | 0.626 | 51 | 41 | 20 | 188 |
| v3 kw=base match=substring corte=1.75 | 0.623 | 0.606 | 0.614 | 43 | 26 | 28 | 203 |
| v3 kw=base match=substring corte=2.00 | 0.702 | 0.465 | 0.559 | 33 | 14 | 38 | 215 |
| v3 kw=base match=substring corte=2.25 | 0.727 | 0.225 | 0.344 | 16 | 6 | 55 | 223 |
| v3 kw=base match=substring corte=2.50 | 0.769 | 0.141 | 0.238 | 10 | 3 | 61 | 226 |
| v3 kw=base match=substring corte=2.75 | 0.833 | 0.070 | 0.130 | 5 | 1 | 66 | 228 |
| v3 kw=base match=substring corte=3.00 | 0.750 | 0.042 | 0.080 | 3 | 1 | 68 | 228 |
| v3 kw=base match=palavra corte=0.25 | 0.280 | 0.986 | 0.436 | 70 | 180 | 1 | 49 |
| v3 kw=base match=palavra corte=0.50 | 0.306 | 0.930 | 0.460 | 66 | 150 | 5 | 79 |
| v3 kw=base match=palavra corte=0.75 | 0.352 | 0.873 | 0.502 | 62 | 114 | 9 | 115 |
| v3 kw=base match=palavra corte=1.00 | 0.394 | 0.859 | 0.540 | 61 | 94 | 10 | 135 |
| v3 kw=base match=palavra corte=1.25 | 0.442 | 0.746 | 0.555 | 53 | 67 | 18 | 162 |
| v3 kw=base match=palavra corte=1.50 | 0.567 | 0.718 | 0.634 | 51 | 39 | 20 | 190 |
| v3 kw=base match=palavra corte=1.75 | 0.652 | 0.606 | 0.628 | 43 | 23 | 28 | 206 |
| v3 kw=base match=palavra corte=2.00 | 0.717 | 0.465 | 0.564 | 33 | 13 | 38 | 216 |
| v3 kw=base match=palavra corte=2.25 | 0.727 | 0.225 | 0.344 | 16 | 6 | 55 | 223 |
| v3 kw=base match=palavra corte=2.50 | 0.769 | 0.141 | 0.238 | 10 | 3 | 61 | 226 |
| v3 kw=base match=palavra corte=2.75 | 0.833 | 0.070 | 0.130 | 5 | 1 | 66 | 228 |
| v3 kw=base match=palavra corte=3.00 | 0.750 | 0.042 | 0.080 | 3 | 1 | 68 | 228 |
| v3 kw=ampliado match=substring corte=0.25 | 0.275 | 0.986 | 0.429 | 70 | 185 | 1 | 44 |
| v3 kw=ampliado match=substring corte=0.50 | 0.295 | 0.944 | 0.450 | 67 | 160 | 4 | 69 |
| v3 kw=ampliado match=substring corte=0.75 | 0.335 | 0.873 | 0.484 | 62 | 123 | 9 | 106 |
| v3 kw=ampliado match=substring corte=1.00 | 0.374 | 0.859 | 0.521 | 61 | 102 | 10 | 127 |
| v3 kw=ampliado match=substring corte=1.25 | 0.432 | 0.761 | 0.551 | 54 | 71 | 17 | 158 |
| v3 kw=ampliado match=substring corte=1.50 | 0.531 | 0.718 | 0.611 | 51 | 45 | 20 | 184 |
| v3 kw=ampliado match=substring corte=1.75 | 0.592 | 0.634 | 0.612 | 45 | 31 | 26 | 198 |
| v3 kw=ampliado match=substring corte=2.00 | 0.667 | 0.507 | 0.576 | 36 | 18 | 35 | 211 |
| v3 kw=ampliado match=substring corte=2.25 | 0.708 | 0.239 | 0.358 | 17 | 7 | 54 | 222 |
| v3 kw=ampliado match=substring corte=2.50 | 0.786 | 0.155 | 0.259 | 11 | 3 | 60 | 226 |
| v3 kw=ampliado match=substring corte=2.75 | 0.857 | 0.085 | 0.154 | 6 | 1 | 65 | 228 |
| v3 kw=ampliado match=substring corte=3.00 | 0.800 | 0.056 | 0.105 | 4 | 1 | 67 | 228 |
| v3 kw=ampliado match=palavra corte=0.25 | 0.275 | 0.986 | 0.429 | 70 | 185 | 1 | 44 |
| v3 kw=ampliado match=palavra corte=0.50 | 0.293 | 0.930 | 0.446 | 66 | 159 | 5 | 70 |
| v3 kw=ampliado match=palavra corte=0.75 | 0.343 | 0.873 | 0.492 | 62 | 119 | 9 | 110 |
| v3 kw=ampliado match=palavra corte=1.00 | 0.384 | 0.859 | 0.530 | 61 | 98 | 10 | 131 |
| v3 kw=ampliado match=palavra corte=1.25 | 0.432 | 0.761 | 0.551 | 54 | 71 | 17 | 158 |
| v3 kw=ampliado match=palavra corte=1.50 | 0.531 | 0.718 | 0.611 | 51 | 45 | 20 | 184 |
| v3 kw=ampliado match=palavra corte=1.75 | 0.595 | 0.620 | 0.607 | 44 | 30 | 27 | 199 |
| v3 kw=ampliado match=palavra corte=2.00 | 0.686 | 0.493 | 0.574 | 35 | 16 | 36 | 213 |
| v3 kw=ampliado match=palavra corte=2.25 | 0.739 | 0.239 | 0.362 | 17 | 6 | 54 | 223 |
| v3 kw=ampliado match=palavra corte=2.50 | 0.786 | 0.155 | 0.259 | 11 | 3 | 60 | 226 |
| v3 kw=ampliado match=palavra corte=2.75 | 0.857 | 0.085 | 0.154 | 6 | 1 | 65 | 228 |
| v3 kw=ampliado match=palavra corte=3.00 | 0.800 | 0.056 | 0.105 | 4 | 1 | 67 | 228 |
| v4 kw=base match=substring feat=-0 corte=0.25 | 0.266 | 1.000 | 0.420 | 71 | 196 | 0 | 33 |
| v4 kw=base match=substring feat=-0 corte=0.50 | 0.297 | 1.000 | 0.458 | 71 | 168 | 0 | 61 |
| v4 kw=base match=substring feat=-0 corte=0.75 | 0.335 | 1.000 | 0.502 | 71 | 141 | 0 | 88 |
| v4 kw=base match=substring feat=-0 corte=1.00 | 0.363 | 0.986 | 0.530 | 70 | 123 | 1 | 106 |
| v4 kw=base match=substring feat=-0 corte=1.25 | 0.433 | 0.915 | 0.588 | 65 | 85 | 6 | 144 |
| v4 kw=base match=substring feat=-0 corte=1.50 | 0.517 | 0.845 | 0.642 | 60 | 56 | 11 | 173 |
| v4 kw=base match=substring feat=-0 corte=1.75 | 0.593 | 0.676 | 0.632 | 48 | 33 | 23 | 196 |
| v4 kw=base match=substring feat=-0 corte=2.00 | 0.672 | 0.549 | 0.605 | 39 | 19 | 32 | 210 |
| v4 kw=base match=substring feat=-0 corte=2.25 | 0.704 | 0.268 | 0.388 | 19 | 8 | 52 | 221 |
| v4 kw=base match=substring feat=-0 corte=2.50 | 0.706 | 0.169 | 0.273 | 12 | 5 | 59 | 224 |
| v4 kw=base match=substring feat=-0 corte=2.75 | 0.700 | 0.099 | 0.173 | 7 | 3 | 64 | 226 |
| v4 kw=base match=substring feat=-0 corte=3.00 | 0.571 | 0.056 | 0.103 | 4 | 3 | 67 | 226 |
| v4 kw=base match=substring feat=-1 corte=0.25 | 0.309 | 1.000 | 0.472 | 71 | 159 | 0 | 70 |
| v4 kw=base match=substring feat=-1 corte=0.50 | 0.346 | 1.000 | 0.514 | 71 | 134 | 0 | 95 |
| v4 kw=base match=substring feat=-1 corte=0.75 | 0.397 | 1.000 | 0.568 | 71 | 108 | 0 | 121 |
| v4 kw=base match=substring feat=-1 corte=1.00 | 0.423 | 0.972 | 0.590 | 69 | 94 | 2 | 135 |
| v4 kw=base match=substring feat=-1 corte=1.25 | 0.521 | 0.887 | 0.656 | 63 | 58 | 8 | 171 |
| v4 kw=base match=substring feat=-1 corte=1.50 | 0.629 | 0.789 | 0.700 | 56 | 33 | 15 | 196 |
| v4 kw=base match=substring feat=-1 corte=1.75 | 0.710 | 0.620 | 0.662 | 44 | 18 | 27 | 211 |
| v4 kw=base match=substring feat=-1 corte=2.00 | 0.791 | 0.479 | 0.596 | 34 | 9 | 37 | 220 |
| v4 kw=base match=substring feat=-1 corte=2.25 | 0.833 | 0.211 | 0.337 | 15 | 3 | 56 | 226 |
| v4 kw=base match=substring feat=-1 corte=2.50 | 0.769 | 0.141 | 0.238 | 10 | 3 | 61 | 226 |
| v4 kw=base match=substring feat=-1 corte=2.75 | 0.714 | 0.070 | 0.128 | 5 | 2 | 66 | 227 |
| v4 kw=base match=substring feat=-1 corte=3.00 | 0.667 | 0.056 | 0.104 | 4 | 2 | 67 | 227 |
| v4 kw=base match=substring feat=-2 corte=0.25 | 0.343 | 0.972 | 0.507 | 69 | 132 | 2 | 97 |
| v4 kw=base match=substring feat=-2 corte=0.50 | 0.376 | 0.944 | 0.538 | 67 | 111 | 4 | 118 |
| v4 kw=base match=substring feat=-2 corte=0.75 | 0.419 | 0.944 | 0.580 | 67 | 93 | 4 | 136 |
| v4 kw=base match=substring feat=-2 corte=1.00 | 0.432 | 0.901 | 0.584 | 64 | 84 | 7 | 145 |
| v4 kw=base match=substring feat=-2 corte=1.25 | 0.527 | 0.831 | 0.645 | 59 | 53 | 12 | 176 |
| v4 kw=base match=substring feat=-2 corte=1.50 | 0.635 | 0.761 | 0.692 | 54 | 31 | 17 | 198 |
| v4 kw=base match=substring feat=-2 corte=1.75 | 0.712 | 0.592 | 0.646 | 42 | 17 | 29 | 212 |
| v4 kw=base match=substring feat=-2 corte=2.00 | 0.810 | 0.479 | 0.602 | 34 | 8 | 37 | 221 |
| v4 kw=base match=substring feat=-2 corte=2.25 | 0.833 | 0.211 | 0.337 | 15 | 3 | 56 | 226 |
| v4 kw=base match=substring feat=-2 corte=2.50 | 0.769 | 0.141 | 0.238 | 10 | 3 | 61 | 226 |
| v4 kw=base match=substring feat=-2 corte=2.75 | 0.714 | 0.070 | 0.128 | 5 | 2 | 66 | 227 |
| v4 kw=base match=substring feat=-2 corte=3.00 | 0.667 | 0.056 | 0.104 | 4 | 2 | 67 | 227 |
| v4 kw=base match=palavra feat=-0 corte=0.25 | 0.267 | 1.000 | 0.421 | 71 | 195 | 0 | 34 |
| v4 kw=base match=palavra feat=-0 corte=0.50 | 0.297 | 1.000 | 0.458 | 71 | 168 | 0 | 61 |
| v4 kw=base match=palavra feat=-0 corte=0.75 | 0.336 | 1.000 | 0.504 | 71 | 140 | 0 | 89 |
| v4 kw=base match=palavra feat=-0 corte=1.00 | 0.363 | 0.986 | 0.530 | 70 | 123 | 1 | 106 |
| v4 kw=base match=palavra feat=-0 corte=1.25 | 0.433 | 0.915 | 0.588 | 65 | 85 | 6 | 144 |
| v4 kw=base match=palavra feat=-0 corte=1.50 | 0.526 | 0.845 | 0.649 | 60 | 54 | 11 | 175 |
| v4 kw=base match=palavra feat=-0 corte=1.75 | 0.615 | 0.676 | 0.644 | 48 | 30 | 23 | 199 |
| v4 kw=base match=palavra feat=-0 corte=2.00 | 0.696 | 0.549 | 0.614 | 39 | 17 | 32 | 212 |
| v4 kw=base match=palavra feat=-0 corte=2.25 | 0.704 | 0.268 | 0.388 | 19 | 8 | 52 | 221 |
| v4 kw=base match=palavra feat=-0 corte=2.50 | 0.706 | 0.169 | 0.273 | 12 | 5 | 59 | 224 |
| v4 kw=base match=palavra feat=-0 corte=2.75 | 0.700 | 0.099 | 0.173 | 7 | 3 | 64 | 226 |
| v4 kw=base match=palavra feat=-0 corte=3.00 | 0.571 | 0.056 | 0.103 | 4 | 3 | 67 | 226 |
| v4 kw=base match=palavra feat=-1 corte=0.25 | 0.309 | 1.000 | 0.472 | 71 | 159 | 0 | 70 |
| v4 kw=base match=palavra feat=-1 corte=0.50 | 0.346 | 1.000 | 0.514 | 71 | 134 | 0 | 95 |
| v4 kw=base match=palavra feat=-1 corte=0.75 | 0.399 | 1.000 | 0.570 | 71 | 107 | 0 | 122 |
| v4 kw=base match=palavra feat=-1 corte=1.00 | 0.423 | 0.972 | 0.590 | 69 | 94 | 2 | 135 |
| v4 kw=base match=palavra feat=-1 corte=1.25 | 0.521 | 0.887 | 0.656 | 63 | 58 | 8 | 171 |
| v4 kw=base match=palavra feat=-1 corte=1.50 | 0.644 | 0.789 | 0.709 | 56 | 31 | 15 | 198 |
| v4 kw=base match=palavra feat=-1 corte=1.75 | 0.733 | 0.620 | 0.672 | 44 | 16 | 27 | 213 |
| v4 kw=base match=palavra feat=-1 corte=2.00 | 0.829 | 0.479 | 0.607 | 34 | 7 | 37 | 222 |
| v4 kw=base match=palavra feat=-1 corte=2.25 | 0.833 | 0.211 | 0.337 | 15 | 3 | 56 | 226 |
| v4 kw=base match=palavra feat=-1 corte=2.50 | 0.769 | 0.141 | 0.238 | 10 | 3 | 61 | 226 |
| v4 kw=base match=palavra feat=-1 corte=2.75 | 0.714 | 0.070 | 0.128 | 5 | 2 | 66 | 227 |
| v4 kw=base match=palavra feat=-1 corte=3.00 | 0.667 | 0.056 | 0.104 | 4 | 2 | 67 | 227 |
| v4 kw=base match=palavra feat=-2 corte=0.25 | 0.343 | 0.972 | 0.507 | 69 | 132 | 2 | 97 |
| v4 kw=base match=palavra feat=-2 corte=0.50 | 0.376 | 0.944 | 0.538 | 67 | 111 | 4 | 118 |
| v4 kw=base match=palavra feat=-2 corte=0.75 | 0.419 | 0.944 | 0.580 | 67 | 93 | 4 | 136 |
| v4 kw=base match=palavra feat=-2 corte=1.00 | 0.432 | 0.901 | 0.584 | 64 | 84 | 7 | 145 |
| v4 kw=base match=palavra feat=-2 corte=1.25 | 0.527 | 0.831 | 0.645 | 59 | 53 | 12 | 176 |
| v4 kw=base match=palavra feat=-2 corte=1.50 | 0.651 | 0.761 | 0.701 | 54 | 29 | 17 | 200 |
| v4 kw=base match=palavra feat=-2 corte=1.75 | 0.737 | 0.592 | 0.656 | 42 | 15 | 29 | 214 |
| v4 kw=base match=palavra feat=-2 corte=2.00 | 0.850 | 0.479 | 0.613 | 34 | 6 | 37 | 223 |
| v4 kw=base match=palavra feat=-2 corte=2.25 | 0.833 | 0.211 | 0.337 | 15 | 3 | 56 | 226 |
| v4 kw=base match=palavra feat=-2 corte=2.50 | 0.769 | 0.141 | 0.238 | 10 | 3 | 61 | 226 |
| v4 kw=base match=palavra feat=-2 corte=2.75 | 0.714 | 0.070 | 0.128 | 5 | 2 | 66 | 227 |
| v4 kw=base match=palavra feat=-2 corte=3.00 | 0.667 | 0.056 | 0.104 | 4 | 2 | 67 | 227 |
| v4 kw=ampliado match=substring feat=-0 corte=0.25 | 0.264 | 1.000 | 0.418 | 71 | 198 | 0 | 31 |
| v4 kw=ampliado match=substring feat=-0 corte=0.50 | 0.287 | 1.000 | 0.447 | 71 | 176 | 0 | 53 |
| v4 kw=ampliado match=substring feat=-0 corte=0.75 | 0.327 | 1.000 | 0.493 | 71 | 146 | 0 | 83 |
| v4 kw=ampliado match=substring feat=-0 corte=1.00 | 0.352 | 0.986 | 0.519 | 70 | 129 | 1 | 100 |
| v4 kw=ampliado match=substring feat=-0 corte=1.25 | 0.419 | 0.915 | 0.575 | 65 | 90 | 6 | 139 |
| v4 kw=ampliado match=substring feat=-0 corte=1.50 | 0.500 | 0.859 | 0.632 | 61 | 61 | 10 | 168 |
| v4 kw=ampliado match=substring feat=-0 corte=1.75 | 0.556 | 0.704 | 0.621 | 50 | 40 | 21 | 189 |
| v4 kw=ampliado match=substring feat=-0 corte=2.00 | 0.646 | 0.592 | 0.618 | 42 | 23 | 29 | 206 |
| v4 kw=ampliado match=substring feat=-0 corte=2.25 | 0.677 | 0.296 | 0.412 | 21 | 10 | 50 | 219 |
| v4 kw=ampliado match=substring feat=-0 corte=2.50 | 0.684 | 0.183 | 0.289 | 13 | 6 | 58 | 223 |
| v4 kw=ampliado match=substring feat=-0 corte=2.75 | 0.667 | 0.113 | 0.193 | 8 | 4 | 63 | 225 |
| v4 kw=ampliado match=substring feat=-0 corte=3.00 | 0.556 | 0.070 | 0.125 | 5 | 4 | 66 | 225 |
| v4 kw=ampliado match=substring feat=-1 corte=0.25 | 0.306 | 1.000 | 0.469 | 71 | 161 | 0 | 68 |
| v4 kw=ampliado match=substring feat=-1 corte=0.50 | 0.340 | 1.000 | 0.507 | 71 | 138 | 0 | 91 |
| v4 kw=ampliado match=substring feat=-1 corte=0.75 | 0.384 | 1.000 | 0.555 | 71 | 114 | 0 | 115 |
| v4 kw=ampliado match=substring feat=-1 corte=1.00 | 0.419 | 0.986 | 0.588 | 70 | 97 | 1 | 132 |
| v4 kw=ampliado match=substring feat=-1 corte=1.25 | 0.496 | 0.887 | 0.636 | 63 | 64 | 8 | 165 |
| v4 kw=ampliado match=substring feat=-1 corte=1.50 | 0.600 | 0.803 | 0.687 | 57 | 38 | 14 | 191 |
| v4 kw=ampliado match=substring feat=-1 corte=1.75 | 0.667 | 0.648 | 0.657 | 46 | 23 | 25 | 206 |
| v4 kw=ampliado match=substring feat=-1 corte=2.00 | 0.735 | 0.507 | 0.600 | 36 | 13 | 35 | 216 |
| v4 kw=ampliado match=substring feat=-1 corte=2.25 | 0.850 | 0.239 | 0.374 | 17 | 3 | 54 | 226 |
| v4 kw=ampliado match=substring feat=-1 corte=2.50 | 0.786 | 0.155 | 0.259 | 11 | 3 | 60 | 226 |
| v4 kw=ampliado match=substring feat=-1 corte=2.75 | 0.750 | 0.085 | 0.152 | 6 | 2 | 65 | 227 |
| v4 kw=ampliado match=substring feat=-1 corte=3.00 | 0.714 | 0.070 | 0.128 | 5 | 2 | 66 | 227 |
| v4 kw=ampliado match=substring feat=-2 corte=0.25 | 0.338 | 0.972 | 0.502 | 69 | 135 | 2 | 94 |
| v4 kw=ampliado match=substring feat=-2 corte=0.50 | 0.368 | 0.944 | 0.530 | 67 | 115 | 4 | 114 |
| v4 kw=ampliado match=substring feat=-2 corte=0.75 | 0.409 | 0.944 | 0.570 | 67 | 97 | 4 | 132 |
| v4 kw=ampliado match=substring feat=-2 corte=1.00 | 0.424 | 0.901 | 0.577 | 64 | 87 | 7 | 142 |
| v4 kw=ampliado match=substring feat=-2 corte=1.25 | 0.509 | 0.831 | 0.631 | 59 | 57 | 12 | 172 |
| v4 kw=ampliado match=substring feat=-2 corte=1.50 | 0.611 | 0.775 | 0.683 | 55 | 35 | 16 | 194 |
| v4 kw=ampliado match=substring feat=-2 corte=1.75 | 0.677 | 0.620 | 0.647 | 44 | 21 | 27 | 208 |
| v4 kw=ampliado match=substring feat=-2 corte=2.00 | 0.766 | 0.507 | 0.610 | 36 | 11 | 35 | 218 |
| v4 kw=ampliado match=substring feat=-2 corte=2.25 | 0.850 | 0.239 | 0.374 | 17 | 3 | 54 | 226 |
| v4 kw=ampliado match=substring feat=-2 corte=2.50 | 0.786 | 0.155 | 0.259 | 11 | 3 | 60 | 226 |
| v4 kw=ampliado match=substring feat=-2 corte=2.75 | 0.750 | 0.085 | 0.152 | 6 | 2 | 65 | 227 |
| v4 kw=ampliado match=substring feat=-2 corte=3.00 | 0.714 | 0.070 | 0.128 | 5 | 2 | 66 | 227 |
| v4 kw=ampliado match=palavra feat=-0 corte=0.25 | 0.264 | 1.000 | 0.418 | 71 | 198 | 0 | 31 |
| v4 kw=ampliado match=palavra feat=-0 corte=0.50 | 0.287 | 1.000 | 0.447 | 71 | 176 | 0 | 53 |
| v4 kw=ampliado match=palavra feat=-0 corte=0.75 | 0.332 | 1.000 | 0.498 | 71 | 143 | 0 | 86 |
| v4 kw=ampliado match=palavra feat=-0 corte=1.00 | 0.357 | 0.986 | 0.524 | 70 | 126 | 1 | 103 |
| v4 kw=ampliado match=palavra feat=-0 corte=1.25 | 0.419 | 0.915 | 0.575 | 65 | 90 | 6 | 139 |
| v4 kw=ampliado match=palavra feat=-0 corte=1.50 | 0.500 | 0.845 | 0.628 | 60 | 60 | 11 | 169 |
| v4 kw=ampliado match=palavra feat=-0 corte=1.75 | 0.563 | 0.690 | 0.620 | 49 | 38 | 22 | 191 |
| v4 kw=ampliado match=palavra feat=-0 corte=2.00 | 0.672 | 0.577 | 0.621 | 41 | 20 | 30 | 209 |
| v4 kw=ampliado match=palavra feat=-0 corte=2.25 | 0.700 | 0.296 | 0.416 | 21 | 9 | 50 | 220 |
| v4 kw=ampliado match=palavra feat=-0 corte=2.50 | 0.684 | 0.183 | 0.289 | 13 | 6 | 58 | 223 |
| v4 kw=ampliado match=palavra feat=-0 corte=2.75 | 0.667 | 0.113 | 0.193 | 8 | 4 | 63 | 225 |
| v4 kw=ampliado match=palavra feat=-0 corte=3.00 | 0.556 | 0.070 | 0.125 | 5 | 4 | 66 | 225 |
| v4 kw=ampliado match=palavra feat=-1 corte=0.25 | 0.306 | 1.000 | 0.469 | 71 | 161 | 0 | 68 |
| v4 kw=ampliado match=palavra feat=-1 corte=0.50 | 0.340 | 1.000 | 0.507 | 71 | 138 | 0 | 91 |
| v4 kw=ampliado match=palavra feat=-1 corte=0.75 | 0.388 | 1.000 | 0.559 | 71 | 112 | 0 | 117 |
| v4 kw=ampliado match=palavra feat=-1 corte=1.00 | 0.418 | 0.972 | 0.585 | 69 | 96 | 2 | 133 |
| v4 kw=ampliado match=palavra feat=-1 corte=1.25 | 0.500 | 0.887 | 0.640 | 63 | 63 | 8 | 166 |
| v4 kw=ampliado match=palavra feat=-1 corte=1.50 | 0.602 | 0.789 | 0.683 | 56 | 37 | 15 | 192 |
| v4 kw=ampliado match=palavra feat=-1 corte=1.75 | 0.672 | 0.634 | 0.652 | 45 | 22 | 26 | 207 |
| v4 kw=ampliado match=palavra feat=-1 corte=2.00 | 0.766 | 0.507 | 0.610 | 36 | 11 | 35 | 218 |
| v4 kw=ampliado match=palavra feat=-1 corte=2.25 | 0.850 | 0.239 | 0.374 | 17 | 3 | 54 | 226 |
| v4 kw=ampliado match=palavra feat=-1 corte=2.50 | 0.786 | 0.155 | 0.259 | 11 | 3 | 60 | 226 |
| v4 kw=ampliado match=palavra feat=-1 corte=2.75 | 0.750 | 0.085 | 0.152 | 6 | 2 | 65 | 227 |
| v4 kw=ampliado match=palavra feat=-1 corte=3.00 | 0.714 | 0.070 | 0.128 | 5 | 2 | 66 | 227 |
| v4 kw=ampliado match=palavra feat=-2 corte=0.25 | 0.340 | 0.972 | 0.504 | 69 | 134 | 2 | 95 |
| v4 kw=ampliado match=palavra feat=-2 corte=0.50 | 0.368 | 0.944 | 0.530 | 67 | 115 | 4 | 114 |
| v4 kw=ampliado match=palavra feat=-2 corte=0.75 | 0.411 | 0.944 | 0.573 | 67 | 96 | 4 | 133 |
| v4 kw=ampliado match=palavra feat=-2 corte=1.00 | 0.424 | 0.901 | 0.577 | 64 | 87 | 7 | 142 |
| v4 kw=ampliado match=palavra feat=-2 corte=1.25 | 0.509 | 0.831 | 0.631 | 59 | 57 | 12 | 172 |
| v4 kw=ampliado match=palavra feat=-2 corte=1.50 | 0.614 | 0.761 | 0.679 | 54 | 34 | 17 | 195 |
| v4 kw=ampliado match=palavra feat=-2 corte=1.75 | 0.683 | 0.606 | 0.642 | 43 | 20 | 28 | 209 |
| v4 kw=ampliado match=palavra feat=-2 corte=2.00 | 0.800 | 0.507 | 0.621 | 36 | 9 | 35 | 220 |
| v4 kw=ampliado match=palavra feat=-2 corte=2.25 | 0.850 | 0.239 | 0.374 | 17 | 3 | 54 | 226 |
| v4 kw=ampliado match=palavra feat=-2 corte=2.50 | 0.786 | 0.155 | 0.259 | 11 | 3 | 60 | 226 |
| v4 kw=ampliado match=palavra feat=-2 corte=2.75 | 0.750 | 0.085 | 0.152 | 6 | 2 | 65 | 227 |
| v4 kw=ampliado match=palavra feat=-2 corte=3.00 | 0.714 | 0.070 | 0.128 | 5 | 2 | 66 | 227 |
<!-- tuning:end -->
