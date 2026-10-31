"""Motor de simulação de Monte Carlo (Q1, Q2 e Q3).

Roda 10.000 réplicas para cada combinação de situação × efeito, aplica os dois
testes e salva todos os p-valores em `data/sim/` (com cache), além do r e do ρ
de Spearman populacionais correspondentes a cada ρ latente.

Issue: #83 (T08).
"""
