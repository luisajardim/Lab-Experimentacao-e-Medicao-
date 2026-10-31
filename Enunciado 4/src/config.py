"""Configuração central do Lab04.

Constantes compartilhadas por todos os módulos: semente fixa (42), caminhos de
`data/real/` e `data/sim/`, situações simuladas (S-base, S-real, S-real-n10),
grade de efeitos (ρ latente de 0 a 0,6), número de réplicas (10.000), níveis de
α (0,05 e 0,01) e a paleta fixa (uma cor para Pearson, outra para Spearman).

Issues: #75 (T01), #76 (T02: semente e caminhos dos dados).
"""

from pathlib import Path

SEED = 42

ROOT = Path(__file__).resolve().parents[1]
DATA_REAL = ROOT / "data" / "real"
DATA_SIM = ROOT / "data" / "sim"
