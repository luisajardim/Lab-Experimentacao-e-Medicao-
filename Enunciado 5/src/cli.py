"""Comando único do Lab05 (`uv run lab05`).

Sem subcomando, garante o CSV sintético (enquanto não há coleta real) e abre o dashboard.
Subcomandos são adicionados pelas tarefas que os implementam:

- `synthetic`: (re)gera o CSV sintético no schema de `runs.csv` (T01, #96).
- `registry {up,down,status,warm}`: Verdaccio local (T02, #97).
- `collect --machine <nome> [--pilot] [--dry-run]`: coleta medida (T04, #99).
- `specs --machine <nome>`: specs da máquina + checklist do protocolo (T07, #102).
- `downloads`: séries de downloads da API pública do npm (T15, #112).
- `validate`: T13.

Flags do dashboard: `--prepare-only` (não abre o Streamlit); o resto vai para o Streamlit.

Issues: #96 (T01), #97 (T02), #99 (T04), #102 (T07), #112 (T15).
"""

from __future__ import annotations

import subprocess
import sys

import npm_downloads
import power
import registry
import runner
import specs
import synthetic
from config import ROOT

APP_PATH = ROOT / "app.py"

SUBCOMMANDS = {
    "synthetic": synthetic.main,
    "registry": registry.main,
    "collect": runner.main,
    "specs": specs.main,
    "power": power.main,
    "downloads": npm_downloads.main,
}


def prepare_pipeline() -> None:
    """Garante os dados mínimos para o dashboard abrir."""
    if not synthetic.OUT_PATH.exists():
        print("[lab05] Gerando o CSV sintético (desenvolvimento antes da coleta)...")
        synthetic.main()


def main(argv: list[str] | None = None) -> int:
    """Ponto de entrada do script `lab05` definido em `pyproject.toml`."""
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] in SUBCOMMANDS:
        SUBCOMMANDS[args[0]](args[1:])
        return 0
    if args and not args[0].startswith("-"):
        print(f"[lab05] subcomando desconhecido: {args[0]}. Disponíveis: {', '.join(SUBCOMMANDS)}")
        return 2

    prepare_pipeline()
    if "--prepare-only" in args:
        print("[lab05] Dados preparados (--prepare-only).")
        return 0
    cmd = [sys.executable, "-m", "streamlit", "run", str(APP_PATH), *args]
    return subprocess.run(cmd, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
