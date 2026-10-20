# Relatório de Métricas DORA

Total de repositórios analisados: 315

## Sumário das Métricas

- **lead_time_a_hours**: mediana=166.26, média=1561.49, min=0.00, max=95349.14
- **lead_time_b_hours**: mediana=151.73, média=1040.77, min=0.00, max=63885.39
- **cfr_a**: mediana=0.05, média=0.10, min=0.00, max=1.00
- **recovery_hours**: mediana=3.32, média=33.25, min=0.03, max=1084.76
- **deployment_frequency_per_week**: mediana=0.35, média=0.81, min=0.10, max=13.80
- **deployment_frequency_with_tags_per_week**: mediana=0.81, média=2.09, min=0.19, max=31.52

## Classificação DORA

### Variante C1
- High: 113
- Medium: 97
- Elite: 22
- Low: 14

### Variante C2
- High: 133
- Medium: 81
- Elite: 26
- Low: 6

### Variante C3
- High: 135
- Medium: 81
- Elite: 25
- Low: 5

## Correlações (Spearman)

- **lead_time_a_vs_cfr_a**: ρ=-0.160, p=0.0081, significativo
- **lead_time_b_vs_cfr_a**: ρ=-0.136, p=0.0246, significativo
- **deploy_freq_vs_recovery**: ρ=-0.167, p=0.0046, significativo
- **deploy_freq_tags_vs_recovery**: ρ=-0.152, p=0.0103, significativo

---
*Gerado automaticamente pelo pipeline DORA Miner (Lab03).*
