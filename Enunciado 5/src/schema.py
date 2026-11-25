"""Schema de `runs.csv`: o contrato de dados entre coleta, validação, análise e dashboard.

Cada linha é **uma instalação medida**: um gerenciador, num cenário, num projeto, numa
máquina (bloco), numa repetição. O runner (T04, #99) escreve neste formato; a validação
(T13, #110), a estatística (T08, #103) e o dashboard (T10, #105) leem com `load_runs`.
Documentação para humanos em `docs/schema.md`.

Issues: #96 (T01).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from config import DATA_RAW, MANAGERS, PROJECTS, REGISTRIES, RUNS_ALL, RUNS_FILENAME, SCENARIOS


@dataclass(frozen=True)
class Column:
    name: str
    dtype: str          # dtype do pandas
    scale: str          # escala de medida (teoria de medição)
    description: str


COLUMNS: tuple[Column, ...] = (
    Column("machine", "string", "nominal", "Bloco: identificador da máquina (ex.: bernardo)"),
    Column("run_id", "string", "nominal", "Identificador único da instalação"),
    Column("timestamp", "string", "intervalar", "Início da instalação, ISO 8601 com fuso"),
    Column("project", "string", "nominal", "Projeto-carga (config.PROJECTS)"),
    Column("scenario", "string", "nominal", "Cenário de instalação (config.SCENARIOS)"),
    Column("manager", "string", "nominal", "Tratamento (config.MANAGERS)"),
    Column("manager_version", "string", "nominal", "Versão exata do gerenciador"),
    Column("node_version", "string", "nominal", "Versão exata do Node.js"),
    Column("registry", "string", "nominal", "local (Verdaccio) ou public"),
    Column("rep", "int64", "ordinal", "Repetição (1..N) da célula"),
    Column("order", "int64", "ordinal", "Posição na sequência aleatorizada do bloco"),
    Column("warmup", "bool", "nominal", "Rodada de aquecimento (descartada na análise)"),
    Column("wall_s", "float64", "razão", "Tempo de relógio da instalação (s)"),
    Column("cpu_s", "float64", "razão", "Tempo de CPU (usuário + sistema) da árvore de processos (s)"),
    Column("peak_rss_mb", "float64", "razão", "Pico de memória residente da árvore de processos (MB)"),
    Column("disk_mb", "float64", "razão",
           "Disco dos artefatos da instalação no projeto: node_modules, .pnp.*, .yarn/* (MB)"),
    Column("cache_mb", "float64", "razão",
           "Disco do cache/store sem os arquivos já contados no projeto (MB); "
           "disk_mb + cache_mb = pegada total"),
    Column("n_files", "int64", "razão", "Nº de arquivos criados no projeto"),
    Column("build_ok", "bool", "nominal", "O `build` do projeto passou após a instalação"),
    Column("exit_code", "int64", "nominal", "Código de saída da instalação (124 = timeout)"),
)

COLUMN_NAMES: tuple[str, ...] = tuple(c.name for c in COLUMNS)
DTYPES: dict[str, str] = {c.name: c.dtype for c in COLUMNS}

ALLOWED_VALUES: dict[str, tuple[str, ...]] = {
    "manager": tuple(MANAGERS),
    "scenario": tuple(SCENARIOS),
    "project": tuple(PROJECTS),
    "registry": REGISTRIES,
}
NON_NEGATIVE = ("wall_s", "cpu_s", "peak_rss_mb", "disk_mb", "cache_mb", "n_files")


class SchemaError(ValueError):
    """O DataFrame não segue o schema de `runs.csv`."""


def validate(df: pd.DataFrame) -> pd.DataFrame:
    """Confere colunas, tipos e valores; devolve o DataFrame com os dtypes do schema.

    Levanta `SchemaError` com todos os problemas encontrados de uma vez.
    """
    problems: list[str] = []
    missing = [c for c in COLUMN_NAMES if c not in df.columns]
    extra = [c for c in df.columns if c not in COLUMN_NAMES]
    if missing:
        problems.append(f"colunas faltando: {missing}")
    if extra:
        problems.append(f"colunas a mais: {extra}")
    if problems:
        raise SchemaError("; ".join(problems))

    try:
        out = df[list(COLUMN_NAMES)].astype(DTYPES)
    except (ValueError, TypeError) as exc:
        raise SchemaError(f"tipo inválido: {exc}") from exc

    for col, allowed in ALLOWED_VALUES.items():
        bad = sorted(set(out[col].dropna()) - set(allowed))
        if bad:
            problems.append(f"{col} com valores fora do permitido: {bad}")
    for col in NON_NEGATIVE:
        if (out[col] < 0).any():
            problems.append(f"{col} com valores negativos")
    required = ["machine", "run_id", "project", "scenario", "manager", "rep", "wall_s"]
    for col in required:
        if out[col].isna().any():
            problems.append(f"{col} com valores vazios")
    if out["run_id"].duplicated().any():
        problems.append("run_id duplicado")
    if problems:
        raise SchemaError("; ".join(problems))
    return out


def empty_frame() -> pd.DataFrame:
    """DataFrame vazio com as colunas e os tipos do schema."""
    return pd.DataFrame({c: pd.Series(dtype=t) for c, t in DTYPES.items()})


def read_runs(path: Path) -> pd.DataFrame:
    """Lê e valida um `runs.csv`."""
    return validate(pd.read_csv(path, dtype={"manager_version": "string", "node_version": "string"}))


def write_runs(df: pd.DataFrame, path: Path) -> Path:
    """Valida e grava um `runs.csv` (cria a pasta se preciso)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    validate(df).to_csv(path, index=False)
    return path


SYNTHETIC_DIR = "synthetic"   # números inventados, só para desenvolver (T01)
PILOT_DIR = "pilot"           # coleta piloto (T05): outros cenários e N, não entra na análise


def load_runs(root: Path = DATA_RAW, include_synthetic: bool = False,
              include_pilot: bool = False, include_warmup: bool = False) -> pd.DataFrame:
    """Junta os `data/raw/<maquina>/runs.csv` da coleta completa.

    Por padrão ignora o CSV sintético (`synthetic/`), o piloto (`pilot/`) e as rodadas de
    aquecimento: o piloto roda na mesma máquina de um dos blocos, com outros cenários e outro N, e
    misturá-lo à coleta duplicaria repetições. Use `include_synthetic=True` ou `include_pilot=True`
    para desenvolver antes da coleta completa.
    """
    skip = {name for name, keep in ((SYNTHETIC_DIR, include_synthetic),
                                    (PILOT_DIR, include_pilot)) if not keep}
    frames = [read_runs(path) for path in sorted(root.glob(f"*/{RUNS_FILENAME}"))
              if path.parent.name not in skip]
    if not frames:
        return empty_frame()
    df = validate(pd.concat(frames, ignore_index=True))
    if not include_warmup:
        df = df[~df["warmup"]].reset_index(drop=True)
    return df


def load_dataset(path: Path = RUNS_ALL, include_warmup: bool = False) -> pd.DataFrame:
    """Dataset congelado pela validação (T13, #110); vazio se ainda não existe.

    É o que a análise e o dashboard leem. `uv run lab05 validate` o gera a partir de `load_runs`.
    """
    if not path.exists():
        return empty_frame()
    df = read_runs(path)
    if not include_warmup:
        df = df[~df["warmup"]].reset_index(drop=True)
    return df
