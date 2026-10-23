# T23 — RQ08 (Bônus): Taxa de Retrabalho e Evolução Temporal

Amostra analisada: **315 repositórios** no período de observação (2025-10-01 a 2026-09-30).
Heurística de release corretiva: a mesma da CFR (b), escolhida no tuning contra o consenso (**v4 kw=base match=palavra feat=-0 corte=0.75; F1 = 0.574 no consenso da amostra-ouro**). Deploy = release publicada, não-draft e não-pré-release.

---

## 1. Taxa de Retrabalho (Rework Rate — DORA 2024)

A *Rework Rate* mede a proporção de releases corretivas frente ao total de releases entregues. Diferente da Change Failure Rate clássica de CI (que mede builds com falha no pipeline), a taxa de retrabalho reflete o percentual de esforço despendido em corrigir defeitos que já chegaram aos usuários.

### Estatísticas Descritivas na Janela de Observação

| Métrica | n | Média | Mediana | Desv. Padrão | Q1 (25%) | Q3 (75%) | IQR | Min | Max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Rework Rate (janela) | 315 | 0.6976 | 0.7692 | 0.2661 | 0.5240 | 0.9091 | 0.3851 | 0.0000 | 1.0000 |
| Change Failure Rate (CFR a) | 315 | 0.0997 | 0.0530 | 0.1446 | 0.0203 | 0.1157 | 0.0953 | 0.0000 | 1.0000 |
| Diferença (Rework − CFR) | 315 | 0.5978 | 0.6712 | 0.2991 | 0.4139 | 0.8308 | 0.4168 | -0.3596 | 1.0000 |

### Discussão Conceitual: Rework Rate vs. Change Failure Rate

1. **Unidade de análise:** O CFR(a) baseia-se em *execuções de workflow de CI*, capturando falhas imediatas de integração antes ou durante a entrega. Já a Rework Rate baseia-se em *releases completas*, capturando defeitos pós-entrega que demandaram uma nova versão com foco corretivo.
2. **Ordem de magnitude observada:** a mediana da Rework Rate (76,9%) é muito superior à do CFR (a) (5,3%). A diferença vem da unidade: o CI corrige falhas de integração antes da release, enquanto boa parte das releases de projetos open-source é de patch, que a heurística tende a marcar como corretiva (precisão baixa na amostra-ouro).

---

## 2. Evolução Temporal (Teste de Mann-Kendall)

Para cada repositório, foi aplicado o teste não-paramétrico de Mann-Kendall (`pymannkendall`) para identificar tendências monotônicas significativas ($p < 0{,}05$) em cada direção.

### Proporções de Repositórios por Tendência

| Dimensão / Escala | Total | Aumento (pior/mais) | % Aumento | Queda (melhor/menos) | % Queda | Estável / Desprezível | % Estável |
|---|---:|---:|---:|---:|---:|---:|---:|
| Deploy Frequency (Trimestral) | 315 | 0 | 0.0% | 0 | 0.0% | 315 | 100.0% |
| Rework Rate (Trimestral) | 315 | 0 | 0.0% | 0 | 0.0% | 315 | 100.0% |
| CFR CI (Trimestral) | 315 | 0 | 0.0% | 0 | 0.0% | 315 | 100.0% |
| Deploy Frequency (Mensal) | 315 | 48 | 15.2% | 21 | 6.7% | 246 | 78.1% |
| CFR CI (Mensal) | 315 | 14 | 4.4% | 23 | 7.3% | 278 | 88.3% |

### Achado Metodológico: Escala Trimestral vs. Mensal

- **Limitação assintótica na escala trimestral ($n = 4$):** O teste de Mann-Kendall com apenas 4 observações possui poder estatístico limitado para atingir $p < 0{,}05$ assintótico (a sequência monótona perfeita atinge $p \approx 0{,}089$). Portanto, 100% dos repositórios são classificados como `negligible` (sem tendência estatisticamente comprovável a 5%).
- **Resolução na escala mensal ($n = 12$):** a frequência de deploy aumenta em 15,2% dos repositórios e cai em 6,7%; o CFR (a) aumenta em 4,4% e cai em 7,3%. Os demais não têm tendência significativa a 5%.
