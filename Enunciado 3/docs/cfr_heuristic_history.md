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

O loop de tuning varia, para v2 e v3:

- **conjunto de palavras-chave:** `base` (`fix`, `revert`, `hotfix`) ou
  `ampliado` (+ `bug`, `patch`, `regression`, `crash`);
- **casamento:** `substring` (o enunciado literal; `prefix` casa com `fix`) ou
  `palavra` (início de palavra: `fixes`/`fixed` casam, `prefix` não);
- **corte da v3:** 0,25 a 3,00 em passos de 0,25.

A combinação escolhida é a de maior F1; em empate, vale a mais simples
(v1 → v2 → v3). Como o corte é escolhido na própria amostra-ouro, o F1 reportado
é otimista; isso deve ser citado como ameaça à validade no relatório.

## Execuções

A seção abaixo é reescrita por `python scripts/tune_cfr.py`.

<!-- tuning:start -->
_Ainda não executado: depende de `data/gold/labels_consensus.csv` (T13)._
<!-- tuning:end -->
