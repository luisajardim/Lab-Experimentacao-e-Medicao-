"""Comando único do Lab04 (`uv run lab04`).

Executa o fluxo completo: prepara os dados reais (se faltarem), ajusta os
parâmetros, roda as simulações (com cache) e abre o dashboard Streamlit.

Flags: `--prepare-only` (não abre o dashboard) e `--sample-size` (roda também a
simulação extra de tamanho da amostra, #91, mais lenta e opcional).

Issues: #75 (T01), #82 (T07).
"""

import subprocess
import sys

import data
import fit
import sample_size
import simulate
from config import ROOT
from data import FULL_CSV, SAMPLE_CSV
from fit import PARAMS_JSON

APP_PATH = ROOT / "app.py"


def prepare_pipeline() -> None:
    """Garante que dados reais, parâmetros ajustados e simulações (se disponíveis) existam."""
    if not (FULL_CSV.exists() and SAMPLE_CSV.exists()):
        print("[lab04] Gerando CSVs dos dados reais (NASA KC1)...")
        data.main()

    if not PARAMS_JSON.exists():
        print("[lab04] Ajustando parâmetros Gamma e Binomial Negativa...")
        fit.main()

    # Na S02 (T08, #83), `simulate` expõe `main()` ou `run_simulations()` com cache.
    sim_entry = getattr(simulate, "main", None) or getattr(simulate, "run_simulations", None)
    if callable(sim_entry):
        print("[lab04] Verificando / executando simulações de Monte Carlo...")
        sim_entry()


def main(argv: list[str] | None = None) -> int:
    """Ponto de entrada do script `lab04` definido em `pyproject.toml`."""
    args = list(sys.argv[1:] if argv is None else argv)
    prepare_pipeline()

    # Extra opcional (#91): simulação por tamanho de amostra (~1,5 min, com cache).
    if "--sample-size" in args:
        args.remove("--sample-size")
        print("[lab04] Verificando / executando a simulação extra de tamanho da amostra...")
        sample_size.main([])

    if "--prepare-only" in args or "--check" in args:
        print("[lab04] Pipeline preparado com sucesso (--prepare-only).")
        return 0

    cmd = [sys.executable, "-m", "streamlit", "run", str(APP_PATH), *args]
    completed = subprocess.run(cmd, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
