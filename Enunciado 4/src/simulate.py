"""Motor de simulação de Monte Carlo (Q1, Q2 e Q3).

Roda 10.000 réplicas para cada combinação de situação × efeito, aplica os dois
testes e salva todos os p-valores em `data/sim/` (com cache), além do r e do ρ
de Spearman populacionais correspondentes a cada ρ latente.

Saídas em `data/sim/` (formato descrito em `docs/simulacao.md`):
- `pvalues.parquet`: uma linha por réplica (coeficientes e p-valores dos dois testes);
- `summary.csv`: taxa de rejeição por situação × efeito × α × teste;
- `population.csv`: r e ρₛ populacionais de cada situação × efeito;
- `meta.json`: chave de cache, configuração e tempo de execução.

Uso: `uv run python -m simulate [--force] [--reps N]`
(o `uv run lab04` chama `main()` e só re-simula se a configuração mudou).

Issue: #83 (T08).
"""

import argparse
import hashlib
import json
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

from config import (
    ALPHAS,
    DATA_SIM,
    EFFECT_GRID,
    OUTLIER_RATE,
    OUTLIER_TAIL,
    REPS,
    SEED,
    SITUATIONS,
)
from fit import PARAMS_JSON
from generate import generate
from stat_tests import pearson, spearman

PVALUES_FILE = "pvalues.parquet"
SUMMARY_FILE = "summary.csv"
POPULATION_FILE = "population.csv"
META_FILE = "meta.json"

# Tamanho da amostra usada para estimar r e ρₛ "populacionais" de cada célula.
POPULATION_N = 1_000_000
TESTS = ("pearson", "spearman")

# Código que, se mudar, invalida o cache (além da configuração).
CODE_FILES = ("generate.py", "stat_tests.py", "simulate.py")
SRC_DIR = Path(__file__).resolve().parent


def cell_rng(name: str, rho: float, purpose: int = 0) -> np.random.Generator:
    """Stream independente e estável para cada (nome, efeito).

    A chave usa o nome (situação ou gerador) e o valor do efeito, não a posição
    na configuração: incluir, remover ou reordenar situações e efeitos não muda
    os números das células que continuam existindo.
    `purpose` separa a simulação (0) da estimativa populacional (1).
    """
    key = (zlib.crc32(name.encode()), round(rho * 1000), purpose)
    return np.random.default_rng(np.random.SeedSequence(SEED, spawn_key=key))


def simulate_cell(situation: str, rho: float, reps: int) -> pd.DataFrame:
    """Gera `reps` conjuntos, aplica os dois testes e devolve uma linha por réplica."""
    x, y = generate(situation, rho, reps=reps, rng=cell_rng(situation, rho))
    r_test, s_test = pearson(x, y), spearman(x, y)
    return pd.DataFrame(
        {
            "situation": situation,
            "rho": rho,
            "rep": np.arange(reps, dtype=np.int32),
            "r": r_test.coef,
            "p_pearson": r_test.p,
            "rho_s": s_test.coef,
            "p_spearman": s_test.p,
        }
    )


def population_cell(kind: str, rho: float, n: int | None = None) -> dict:
    """r e ρₛ numa amostra grande de um gerador (estimativa dos valores populacionais).

    A população depende só do gerador, não do n da situação: S-real e S-real-n10
    compartilham o mesmo resultado.
    """
    n = POPULATION_N if n is None else n
    x, y = generate(kind, rho, n=n, rng=cell_rng(kind, rho, purpose=1))
    return {"r_pop": float(pearson(x[0], y[0]).coef), "rho_s_pop": float(spearman(x[0], y[0]).coef)}


def summarize(pvalues: pd.DataFrame, alphas=ALPHAS) -> pd.DataFrame:
    """Taxa de rejeição por situação × efeito × α × teste, com erro padrão de Monte Carlo.

    Réplicas com p-valor NaN (amostra constante) contam como "não rejeita H₀";
    `n_nan` registra quantas foram.
    """
    rows = []
    for (situation, rho), group in pvalues.groupby(["situation", "rho"], sort=False):
        n = len(group)
        for alpha in alphas:
            for test in TESTS:
                p = group[f"p_{test}"].to_numpy()
                rate = float(np.mean(p < alpha))
                rows.append(
                    {
                        "situation": situation,
                        "rho": rho,
                        "alpha": alpha,
                        "test": test,
                        "reject_rate": rate,
                        "mc_se": float(np.sqrt(rate * (1 - rate) / n)),
                        "n_reps": n,
                        "n_nan": int(np.isnan(p).sum()),
                    }
                )
    return pd.DataFrame(rows)


