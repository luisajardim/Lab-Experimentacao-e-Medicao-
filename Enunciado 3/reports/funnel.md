# Funil de seleção de repositórios

Gerado por `python -m pipeline --stage report` a partir do snapshot versionado; não edite à mão.

| Etapa | Critério | Descartados | Restantes |
|---|---|---|---:|
| 1. Resultados da busca | Search API, 12 faixas de estrelas (máx. 1.000 por consulta) | — | 12000 |
| 2. Coletados | JSON de releases, tags, commits e runs salvo em `data/gold/` | 11175 não persistidos: descartados no collect (sem Actions, poucas releases ou poucos runs) ou não visitados; o snapshot não guarda o motivo por repositório | 825 |
| 3. Com Actions | ≥ 1 workflow run `push` no default branch na janela | 0 sem runs válidos | 825 |
| 4. ≥ 5 releases | releases publicadas (não-draft, não-pré-release) na janela | 64 com poucas releases | 761 |
| 5. ≥ 50 runs | runs `push` no default branch na janela | 0 com poucos runs | 761 |
| 6. Manifesto | população congelada (`candidate_manifest.csv`, seed 42) | 11 fora do corte | 750 |
| 7. Amostra final | corte determinístico do estágio `metrics` (seed 42) | 435 fora do corte | 315 |
