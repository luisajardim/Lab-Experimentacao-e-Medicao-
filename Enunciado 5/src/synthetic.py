"""Gera um `runs.csv` **sintético** no schema oficial, para desenvolver antes da coleta.

Os números são inventados, só para ter dados com a forma certa: 3 máquinas fictícias
(blocos), os 6 tratamentos, os 4 cenários, os 3 projetos e algumas repetições, com ruído
log-normal, efeito de máquina e algumas instalações inválidas. **Não são hipóteses nem
resultados**: servem para a estatística (T08, #103), o poder (T09, #104), o dashboard
(T10, #105) e a aba de adoção (T16, #113) serem construídos em paralelo à coleta.

Uso: `uv run lab05 synthetic` (ou `uv run python -m synthetic`).

Issues: #96 (T01).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd

from config import DATA_SYNTHETIC, MANAGERS, PROJECTS, RUNS_FILENAME, SCENARIOS, SEED
from schema import validate, write_runs

OUT_PATH = DATA_SYNTHETIC / RUNS_FILENAME

MACHINES = {"sint-a": 1.0, "sint-b": 1.35, "sint-c": 0.8}   # fator de velocidade da máquina
REPS = 5
WARMUP_PER_BLOCK = 2

# Valores fictícios de referência para o npm a frio (s, MB, nº de arquivos).
PROJECT_BASE = {
    "express-api": {"wall_s": 6.0, "disk_mb": 12.0, "n_files": 1_500},
    "react-vite": {"wall_s": 18.0, "disk_mb": 120.0, "n_files": 12_000},
    "next-app": {"wall_s": 35.0, "disk_mb": 380.0, "n_files": 28_000},
}
SCENARIO_FACTOR = {"cold": 1.0, "ci": 0.75, "warm-cache": 0.35, "reinstall": 0.08}
# Fator fictício de tempo, disco do projeto e nº de arquivos em relação ao npm.
MANAGER_FACTOR = {
    "npm": (1.00, 1.00, 1.00),
    "pnpm": (0.55, 0.35, 0.30),
    "bun": (0.20, 0.95, 0.95),
    "yarn-classic": (0.90, 1.00, 1.00),
    "yarn-berry-nm": (0.70, 1.00, 1.00),
    "yarn-berry-pnp": (0.45, 0.25, 0.05),
}
NOISE_SIGMA = 0.12
FAIL_RATE = 0.01
PNP_NEXT_FAIL_RATE = 0.3   # fictício: ilustra a coluna build_ok na aba Yarn × Yarn
FAKE_VERSIONS = {"npm": "11.0.0", "pnpm": "10.0.0", "bun": "1.0.0", "yarn-classic": "1.22.22",
                 "yarn-berry-nm": "4.0.0", "yarn-berry-pnp": "4.0.0"}


def generate(seed: int = SEED, reps: int = REPS) -> pd.DataFrame:
    """Devolve o DataFrame sintético, validado pelo schema."""
    rng = np.random.default_rng(seed)
    start = datetime(2026, 11, 15, 9, 0, tzinfo=timezone(timedelta(hours=-3)))
    cells = [(p, s, m) for p in PROJECTS for s in SCENARIOS for m in MANAGERS]
    rows = []
    for machine, speed in MACHINES.items():
        clock = start
        # Aquecimento + repetições, cada repetição numa ordem aleatória das células.
        sequence = [(cells[i], 0, True) for i in rng.choice(len(cells), WARMUP_PER_BLOCK,
                                                            replace=False)]
        for rep in range(1, reps + 1):
            sequence += [(cells[i], rep, False) for i in rng.permutation(len(cells))]
        for order, ((project, scenario, manager), rep, warmup) in enumerate(sequence, start=1):
            base = PROJECT_BASE[project]
            f_time, f_disk, f_files = MANAGER_FACTOR[manager]
            noise = rng.lognormal(0.0, NOISE_SIGMA)
            wall = base["wall_s"] * SCENARIO_FACTOR[scenario] * f_time * speed * noise
            fail_rate = PNP_NEXT_FAIL_RATE if (manager, project) == ("yarn-berry-pnp",
                                                                     "next-app") else FAIL_RATE
            rows.append({
                "machine": machine,
                "run_id": str(uuid.UUID(int=int(rng.integers(0, 2**63)))),
                "timestamp": clock.isoformat(),
                "project": project,
                "scenario": scenario,
                "manager": manager,
                "manager_version": FAKE_VERSIONS[manager],
                "node_version": "24.0.0",
                "registry": "local",
                "rep": rep,
                "order": order,
                "warmup": warmup,
                "wall_s": round(wall, 3),
                "cpu_s": round(wall * rng.uniform(0.6, 1.4), 3),
                "peak_rss_mb": round(rng.uniform(120, 600) * (0.6 if manager == "bun" else 1), 1),
                "disk_mb": round(base["disk_mb"] * f_disk * rng.lognormal(0, 0.02), 2),
                # Medido depois da instalação: o cache já está cheio em todos os cenários.
                "cache_mb": round(base["disk_mb"] * rng.uniform(0.9, 1.3), 2),
                "n_files": int(base["n_files"] * f_files * rng.lognormal(0, 0.02)),
                "build_ok": bool(rng.random() >= fail_rate),
                "exit_code": 0,
            })
            clock += timedelta(seconds=wall + 5)
    return validate(pd.DataFrame(rows))


def main(argv: list[str] | None = None) -> None:
    df = generate()
    write_runs(df, OUT_PATH)
    print(f"[lab05] CSV sintético: {len(df)} linhas em {OUT_PATH.relative_to(OUT_PATH.parents[3])}")


if __name__ == "__main__":
    main()
