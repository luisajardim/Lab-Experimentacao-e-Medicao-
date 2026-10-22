# T23 — RQ08 (Bônus): Taxa de Retrabalho e Evolução Temporal

Amostra analisada: **315 repositórios** no período de observação (2025-10-01 a 2026-09-30).
Heurística de release corretiva: **v2 kw=base match=palavra** (calibrada e validada contra consenso com F1 ≥ 0,70).

---

## 1. Taxa de Retrabalho (Rework Rate — DORA 2024)

A *Rework Rate* mede a proporção de releases corretivas frente ao total de releases entregues. Diferente da Change Failure Rate clássica de CI (que mede builds com falha no pipeline), a taxa de retrabalho reflete o percentual de esforço despendido em corrigir defeitos que já chegaram aos usuários.

### Estatísticas Descritivas na Janela de Observação

| Métrica | n | Média | Mediana | Desv. Padrão | Q1 (25%) | Q3 (75%) | IQR | Min | Max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Rework Rate (janela) | 315 | 0.7459 | 0.8750 | 0.2895 | 0.5869 | 0.9733 | 0.3864 | 0.0000 | 1.0000 |
| Change Failure Rate (CFR a) | 315 | 0.0997 | 0.0530 | 0.1446 | 0.0203 | 0.1157 | 0.0953 | 0.0000 | 1.0000 |
| Diferença (Rework − CFR) | 315 | 0.6462 | 0.7545 | 0.3385 | 0.4616 | 0.9102 | 0.4486 | -0.8000 | 1.0000 |

### Discussão Conceitual: Rework Rate vs. Change Failure Rate

1. **Unidade de análise:** O CFR(a) baseia-se em *execuções de workflow de CI*, capturando falhas imediatas de integração antes ou durante a entrega. Já a Rework Rate baseia-se em *releases completas*, capturando defeitos pós-entrega que demandaram uma nova versão com foco corretivo.
2. **Ordem de magnitude observada:** A mediana da Rework Rate é expressivamente superior à do CFR(a). Enquanto os testes automatizados de CI mantêm uma taxa de falha baixa (mediana ~5,3%), a grande maioria dos repositórios tem lançamentos de patch frequentes (mediana de retrabalho ~87,5%), indicando que a natureza iterativa de projetos open-source é predominantemente corretiva entre versões principais.

---

## 2. Evolução Temporal (Teste de Mann-Kendall)

Para cada repositório, foi aplicado o teste não-paramétrico de Mann-Kendall (`pymannkendall`) para identificar tendências monotônicas significativas ($p < 0{,}05$) em cada direção.

### Proporções de Repositórios por Tendência

| Dimensão / Escala | Total | Aumento (pior/mais) | % Aumento | Queda (melhor/menos) | % Queda | Estável / Desprezível | % Estável |
|---|---:|---:|---:|---:|---:|---:|---:|
| Deploy Frequency (Trimestral) | 315 | 0 | 0.0% | 0 | 0.0% | 315 | 100.0% |
| Rework Rate (Trimestral) | 315 | 0 | 0.0% | 0 | 0.0% | 315 | 100.0% |
| CFR CI (Trimestral) | 315 | 0 | 0.0% | 0 | 0.0% | 315 | 100.0% |
| Deploy Frequency (Mensal) | 315 | 53 | 16.8% | 19 | 6.0% | 243 | 77.1% |
| CFR CI (Mensal) | 315 | 35 | 11.1% | 18 | 5.7% | 262 | 83.2% |

### Achado Metodológico: Escala Trimestral vs. Mensal

- **Limitação assintótica na escala trimestral ($n = 4$):** O teste de Mann-Kendall com apenas 4 observações possui poder estatístico limitado para atingir $p < 0{,}05$ assintótico (a sequência monótona perfeita atinge $p \approx 0{,}089$). Portanto, 100% dos repositórios são classificados como `negligible` (sem tendência estatisticamente comprovável a 5%).
- **Resolução na escala mensal ($n = 12$):** Ao expandir para os 12 meses da janela, detectam-se tendências significativas: **16,8% dos repositórios aumentaram sua frequência de deploy** e **11,1% apresentaram aumento na taxa de falha de CI**, enquanto a vasta maioria (~77% a 83%) manteve desempenho estável ao longo de todo o ano de observação.
