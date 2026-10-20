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
## Execução de 2026-10-20T16:50:23+00:00

Gerado por `scripts/tune_cfr.py`; o texto entre os marcadores é reescrito a cada execução.

- Itens (releases com consenso): 300 (146 corretivas)
- Com commits coletados: 188; com release anterior: 294
- Palavras-chave: `base` = fix, revert, hotfix; `ampliado` = fix, revert, hotfix, bug, patch, regression, crash
- **Melhor: v2 kw=base match=palavra** — precisão 0.730, recall 1.000, F1 0.844 (atinge a meta de 0.70)
- F1 fora da amostra (5-fold por repositório, 20 repetições): média 0.837 (mín. 0.801, máx. 0.844)

### Melhor combinação de cada versão

| Versão | Combinação | F1 |
|---|---|---:|
| v1 | v1 | 0.644 |
| v2 | v2 kw=base match=palavra | 0.844 |
| v3 | v3 kw=ampliado match=palavra corte=0.25 | 0.831 |
| v4 | v4 kw=ampliado match=substring feat=-0 corte=1.25 | 0.798 |

### Todas as combinações

| Combinação | Precisão | Recall | F1 | TP | FP | FN | TN |
|---|---:|---:|---:|---:|---:|---:|---:|
| v1 | 0.638 | 0.651 | 0.644 | 95 | 54 | 51 | 100 |
| v2 kw=base match=substring | 0.723 | 1.000 | 0.839 | 146 | 56 | 0 | 98 |
| v2 kw=base match=palavra | 0.730 | 1.000 | 0.844 | 146 | 54 | 0 | 100 |
| v2 kw=ampliado match=substring | 0.719 | 1.000 | 0.837 | 146 | 57 | 0 | 97 |
| v2 kw=ampliado match=palavra | 0.723 | 1.000 | 0.839 | 146 | 56 | 0 | 98 |
| v3 kw=base match=substring corte=0.25 | 0.721 | 0.973 | 0.828 | 142 | 55 | 4 | 99 |
| v3 kw=base match=substring corte=0.50 | 0.703 | 0.877 | 0.780 | 128 | 54 | 18 | 100 |
| v3 kw=base match=substring corte=0.75 | 0.679 | 0.781 | 0.726 | 114 | 54 | 32 | 100 |
| v3 kw=base match=substring corte=1.00 | 0.660 | 0.719 | 0.689 | 105 | 54 | 41 | 100 |
| v3 kw=base match=substring corte=1.25 | 1.000 | 0.582 | 0.736 | 85 | 0 | 61 | 154 |
| v3 kw=base match=substring corte=1.50 | 1.000 | 0.514 | 0.679 | 75 | 0 | 71 | 154 |
| v3 kw=base match=substring corte=1.75 | 1.000 | 0.363 | 0.533 | 53 | 0 | 93 | 154 |
| v3 kw=base match=substring corte=2.00 | 1.000 | 0.260 | 0.413 | 38 | 0 | 108 | 154 |
| v3 kw=base match=substring corte=2.25 | 1.000 | 0.158 | 0.272 | 23 | 0 | 123 | 154 |
| v3 kw=base match=substring corte=2.50 | 1.000 | 0.144 | 0.251 | 21 | 0 | 125 | 154 |
| v3 kw=base match=substring corte=2.75 | 1.000 | 0.103 | 0.186 | 15 | 0 | 131 | 154 |
| v3 kw=base match=substring corte=3.00 | 1.000 | 0.089 | 0.164 | 13 | 0 | 133 | 154 |
| v3 kw=base match=palavra corte=0.25 | 0.724 | 0.973 | 0.830 | 142 | 54 | 4 | 100 |
| v3 kw=base match=palavra corte=0.50 | 0.703 | 0.877 | 0.780 | 128 | 54 | 18 | 100 |
| v3 kw=base match=palavra corte=0.75 | 0.677 | 0.774 | 0.722 | 113 | 54 | 33 | 100 |
| v3 kw=base match=palavra corte=1.00 | 0.656 | 0.705 | 0.680 | 103 | 54 | 43 | 100 |
| v3 kw=base match=palavra corte=1.25 | 1.000 | 0.575 | 0.730 | 84 | 0 | 62 | 154 |
| v3 kw=base match=palavra corte=1.50 | 1.000 | 0.507 | 0.673 | 74 | 0 | 72 | 154 |
| v3 kw=base match=palavra corte=1.75 | 1.000 | 0.349 | 0.518 | 51 | 0 | 95 | 154 |
| v3 kw=base match=palavra corte=2.00 | 1.000 | 0.247 | 0.396 | 36 | 0 | 110 | 154 |
| v3 kw=base match=palavra corte=2.25 | 1.000 | 0.151 | 0.262 | 22 | 0 | 124 | 154 |
| v3 kw=base match=palavra corte=2.50 | 1.000 | 0.137 | 0.241 | 20 | 0 | 126 | 154 |
| v3 kw=base match=palavra corte=2.75 | 1.000 | 0.103 | 0.186 | 15 | 0 | 131 | 154 |
| v3 kw=base match=palavra corte=3.00 | 1.000 | 0.089 | 0.164 | 13 | 0 | 133 | 154 |
| v3 kw=ampliado match=substring corte=0.25 | 0.719 | 0.979 | 0.829 | 143 | 56 | 3 | 98 |
| v3 kw=ampliado match=substring corte=0.50 | 0.704 | 0.897 | 0.789 | 131 | 55 | 15 | 99 |
| v3 kw=ampliado match=substring corte=0.75 | 0.680 | 0.788 | 0.730 | 115 | 54 | 31 | 100 |
| v3 kw=ampliado match=substring corte=1.00 | 0.665 | 0.733 | 0.697 | 107 | 54 | 39 | 100 |
| v3 kw=ampliado match=substring corte=1.25 | 1.000 | 0.603 | 0.752 | 88 | 0 | 58 | 154 |
| v3 kw=ampliado match=substring corte=1.50 | 1.000 | 0.534 | 0.696 | 78 | 0 | 68 | 154 |
| v3 kw=ampliado match=substring corte=1.75 | 1.000 | 0.384 | 0.554 | 56 | 0 | 90 | 154 |
| v3 kw=ampliado match=substring corte=2.00 | 1.000 | 0.288 | 0.447 | 42 | 0 | 104 | 154 |
| v3 kw=ampliado match=substring corte=2.25 | 1.000 | 0.164 | 0.282 | 24 | 0 | 122 | 154 |
| v3 kw=ampliado match=substring corte=2.50 | 1.000 | 0.151 | 0.262 | 22 | 0 | 124 | 154 |
| v3 kw=ampliado match=substring corte=2.75 | 1.000 | 0.103 | 0.186 | 15 | 0 | 131 | 154 |
| v3 kw=ampliado match=substring corte=3.00 | 1.000 | 0.089 | 0.164 | 13 | 0 | 133 | 154 |
| v3 kw=ampliado match=palavra corte=0.25 | 0.722 | 0.979 | 0.831 | 143 | 55 | 3 | 99 |
| v3 kw=ampliado match=palavra corte=0.50 | 0.707 | 0.890 | 0.788 | 130 | 54 | 16 | 100 |
| v3 kw=ampliado match=palavra corte=0.75 | 0.680 | 0.788 | 0.730 | 115 | 54 | 31 | 100 |
| v3 kw=ampliado match=palavra corte=1.00 | 0.662 | 0.726 | 0.693 | 106 | 54 | 40 | 100 |
| v3 kw=ampliado match=palavra corte=1.25 | 1.000 | 0.596 | 0.747 | 87 | 0 | 59 | 154 |
| v3 kw=ampliado match=palavra corte=1.50 | 1.000 | 0.527 | 0.691 | 77 | 0 | 69 | 154 |
| v3 kw=ampliado match=palavra corte=1.75 | 1.000 | 0.377 | 0.547 | 55 | 0 | 91 | 154 |
| v3 kw=ampliado match=palavra corte=2.00 | 1.000 | 0.267 | 0.422 | 39 | 0 | 107 | 154 |
| v3 kw=ampliado match=palavra corte=2.25 | 1.000 | 0.151 | 0.262 | 22 | 0 | 124 | 154 |
| v3 kw=ampliado match=palavra corte=2.50 | 1.000 | 0.144 | 0.251 | 21 | 0 | 125 | 154 |
| v3 kw=ampliado match=palavra corte=2.75 | 1.000 | 0.103 | 0.186 | 15 | 0 | 131 | 154 |
| v3 kw=ampliado match=palavra corte=3.00 | 1.000 | 0.089 | 0.164 | 13 | 0 | 133 | 154 |
| v4 kw=base match=substring feat=-0 corte=0.25 | 0.637 | 0.973 | 0.770 | 142 | 81 | 4 | 73 |
| v4 kw=base match=substring feat=-0 corte=0.50 | 0.617 | 0.884 | 0.727 | 129 | 80 | 17 | 74 |
| v4 kw=base match=substring feat=-0 corte=0.75 | 0.600 | 0.822 | 0.694 | 120 | 80 | 26 | 74 |
| v4 kw=base match=substring feat=-0 corte=1.00 | 0.588 | 0.781 | 0.671 | 114 | 80 | 32 | 74 |
| v4 kw=base match=substring feat=-0 corte=1.25 | 1.000 | 0.651 | 0.788 | 95 | 0 | 51 | 154 |
| v4 kw=base match=substring feat=-0 corte=1.50 | 1.000 | 0.575 | 0.730 | 84 | 0 | 62 | 154 |
| v4 kw=base match=substring feat=-0 corte=1.75 | 1.000 | 0.390 | 0.562 | 57 | 0 | 89 | 154 |
| v4 kw=base match=substring feat=-0 corte=2.00 | 1.000 | 0.267 | 0.422 | 39 | 0 | 107 | 154 |
| v4 kw=base match=substring feat=-0 corte=2.25 | 1.000 | 0.158 | 0.272 | 23 | 0 | 123 | 154 |
| v4 kw=base match=substring feat=-0 corte=2.50 | 1.000 | 0.144 | 0.251 | 21 | 0 | 125 | 154 |
| v4 kw=base match=substring feat=-0 corte=2.75 | 1.000 | 0.103 | 0.186 | 15 | 0 | 131 | 154 |
| v4 kw=base match=substring feat=-0 corte=3.00 | 1.000 | 0.089 | 0.164 | 13 | 0 | 133 | 154 |
| v4 kw=base match=substring feat=-1 corte=0.25 | 0.621 | 0.863 | 0.722 | 126 | 77 | 20 | 77 |
| v4 kw=base match=substring feat=-1 corte=0.50 | 0.606 | 0.801 | 0.690 | 117 | 76 | 29 | 78 |
| v4 kw=base match=substring feat=-1 corte=0.75 | 0.563 | 0.671 | 0.613 | 98 | 76 | 48 | 78 |
| v4 kw=base match=substring feat=-1 corte=1.00 | 0.537 | 0.603 | 0.568 | 88 | 76 | 58 | 78 |
| v4 kw=base match=substring feat=-1 corte=1.25 | 1.000 | 0.479 | 0.648 | 70 | 0 | 76 | 154 |
| v4 kw=base match=substring feat=-1 corte=1.50 | 1.000 | 0.418 | 0.589 | 61 | 0 | 85 | 154 |
| v4 kw=base match=substring feat=-1 corte=1.75 | 1.000 | 0.308 | 0.471 | 45 | 0 | 101 | 154 |
| v4 kw=base match=substring feat=-1 corte=2.00 | 1.000 | 0.240 | 0.387 | 35 | 0 | 111 | 154 |
| v4 kw=base match=substring feat=-1 corte=2.25 | 1.000 | 0.151 | 0.262 | 22 | 0 | 124 | 154 |
| v4 kw=base match=substring feat=-1 corte=2.50 | 1.000 | 0.144 | 0.251 | 21 | 0 | 125 | 154 |
| v4 kw=base match=substring feat=-1 corte=2.75 | 1.000 | 0.103 | 0.186 | 15 | 0 | 131 | 154 |
| v4 kw=base match=substring feat=-1 corte=3.00 | 1.000 | 0.089 | 0.164 | 13 | 0 | 133 | 154 |
| v4 kw=base match=substring feat=-2 corte=0.25 | 0.567 | 0.692 | 0.623 | 101 | 77 | 45 | 77 |
| v4 kw=base match=substring feat=-2 corte=0.50 | 0.553 | 0.644 | 0.595 | 94 | 76 | 52 | 78 |
| v4 kw=base match=substring feat=-2 corte=0.75 | 0.531 | 0.589 | 0.558 | 86 | 76 | 60 | 78 |
| v4 kw=base match=substring feat=-2 corte=1.00 | 0.525 | 0.575 | 0.549 | 84 | 76 | 62 | 78 |
| v4 kw=base match=substring feat=-2 corte=1.25 | 1.000 | 0.473 | 0.642 | 69 | 0 | 77 | 154 |
| v4 kw=base match=substring feat=-2 corte=1.50 | 1.000 | 0.418 | 0.589 | 61 | 0 | 85 | 154 |
| v4 kw=base match=substring feat=-2 corte=1.75 | 1.000 | 0.308 | 0.471 | 45 | 0 | 101 | 154 |
| v4 kw=base match=substring feat=-2 corte=2.00 | 1.000 | 0.240 | 0.387 | 35 | 0 | 111 | 154 |
| v4 kw=base match=substring feat=-2 corte=2.25 | 1.000 | 0.151 | 0.262 | 22 | 0 | 124 | 154 |
| v4 kw=base match=substring feat=-2 corte=2.50 | 1.000 | 0.144 | 0.251 | 21 | 0 | 125 | 154 |
| v4 kw=base match=substring feat=-2 corte=2.75 | 1.000 | 0.103 | 0.186 | 15 | 0 | 131 | 154 |
| v4 kw=base match=substring feat=-2 corte=3.00 | 1.000 | 0.089 | 0.164 | 13 | 0 | 133 | 154 |
| v4 kw=base match=palavra feat=-0 corte=0.25 | 0.640 | 0.973 | 0.772 | 142 | 80 | 4 | 74 |
| v4 kw=base match=palavra feat=-0 corte=0.50 | 0.617 | 0.884 | 0.727 | 129 | 80 | 17 | 74 |
| v4 kw=base match=palavra feat=-0 corte=0.75 | 0.598 | 0.815 | 0.690 | 119 | 80 | 27 | 74 |
| v4 kw=base match=palavra feat=-0 corte=1.00 | 0.583 | 0.767 | 0.663 | 112 | 80 | 34 | 74 |
| v4 kw=base match=palavra feat=-0 corte=1.25 | 1.000 | 0.644 | 0.783 | 94 | 0 | 52 | 154 |
| v4 kw=base match=palavra feat=-0 corte=1.50 | 1.000 | 0.568 | 0.725 | 83 | 0 | 63 | 154 |
| v4 kw=base match=palavra feat=-0 corte=1.75 | 1.000 | 0.377 | 0.547 | 55 | 0 | 91 | 154 |
| v4 kw=base match=palavra feat=-0 corte=2.00 | 1.000 | 0.253 | 0.404 | 37 | 0 | 109 | 154 |
| v4 kw=base match=palavra feat=-0 corte=2.25 | 1.000 | 0.151 | 0.262 | 22 | 0 | 124 | 154 |
| v4 kw=base match=palavra feat=-0 corte=2.50 | 1.000 | 0.137 | 0.241 | 20 | 0 | 126 | 154 |
| v4 kw=base match=palavra feat=-0 corte=2.75 | 1.000 | 0.103 | 0.186 | 15 | 0 | 131 | 154 |
| v4 kw=base match=palavra feat=-0 corte=3.00 | 1.000 | 0.089 | 0.164 | 13 | 0 | 133 | 154 |
| v4 kw=base match=palavra feat=-1 corte=0.25 | 0.622 | 0.856 | 0.720 | 125 | 76 | 21 | 78 |
| v4 kw=base match=palavra feat=-1 corte=0.50 | 0.606 | 0.801 | 0.690 | 117 | 76 | 29 | 78 |
| v4 kw=base match=palavra feat=-1 corte=0.75 | 0.561 | 0.664 | 0.608 | 97 | 76 | 49 | 78 |
| v4 kw=base match=palavra feat=-1 corte=1.00 | 0.534 | 0.596 | 0.563 | 87 | 76 | 59 | 78 |
| v4 kw=base match=palavra feat=-1 corte=1.25 | 1.000 | 0.479 | 0.648 | 70 | 0 | 76 | 154 |
| v4 kw=base match=palavra feat=-1 corte=1.50 | 1.000 | 0.411 | 0.583 | 60 | 0 | 86 | 154 |
| v4 kw=base match=palavra feat=-1 corte=1.75 | 1.000 | 0.295 | 0.455 | 43 | 0 | 103 | 154 |
| v4 kw=base match=palavra feat=-1 corte=2.00 | 1.000 | 0.226 | 0.369 | 33 | 0 | 113 | 154 |
| v4 kw=base match=palavra feat=-1 corte=2.25 | 1.000 | 0.144 | 0.251 | 21 | 0 | 125 | 154 |
| v4 kw=base match=palavra feat=-1 corte=2.50 | 1.000 | 0.137 | 0.241 | 20 | 0 | 126 | 154 |
| v4 kw=base match=palavra feat=-1 corte=2.75 | 1.000 | 0.103 | 0.186 | 15 | 0 | 131 | 154 |
| v4 kw=base match=palavra feat=-1 corte=3.00 | 1.000 | 0.089 | 0.164 | 13 | 0 | 133 | 154 |
| v4 kw=base match=palavra feat=-2 corte=0.25 | 0.571 | 0.692 | 0.625 | 101 | 76 | 45 | 78 |
| v4 kw=base match=palavra feat=-2 corte=0.50 | 0.553 | 0.644 | 0.595 | 94 | 76 | 52 | 78 |
| v4 kw=base match=palavra feat=-2 corte=0.75 | 0.528 | 0.582 | 0.554 | 85 | 76 | 61 | 78 |
| v4 kw=base match=palavra feat=-2 corte=1.00 | 0.522 | 0.568 | 0.544 | 83 | 76 | 63 | 78 |
| v4 kw=base match=palavra feat=-2 corte=1.25 | 1.000 | 0.473 | 0.642 | 69 | 0 | 77 | 154 |
| v4 kw=base match=palavra feat=-2 corte=1.50 | 1.000 | 0.411 | 0.583 | 60 | 0 | 86 | 154 |
| v4 kw=base match=palavra feat=-2 corte=1.75 | 1.000 | 0.295 | 0.455 | 43 | 0 | 103 | 154 |
| v4 kw=base match=palavra feat=-2 corte=2.00 | 1.000 | 0.226 | 0.369 | 33 | 0 | 113 | 154 |
| v4 kw=base match=palavra feat=-2 corte=2.25 | 1.000 | 0.144 | 0.251 | 21 | 0 | 125 | 154 |
| v4 kw=base match=palavra feat=-2 corte=2.50 | 1.000 | 0.137 | 0.241 | 20 | 0 | 126 | 154 |
| v4 kw=base match=palavra feat=-2 corte=2.75 | 1.000 | 0.103 | 0.186 | 15 | 0 | 131 | 154 |
| v4 kw=base match=palavra feat=-2 corte=3.00 | 1.000 | 0.089 | 0.164 | 13 | 0 | 133 | 154 |
| v4 kw=ampliado match=substring feat=-0 corte=0.25 | 0.636 | 0.979 | 0.771 | 143 | 82 | 3 | 72 |
| v4 kw=ampliado match=substring feat=-0 corte=0.50 | 0.620 | 0.904 | 0.735 | 132 | 81 | 14 | 73 |
| v4 kw=ampliado match=substring feat=-0 corte=0.75 | 0.602 | 0.829 | 0.697 | 121 | 80 | 25 | 74 |
| v4 kw=ampliado match=substring feat=-0 corte=1.00 | 0.588 | 0.781 | 0.671 | 114 | 80 | 32 | 74 |
| v4 kw=ampliado match=substring feat=-0 corte=1.25 | 1.000 | 0.664 | 0.798 | 97 | 0 | 49 | 154 |
| v4 kw=ampliado match=substring feat=-0 corte=1.50 | 1.000 | 0.589 | 0.741 | 86 | 0 | 60 | 154 |
| v4 kw=ampliado match=substring feat=-0 corte=1.75 | 1.000 | 0.411 | 0.583 | 60 | 0 | 86 | 154 |
| v4 kw=ampliado match=substring feat=-0 corte=2.00 | 1.000 | 0.308 | 0.471 | 45 | 0 | 101 | 154 |
| v4 kw=ampliado match=substring feat=-0 corte=2.25 | 1.000 | 0.171 | 0.292 | 25 | 0 | 121 | 154 |
| v4 kw=ampliado match=substring feat=-0 corte=2.50 | 1.000 | 0.158 | 0.272 | 23 | 0 | 123 | 154 |
| v4 kw=ampliado match=substring feat=-0 corte=2.75 | 1.000 | 0.103 | 0.186 | 15 | 0 | 131 | 154 |
| v4 kw=ampliado match=substring feat=-0 corte=3.00 | 1.000 | 0.089 | 0.164 | 13 | 0 | 133 | 154 |
| v4 kw=ampliado match=substring feat=-1 corte=0.25 | 0.623 | 0.870 | 0.726 | 127 | 77 | 19 | 77 |
| v4 kw=ampliado match=substring feat=-1 corte=0.50 | 0.606 | 0.801 | 0.690 | 117 | 76 | 29 | 78 |
| v4 kw=ampliado match=substring feat=-1 corte=0.75 | 0.566 | 0.678 | 0.617 | 99 | 76 | 47 | 78 |
| v4 kw=ampliado match=substring feat=-1 corte=1.00 | 0.539 | 0.610 | 0.572 | 89 | 76 | 57 | 78 |
| v4 kw=ampliado match=substring feat=-1 corte=1.25 | 1.000 | 0.486 | 0.654 | 71 | 0 | 75 | 154 |
| v4 kw=ampliado match=substring feat=-1 corte=1.50 | 1.000 | 0.432 | 0.603 | 63 | 0 | 83 | 154 |
| v4 kw=ampliado match=substring feat=-1 corte=1.75 | 1.000 | 0.322 | 0.487 | 47 | 0 | 99 | 154 |
| v4 kw=ampliado match=substring feat=-1 corte=2.00 | 1.000 | 0.274 | 0.430 | 40 | 0 | 106 | 154 |
| v4 kw=ampliado match=substring feat=-1 corte=2.25 | 1.000 | 0.164 | 0.282 | 24 | 0 | 122 | 154 |
| v4 kw=ampliado match=substring feat=-1 corte=2.50 | 1.000 | 0.158 | 0.272 | 23 | 0 | 123 | 154 |
| v4 kw=ampliado match=substring feat=-1 corte=2.75 | 1.000 | 0.103 | 0.186 | 15 | 0 | 131 | 154 |
| v4 kw=ampliado match=substring feat=-1 corte=3.00 | 1.000 | 0.089 | 0.164 | 13 | 0 | 133 | 154 |
| v4 kw=ampliado match=substring feat=-2 corte=0.25 | 0.567 | 0.692 | 0.623 | 101 | 77 | 45 | 77 |
| v4 kw=ampliado match=substring feat=-2 corte=0.50 | 0.553 | 0.644 | 0.595 | 94 | 76 | 52 | 78 |
| v4 kw=ampliado match=substring feat=-2 corte=0.75 | 0.531 | 0.589 | 0.558 | 86 | 76 | 60 | 78 |
| v4 kw=ampliado match=substring feat=-2 corte=1.00 | 0.525 | 0.575 | 0.549 | 84 | 76 | 62 | 78 |
| v4 kw=ampliado match=substring feat=-2 corte=1.25 | 1.000 | 0.479 | 0.648 | 70 | 0 | 76 | 154 |
| v4 kw=ampliado match=substring feat=-2 corte=1.50 | 1.000 | 0.432 | 0.603 | 63 | 0 | 83 | 154 |
| v4 kw=ampliado match=substring feat=-2 corte=1.75 | 1.000 | 0.322 | 0.487 | 47 | 0 | 99 | 154 |
| v4 kw=ampliado match=substring feat=-2 corte=2.00 | 1.000 | 0.274 | 0.430 | 40 | 0 | 106 | 154 |
| v4 kw=ampliado match=substring feat=-2 corte=2.25 | 1.000 | 0.164 | 0.282 | 24 | 0 | 122 | 154 |
| v4 kw=ampliado match=substring feat=-2 corte=2.50 | 1.000 | 0.158 | 0.272 | 23 | 0 | 123 | 154 |
| v4 kw=ampliado match=substring feat=-2 corte=2.75 | 1.000 | 0.103 | 0.186 | 15 | 0 | 131 | 154 |
| v4 kw=ampliado match=substring feat=-2 corte=3.00 | 1.000 | 0.089 | 0.164 | 13 | 0 | 133 | 154 |
| v4 kw=ampliado match=palavra feat=-0 corte=0.25 | 0.638 | 0.979 | 0.773 | 143 | 81 | 3 | 73 |
| v4 kw=ampliado match=palavra feat=-0 corte=0.50 | 0.621 | 0.897 | 0.734 | 131 | 80 | 15 | 74 |
| v4 kw=ampliado match=palavra feat=-0 corte=0.75 | 0.602 | 0.829 | 0.697 | 121 | 80 | 25 | 74 |
| v4 kw=ampliado match=palavra feat=-0 corte=1.00 | 0.585 | 0.774 | 0.667 | 113 | 80 | 33 | 74 |
| v4 kw=ampliado match=palavra feat=-0 corte=1.25 | 1.000 | 0.658 | 0.793 | 96 | 0 | 50 | 154 |
| v4 kw=ampliado match=palavra feat=-0 corte=1.50 | 1.000 | 0.582 | 0.736 | 85 | 0 | 61 | 154 |
| v4 kw=ampliado match=palavra feat=-0 corte=1.75 | 1.000 | 0.404 | 0.576 | 59 | 0 | 87 | 154 |
| v4 kw=ampliado match=palavra feat=-0 corte=2.00 | 1.000 | 0.288 | 0.447 | 42 | 0 | 104 | 154 |
| v4 kw=ampliado match=palavra feat=-0 corte=2.25 | 1.000 | 0.158 | 0.272 | 23 | 0 | 123 | 154 |
| v4 kw=ampliado match=palavra feat=-0 corte=2.50 | 1.000 | 0.151 | 0.262 | 22 | 0 | 124 | 154 |
| v4 kw=ampliado match=palavra feat=-0 corte=2.75 | 1.000 | 0.103 | 0.186 | 15 | 0 | 131 | 154 |
| v4 kw=ampliado match=palavra feat=-0 corte=3.00 | 1.000 | 0.089 | 0.164 | 13 | 0 | 133 | 154 |
| v4 kw=ampliado match=palavra feat=-1 corte=0.25 | 0.621 | 0.863 | 0.722 | 126 | 77 | 20 | 77 |
| v4 kw=ampliado match=palavra feat=-1 corte=0.50 | 0.606 | 0.801 | 0.690 | 117 | 76 | 29 | 78 |
| v4 kw=ampliado match=palavra feat=-1 corte=0.75 | 0.566 | 0.678 | 0.617 | 99 | 76 | 47 | 78 |
| v4 kw=ampliado match=palavra feat=-1 corte=1.00 | 0.539 | 0.610 | 0.572 | 89 | 76 | 57 | 78 |
| v4 kw=ampliado match=palavra feat=-1 corte=1.25 | 1.000 | 0.486 | 0.654 | 71 | 0 | 75 | 154 |
| v4 kw=ampliado match=palavra feat=-1 corte=1.50 | 1.000 | 0.425 | 0.596 | 62 | 0 | 84 | 154 |
| v4 kw=ampliado match=palavra feat=-1 corte=1.75 | 1.000 | 0.315 | 0.479 | 46 | 0 | 100 | 154 |
| v4 kw=ampliado match=palavra feat=-1 corte=2.00 | 1.000 | 0.253 | 0.404 | 37 | 0 | 109 | 154 |
| v4 kw=ampliado match=palavra feat=-1 corte=2.25 | 1.000 | 0.151 | 0.262 | 22 | 0 | 124 | 154 |
| v4 kw=ampliado match=palavra feat=-1 corte=2.50 | 1.000 | 0.151 | 0.262 | 22 | 0 | 124 | 154 |
| v4 kw=ampliado match=palavra feat=-1 corte=2.75 | 1.000 | 0.103 | 0.186 | 15 | 0 | 131 | 154 |
| v4 kw=ampliado match=palavra feat=-1 corte=3.00 | 1.000 | 0.089 | 0.164 | 13 | 0 | 133 | 154 |
| v4 kw=ampliado match=palavra feat=-2 corte=0.25 | 0.567 | 0.692 | 0.623 | 101 | 77 | 45 | 77 |
| v4 kw=ampliado match=palavra feat=-2 corte=0.50 | 0.553 | 0.644 | 0.595 | 94 | 76 | 52 | 78 |
| v4 kw=ampliado match=palavra feat=-2 corte=0.75 | 0.531 | 0.589 | 0.558 | 86 | 76 | 60 | 78 |
| v4 kw=ampliado match=palavra feat=-2 corte=1.00 | 0.525 | 0.575 | 0.549 | 84 | 76 | 62 | 78 |
| v4 kw=ampliado match=palavra feat=-2 corte=1.25 | 1.000 | 0.479 | 0.648 | 70 | 0 | 76 | 154 |
| v4 kw=ampliado match=palavra feat=-2 corte=1.50 | 1.000 | 0.425 | 0.596 | 62 | 0 | 84 | 154 |
| v4 kw=ampliado match=palavra feat=-2 corte=1.75 | 1.000 | 0.315 | 0.479 | 46 | 0 | 100 | 154 |
| v4 kw=ampliado match=palavra feat=-2 corte=2.00 | 1.000 | 0.253 | 0.404 | 37 | 0 | 109 | 154 |
| v4 kw=ampliado match=palavra feat=-2 corte=2.25 | 1.000 | 0.151 | 0.262 | 22 | 0 | 124 | 154 |
| v4 kw=ampliado match=palavra feat=-2 corte=2.50 | 1.000 | 0.151 | 0.262 | 22 | 0 | 124 | 154 |
| v4 kw=ampliado match=palavra feat=-2 corte=2.75 | 1.000 | 0.103 | 0.186 | 15 | 0 | 131 | 154 |
| v4 kw=ampliado match=palavra feat=-2 corte=3.00 | 1.000 | 0.089 | 0.164 | 13 | 0 | 133 | 154 |
<!-- tuning:end -->
