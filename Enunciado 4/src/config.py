"""Configuração central do Lab04.

Constantes compartilhadas por todos os módulos: semente fixa (42), caminhos de
`data/real/` e `data/sim/`, situações simuladas (S-base, S-real, S-real-n10, S-outlier),
grade de efeitos (ρ latente de 0 a 0,6), número de réplicas (10.000), níveis de
α (0,05 e 0,01) e a paleta fixa (uma cor para Pearson, outra para Spearman).

Issues: #75 (T01), #76 (T02: semente e caminhos dos dados), #78 (T04: situações).
"""

from pathlib import Path

SEED = 42

ROOT = Path(__file__).resolve().parents[1]
DATA_REAL = ROOT / "data" / "real"
DATA_SIM = ROOT / "data" / "sim"

# Situação -> (gerador, tamanho da amostra). Geradores em `generate.py`.
SITUATIONS = {
    "S-base": ("base", 30),
    "S-real": ("real", 30),
    "S-real-n10": ("real", 10),
    "S-outlier": ("outlier", 30),
}

# S-outlier: cada classe tem esta chance de ser trocada por uma classe extrema
# (1 em 145, a proporção do KC1), sorteada acima deste quantil nas duas variáveis.
OUTLIER_RATE = 1 / 145
OUTLIER_TAIL = 0.99
