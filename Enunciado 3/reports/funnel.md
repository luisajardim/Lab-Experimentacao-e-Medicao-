# Funil de Seleção de Repositórios

Este documento registra as etapas do processo de seleção da amostra de repositórios para o cálculo das métricas DORA.

| Etapa | Filtro Aplicado | Motivo de Descarte | Sobras (Contagem Real) |
|---|---|---|---|
| **1. Candidatos Iniciais** | Repositórios open-source extraídos via Search API (agrupados por faixas de estrelas) | - | 1600 |
| **2. ≥ 5 Releases** | Histórico mínimo de entregas (`config.toml: min_releases`) | Repositório possui menos de 5 releases publicadas na janela de observação (1209 descartados). | 391 |
| **3. Com Actions** | Filtragem de repositórios que utilizam o GitHub Actions (`/actions/runs`) | Repositório não possui workflow runs válidos na janela de observação (12 descartados). | 379 |
| **4. ≥ 50 Runs** | Histórico mínimo de execuções de CI/CD (`config.toml: min_workflow_runs`) | Repositório possui menos de 50 execuções válidas de workflow disparadas por push no default branch (68 descartados). | 311 |
| **5. Amostra Final** | Conjunto final validado para o cálculo das métricas DORA | (Nenhum, compõem o dataset final definitivo) | 311 |
