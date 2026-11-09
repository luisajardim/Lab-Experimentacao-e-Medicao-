"""Converte os resultados da simulação de Parquet para CSV, para integrações externas.

Lê `data/sim/pvalues.parquet` (ou outro `.parquet` passado em `--input`) e grava o
CSV equivalente. Por padrão, a saída vai para `data/sim/export/`, que fica fora do
git (o CSV tem ~30 MB; o Parquet, que é a fonte, é o arquivo versionado).

Uso:
    uv run python scripts/parquet_to_csv.py
    uv run python scripts/parquet_to_csv.py --input data/sim/pvalues.parquet --output saida.csv

Issue: #83 (T08).
"""

import argparse
from pathlib import Path

import pandas as pd

from config import DATA_SIM
from simulate import PVALUES_FILE

EXPORT_DIR = DATA_SIM / "export"


def convert(input_path: Path, output_path: Path | None = None) -> Path:
    """Converte um `.parquet` para `.csv` e devolve o caminho do CSV gravado."""
    output_path = output_path or EXPORT_DIR / f"{input_path.stem}.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.read_parquet(input_path).to_csv(output_path, index=False)
    return output_path


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Converte Parquet da simulação para CSV.")
    parser.add_argument("--input", type=Path, default=DATA_SIM / PVALUES_FILE)
    parser.add_argument("--output", type=Path, default=None, help="padrão: data/sim/export/<nome>.csv")
    args = parser.parse_args(argv)
    out = convert(args.input, args.output)
    print(f"CSV gravado em {out} ({out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
