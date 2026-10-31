"""Coleta dos dados reais.

Baixa o dataset NASA KC1 por classe (OpenML id 1070, `kc1-numeric`, C++),
extrai as colunas `sumLOC_TOTAL` (LOC da classe) e `NUMDEFECTS` (nº de defeitos)
e salva o dataset completo (145 classes) e a amostra de 30 classes sorteada com
semente fixa em `data/real/`. A proveniência fica em `docs/fonte_dados.md`.

Issue: #76 (T02).
"""
