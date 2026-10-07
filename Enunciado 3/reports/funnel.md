# Funil de Seleção de Repositórios

Este documento registra as etapas do processo de seleção da amostra de repositórios para o cálculo das métricas DORA.

| Etapa | Filtro Aplicado | Motivo de Descarte | Sobras (Exemplo/Estimativa) |
|---|---|---|---|
| **1. Candidatos Iniciais** | Repositórios open-source extraídos via Search API (agrupados por estrelas) | - | - |
| **2. Com Actions** | Filtragem de repositórios que utilizam o GitHub Actions (`/actions/workflows`) | Repositório não utiliza GitHub Actions como CI/CD principal ou a aba Actions está desativada. | - |
| **3. ≥ 5 Releases** | Histórico mínimo de entregas (`config.toml: min_releases`) | Repositório possui menos de 5 releases publicadas na janela de observação. | - |
| **4. ≥ 50 Runs** | Histórico mínimo de execuções de CI/CD (`config.toml: min_workflow_runs`) | Repositório possui menos de 50 execuções válidas de workflow disparadas por push no default branch. | - |
| **5. Amostra Final** | Conjunto final validado para o cálculo das métricas DORA | (Nenhum, compõem o dataset final) | - |
