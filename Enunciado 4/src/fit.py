"""Ajuste dos parâmetros da simulação a partir dos dados reais.

Ajusta, no KC1 inteiro, uma lognormal para o LOC (média e desvio do log) e uma
binomial negativa para o nº de defeitos (média e dispersão), e salva os
parâmetros em `data/real/params.json`, usados pelo gerador de dados simulados.

Issue: #77 (T03).
"""