def file_sha256(path: Path) -> str:
    """SHA-256 do conteúdo com fim de linha normalizado para LF.

    No Windows, o checkout com `core.autocrlf=true` grava os arquivos com CRLF; sem a
    normalização, o hash mudaria e o cache re-simularia tudo com o mesmo código.
    """
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def config_snapshot(reps: int) -> dict:
    """Tudo o que, se mudar, exige re-simular."""
    return {
        "seed": SEED,
        "reps": reps,
        "effect_grid": list(EFFECT_GRID),
        "alphas": list(ALPHAS),
        "situations": {k: list(v) for k, v in SITUATIONS.items()},
        "outlier_rate": OUTLIER_RATE,
        "outlier_tail": OUTLIER_TAIL,
        "population_n": POPULATION_N,
        "params_sha256": file_sha256(PARAMS_JSON),
        "code_sha256": {name: file_sha256(SRC_DIR / name) for name in CODE_FILES},
    }


def cache_key(snapshot: dict) -> str:
    return hashlib.sha256(json.dumps(snapshot, sort_keys=True).encode()).hexdigest()


def is_cached(out_dir: Path, key: str) -> bool:
    meta = out_dir / META_FILE
    files = (PVALUES_FILE, SUMMARY_FILE, POPULATION_FILE)
    if not meta.exists() or not all((out_dir / f).exists() for f in files):
        return False
    return json.loads(meta.read_text()).get("cache_key") == key


def run_simulations(
    reps: int = REPS, out_dir: Path = DATA_SIM, force: bool = False, verbose: bool = True
) -> dict:
    """Roda (ou reaproveita) todas as células e grava as saídas. Devolve o `meta`."""
    snapshot = config_snapshot(reps)
    key = cache_key(snapshot)
    if not force and is_cached(out_dir, key):
        if verbose:
            print(f"[simulate] Resultados em {out_dir.name}/ já batem com a configuração (cache).")
        return json.loads((out_dir / META_FILE).read_text())

    start = time.perf_counter()
    cells, population, by_kind = [], [], {}
    for situation, (kind, _) in SITUATIONS.items():
        for rho in EFFECT_GRID:
            cells.append(simulate_cell(situation, rho, reps))
            if (kind, rho) not in by_kind:
                by_kind[kind, rho] = population_cell(kind, rho)
            population.append({"situation": situation, "rho": rho, **by_kind[kind, rho]})
        if verbose:
            print(f"[simulate] {situation}: {len(EFFECT_GRID)} efeitos × {reps} réplicas")
    pvalues = pd.concat(cells, ignore_index=True)
    pvalues["situation"] = pd.Categorical(pvalues["situation"], categories=list(SITUATIONS))
    elapsed = time.perf_counter() - start

    out_dir.mkdir(parents=True, exist_ok=True)
    pvalues.to_parquet(out_dir / PVALUES_FILE, index=False)
    summary = summarize(pvalues.assign(situation=pvalues["situation"].astype(str)))
    summary.to_csv(out_dir / SUMMARY_FILE, index=False)
    pd.DataFrame(population).to_csv(out_dir / POPULATION_FILE, index=False)
    meta = {"cache_key": key, "config": snapshot, "elapsed_seconds": round(elapsed, 1)}
    (out_dir / META_FILE).write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    if verbose:
        print(f"[simulate] {len(pvalues):,} réplicas em {elapsed:.1f} s → {out_dir}")
    return meta


def load_pvalues(out_dir: Path = DATA_SIM) -> pd.DataFrame:
    return pd.read_parquet(out_dir / PVALUES_FILE)


def load_summary(out_dir: Path = DATA_SIM) -> pd.DataFrame:
    return pd.read_csv(out_dir / SUMMARY_FILE)


def load_population(out_dir: Path = DATA_SIM) -> pd.DataFrame:
    return pd.read_csv(out_dir / POPULATION_FILE)


def main(argv: list[str] | None = None) -> None:
    """Sem argumentos (como no `uv run lab04`), usa os padrões e respeita o cache."""
    parser = argparse.ArgumentParser(description="Simulações de Monte Carlo do Lab04.")
    parser.add_argument("--force", action="store_true", help="re-simula mesmo com cache válido")
    parser.add_argument("--reps", type=int, default=REPS, help=f"réplicas por célula ({REPS})")
    args = parser.parse_args([] if argv is None else argv)
    run_simulations(reps=args.reps, force=args.force)


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
