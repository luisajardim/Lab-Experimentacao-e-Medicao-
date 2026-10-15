# Relatório de Métricas DORA

Total de repositórios analisados: 311

## Sumário das Métricas

- **lead_time_a_hours**: mediana=191.23, média=1222.49, min=0.03, max=70292.95
- **lead_time_b_hours**: mediana=180.87, média=939.13, min=0.04, max=53267.31
- **cfr_a**: mediana=0.06, média=0.10, min=0.00, max=1.00
- **recovery_hours**: mediana=3.88, média=44.54, min=0.02, max=3798.22
- **deployment_frequency_per_week**: mediana=0.33, média=0.82, min=0.10, max=13.80
- **deployment_frequency_with_tags_per_week**: mediana=0.71, média=2.00, min=0.12, max=37.52

## Classificação DORA

### Variante C1
- Medium/Low: 155
- High: 19
- Elite: 1

### Variante C2
- Medium/Low: 150
- High: 24
- Elite: 1

### Variante C3
- Medium/Low: 154
- High: 20
- Elite: 1

## Correlações (Spearman)

- **lead_time_a_vs_cfr_a**: ρ=-0.136, p=0.0581, não significativo
- **lead_time_b_vs_cfr_a**: ρ=-0.115, p=0.1109, não significativo
- **deploy_freq_vs_recovery**: ρ=-0.193, p=0.0011, significativo
- **deploy_freq_tags_vs_recovery**: ρ=-0.194, p=0.0010, significativo

---
*Gerado automaticamente pelo pipeline DORA Miner (Lab03).*
