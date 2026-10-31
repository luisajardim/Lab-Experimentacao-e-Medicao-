"""Coleta dos dados reais.

Baixa o dataset NASA KC1 por classe (OpenML id 1070, `kc1-numeric`, C++),
extrai as colunas `sumLOC_TOTAL` (LOC da classe) e `NUMDEFECTS` (nº de defeitos)
e salva o dataset completo (145 classes) e a amostra de 30 classes sorteada com
semente fixa em `data/real/`. A proveniência fica em `docs/fonte_dados.md`.

Uso: `uv run python -m data`

Issue: #76 (T02).
"""

import hashlib
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import arff

from config import DATA_REAL, SEED

OPENML_ID = 1070
ARFF_URL = "https://openml.org/data/v1/download/53953/kc1-numeric.arff"
ARFF_SHA256 = "e83d22835bc98e4602acce372900c2d75bae0b52d073f6fa1f13984a64c0f9da"

ARFF_PATH = DATA_REAL / "kc1-numeric.arff"
FULL_CSV = DATA_REAL / "kc1_full.csv"
SAMPLE_CSV = DATA_REAL / "kc1_sample30.csv"
SAMPLE_SIZE = 30

# Coluna original do ARFF -> nome usado no projeto
COLUMNS = {"sumLOC_TOTAL": "loc", "NUMDEFECTS": "defects"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ensure_arff(path: Path = ARFF_PATH) -> Path:
    """Baixa o ARFF do OpenML se ele não existir e confere o SHA-256."""
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(ARFF_URL, path)
    digest = sha256(path)
    if digest != ARFF_SHA256:
        raise ValueError(f"SHA-256 inesperado para {path}: {digest}")
    return path


def load_kc1(path: Path = ARFF_PATH) -> pd.DataFrame:
    """Lê o ARFF e devolve `class_id`, `loc` e `defects` das 145 classes.

    O ARFF não traz nome nem identificador de classe; `class_id` é a posição
    da linha no arquivo original (0 a 144).
    """
    records, _ = arff.loadarff(path)
    raw = pd.DataFrame(records)
    df = raw[list(COLUMNS)].rename(columns=COLUMNS).astype(int)
    df.insert(0, "class_id", range(len(df)))
    return df


def draw_sample(df: pd.DataFrame, n: int = SAMPLE_SIZE, seed: int = SEED) -> pd.DataFrame:
    """Sorteia `n` classes sem reposição, ordenadas por `class_id`."""
    rng = np.random.default_rng(seed)
    idx = np.sort(rng.choice(len(df), size=n, replace=False))
    return df.iloc[idx].reset_index(drop=True)


def main() -> None:
    full = load_kc1(ensure_arff())
    sample = draw_sample(full)
    full.to_csv(FULL_CSV, index=False)
    sample.to_csv(SAMPLE_CSV, index=False)
    for name, df in (("completo", full), ("amostra", sample)):
        zeros = (df["defects"] == 0).mean()
        print(
            f"{name}: n={len(df)} | LOC mediana={df['loc'].median():.0f} "
            f"| defeitos máx={df['defects'].max()} | classes sem defeito={zeros:.0%}"
        )
    print(f"Salvos em {FULL_CSV.relative_to(DATA_REAL.parents[1])} "
          f"e {SAMPLE_CSV.relative_to(DATA_REAL.parents[1])}")


if __name__ == "__main__":
    main()
