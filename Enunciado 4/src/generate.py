"""Gerador de dados simulados.

Gera, de forma vetorizada, conjuntos de dados para as três situações:
S-base (normal bivariada com correlação ρ, n = 30), S-real (cópula gaussiana com
correlação latente ρ → LOC lognormal e defeitos binomial negativa, n = 30) e
S-real-n10 (mesmo gerador da S-real com n = 10).

Issue: #78 (T04).
"""
