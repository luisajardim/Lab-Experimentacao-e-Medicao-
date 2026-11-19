"""Nº de repetições da coleta completa por análise de poder (simulação sobre o piloto).

Como funciona (no estilo do `sample_size.py` do Lab04):

1. **Ruído real do piloto.** Para cada projeto × cenário, em cada bloco (máquina, repetição),
   calcula d = log(tempo do gerenciador) − log(tempo do npm). Centrar d em cada gerenciador
   (subtrair a mediana) deixa só a variação de uma repetição para outra, sem efeito nenhum. As 5
   comparações contra o npm de um projeto × cenário são juntadas (25 valores no piloto); o log
   torna o ruído comparável entre gerenciadores rápidos e lentos.
2. **Efeito conhecido.** Um speedup s (1,1 = 10% mais rápido que o npm) desloca d em −log(s).
3. **Teste.** Sorteia `n_pares = máquinas × N` diferenças com reposição, aplica o Wilcoxon pareado
   bicaudal e conta as rejeições com α/5 (o 1º degrau do Holm com 5 comparações: o caso mais
   exigente, quando só um gerenciador difere do npm).
4. **Escolha de N.** O menor N por máquina com poder ≥ 80% em **todos** os projetos × cenários para
   o efeito-alvo, cruzado com o tempo estimado da coleta (duração média de uma instalação no
   piloto, já com preparação e `build`).

O piloto só tem os cenários cold e warm-cache: o ruído do cold é usado para o ci (ambos sem
cache) e o do warm-cache para o reinstall (ambos com cache).

Uso: `uv run lab05 power` → `data/power/power.csv` + resumo no terminal (texto em `docs/poder.md`).

Issue: #104 (T09).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as sps

import stats
from config import (
    ALPHA,
    CONTROL,
    DATA,
    DATA_RAW,
    MANAGERS,
    PROJECTS,
    RUNS_FILENAME,
    SCENARIOS,
    SEED,
)
from schema import read_runs

PILOT_CSV = DATA_RAW / "pilot" / RUNS_FILENAME
POWER_DIR = DATA / "power"
POWER_CSV = POWER_DIR / "power.csv"

MACHINES = 3
N_GRID = (3, 4, 5, 6, 8, 10, 12, 15)          # repetições por máquina
SPEEDUPS = (1.1, 1.2, 1.3, 1.5)               # efeito: npm / gerenciador
TARGET_SPEEDUP = 1.2
TARGET_POWER = 0.80
N_COMPARISONS = len(MANAGERS) - 1             # 5 gerenciadores contra o npm
SIMS = 2_000
WARMUP = 2

# Cenários sem piloto herdam o ruído do cenário com a mesma situação de cache.
NOISE_SOURCE = {"cold": "cold", "ci": "cold", "warm-cache": "warm-cache", "reinstall": "warm-cache"}


def load_pilot(path: Path = PILOT_CSV) -> pd.DataFrame:
    """Instalações do piloto, sem as rodadas de aquecimento."""
    df = read_runs(path)
    return df[~df["warmup"]].reset_index(drop=True)


def log_ratio_noise(df: pd.DataFrame, control: str = CONTROL) -> dict[tuple[str, str], np.ndarray]:
    """Ruído centrado de log(gerenciador / controle), juntando os gerenciadores, por projeto × cenário."""
    noise: dict[tuple[str, str], np.ndarray] = {}
    for (project, scenario), sub in df.groupby(["project", "scenario"], observed=True):
        pieces = []
        for manager in MANAGERS:
            if manager == control:
                continue
            wide = stats.paired_wide(sub, [control, manager])
            if len(wide) < 2:
                continue
            d = np.log(wide[manager].to_numpy()) - np.log(wide[control].to_numpy())
            pieces.append(d - np.median(d))
        if pieces:
            noise[project, scenario] = np.concatenate(pieces)
    return noise


def simulate_power(noise: np.ndarray, n_pairs: int, speedup: float, alpha: float,
                   sims: int = SIMS, rng: np.random.Generator | None = None) -> float:
    """Proporção de simulações em que o Wilcoxon pareado rejeita H₀ com nível `alpha`."""
    rng = np.random.default_rng(SEED) if rng is None else rng
    d = rng.choice(noise, size=(sims, n_pairs), replace=True) - np.log(speedup)
    if n_pairs < 2:
        return 0.0
    with np.errstate(all="ignore"):
        p = sps.wilcoxon(d, axis=1, alternative="two-sided", zero_method="wilcox").pvalue
    return float(np.mean(np.nan_to_num(p, nan=1.0) < alpha))


def power_table(noise: dict[tuple[str, str], np.ndarray], machines: int = MACHINES,
                n_grid=N_GRID, speedups=SPEEDUPS, alpha: float = ALPHA,
                n_comparisons: int = N_COMPARISONS, sims: int = SIMS,
                seed: int = SEED) -> pd.DataFrame:
    """Poder por projeto × cenário (os 4 da coleta) × speedup × N por máquina."""
    alpha_eff = alpha / n_comparisons
    rows = []
    for project in PROJECTS:
        for scenario in SCENARIOS:
            key = (project, NOISE_SOURCE[scenario])
            if key not in noise:
                continue
            for s_i, speedup in enumerate(speedups):
                for n in n_grid:
                    # stream estável por célula: mudar a grade não muda os números das outras
                    rng = np.random.default_rng([seed, list(PROJECTS).index(project),
                                                 list(SCENARIOS).index(scenario), s_i, n])
                    rows.append(
                        {
                            "project": project,
                            "scenario": scenario,
                            "noise_from": NOISE_SOURCE[scenario],
                            "noise_sd": float(np.std(noise[key], ddof=1)),
                            "speedup": speedup,
                            "reps_per_machine": n,
                            "n_pairs": machines * n,
                            "alpha_eff": alpha_eff,
                            "power": simulate_power(noise[key], machines * n, speedup,
                                                    alpha_eff, sims, rng),
                        }
                    )
    return pd.DataFrame(rows)


def worst_case(table: pd.DataFrame) -> pd.DataFrame:
    """Menor poder entre os projetos × cenários, por speedup × N (a célula mais ruidosa manda)."""
    return (table.groupby(["speedup", "reps_per_machine"], as_index=False)["power"].min()
            .pivot(index="reps_per_machine", columns="speedup", values="power"))


def choose_n(table: pd.DataFrame, speedup: float = TARGET_SPEEDUP,
             target: float = TARGET_POWER) -> int | None:
    """Menor N por máquina com poder ≥ `target` em todas as células para o `speedup` dado."""
    worst = worst_case(table)
    if speedup not in worst.columns:
        return None
    ok = worst.index[worst[speedup] >= target]
    return int(ok.min()) if len(ok) else None


MAX_GAP_S = 600.0   # intervalo maior que isso é pausa da coleta, não instalação


def seconds_per_install(path: Path = PILOT_CSV, max_gap_s: float = MAX_GAP_S) -> float:
    """Duração média de uma instalação no piloto, de início a início (inclui preparação e build).

    Intervalos acima de `max_gap_s` são pausas e ficam de fora: no piloto, as 30 linhas do pnpm
    foram recoletadas 19 min depois do fim (correção c34174d), e contar essa pausa inflava a média
    de ~24 s para ~30 s por instalação.
    """
    df = read_runs(path)
    gaps = pd.to_datetime(df["timestamp"]).sort_values().diff().dt.total_seconds().dropna()
    return float(gaps[gaps <= max_gap_s].mean())


def collection_hours(reps: int, seconds: float, warmup: int = WARMUP) -> float:
    """Horas de coleta numa máquina: 6 gerenciadores × 4 cenários × 3 projetos × N + aquecimentos."""
    installs = len(MANAGERS) * len(SCENARIOS) * len(PROJECTS) * reps + warmup
    return installs * seconds / 3600


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Nº de repetições por análise de poder (T09).")
    parser.add_argument("--sims", type=int, default=SIMS, help=f"simulações por ponto ({SIMS})")
    parser.add_argument("--machines", type=int, default=MACHINES, help="máquinas (blocos)")
    args = parser.parse_args([] if argv is None else argv)

    pilot = load_pilot()
    table = power_table(log_ratio_noise(pilot), machines=args.machines, sims=args.sims)
    POWER_DIR.mkdir(parents=True, exist_ok=True)
    table.to_csv(POWER_CSV, index=False)

    seconds = seconds_per_install()
    n = choose_n(table)
    print(f"[power] Poder mínimo entre projetos × cenários ({args.machines} máquinas, "
          f"α/{N_COMPARISONS} = {ALPHA / N_COMPARISONS:.3f}):")
    print((worst_case(table) * 100).round(0).to_string())
    print(f"[power] {seconds:.1f} s por instalação no piloto (com preparação e build)")
    for reps in N_GRID:
        print(f"         N = {reps:>2}: {collection_hours(reps, seconds):4.1f} h por máquina")
    print(f"[power] N escolhido para speedup {TARGET_SPEEDUP} e poder {TARGET_POWER:.0%}: {n}")
    print(f"[power] Salvo em {POWER_CSV.relative_to(DATA.parent)}")


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])

