"""Validação e congelamento do dataset da coleta completa (T13, #110).

Junta os `data/raw/<maquina>/runs.csv` das máquinas (sem piloto nem sintético), confere a
qualidade e grava:

- `data/processed/runs_all.csv`: as linhas das 3 máquinas, **com** o aquecimento (coluna
  `warmup`), na ordem de execução de cada bloco;
- `data/processed/manifest.json`: sha256 das fontes e do dataset, contagens e resultado das
  checagens;
- `docs/validacao.md`: o relatório para humanos.

Nada é apagado: falhas de instalação e medições extremas são **registradas**, não removidas
(ameaça C2 em `docs/ameacas.md`). A validação só falha (código de saída 1) com erro de estrutura:
schema, desenho incompleto, versões divergentes ou registry errado.

Uso:
    uv run lab05 validate            # valida e (re)gera dataset, manifesto e relatório
    uv run lab05 validate --check    # só confere se o manifesto bate com os arquivos atuais

Issues: #110 (T13).
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

import schema
from config import (
    DATA_PROCESSED,
    DATA_RAW,
    DEFAULT_REGISTRY,
    DOCS,
    MANAGERS,
    PROJECTS,
    ROOT,
    RUNS_ALL,
    RUNS_FILENAME,
    SCENARIOS,
    SPECS_FILENAME,
)

MANIFEST = DATA_PROCESSED / "manifest.json"
REPORT = DOCS / "validacao.md"

EXPECTED_REPS = 10            # N da análise de poder (T09, docs/poder.md)
EXPECTED_WARMUP = 2           # rodadas de aquecimento por bloco
OUTLIER_FACTOR = 3.0          # "extremo" = mais de 3× a mediana da célula na mesma máquina
OUTLIER_MIN_MEDIAN_S = 1.0    # abaixo de 1 s, 3× é ruído de décimos (reinstall)
GAP_MIN = 5.0                 # lacuna entre dois inícios seguidos que indica pausa/suspensão

ERROR, WARNING, INFO = "erro", "aviso", "ok"


@dataclass
class Check:
    name: str
    status: str               # erro | aviso | ok
    summary: str
    details: list[str] = field(default_factory=list)


def file_sha256(path: Path) -> str:
    """sha256 do arquivo com fim de linha normalizado (o mesmo hash em Windows e Linux)."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def machine_dirs(raw: Path = DATA_RAW) -> list[Path]:
    """Pastas de máquina da coleta completa (sem `synthetic/` nem `pilot/`)."""
    skip = {schema.SYNTHETIC_DIR, schema.PILOT_DIR}
    return sorted(p.parent for p in raw.glob(f"*/{RUNS_FILENAME}") if p.parent.name not in skip)


def load_all(raw: Path = DATA_RAW) -> pd.DataFrame:
    """Todas as linhas das máquinas, com aquecimento, ordenadas por máquina e ordem de execução."""
    df = schema.load_runs(raw, include_warmup=True)
    return df.sort_values(["machine", "order"], kind="stable").reset_index(drop=True)


# --- checagens ----------------------------------------------------------------------------------

def check_design(df: pd.DataFrame, reps: int = EXPECTED_REPS,
                 warmup: int = EXPECTED_WARMUP) -> Check:
    """Cada máquina tem as 72 células × `reps` repetições, cada uma uma vez, e `warmup` rodadas."""
    expected = pd.MultiIndex.from_product(
        [list(PROJECTS), list(SCENARIOS), list(MANAGERS), range(1, reps + 1)],
        names=["project", "scenario", "manager", "rep"])
    details = []
    for machine, block in df.groupby("machine"):
        measured = block[~block["warmup"]]
        counts = measured.groupby(["project", "scenario", "manager", "rep"]).size()
        missing = expected.difference(counts.index)
        extra = counts.index.difference(expected)
        repeated = counts[counts > 1]
        n_warm = int(block["warmup"].sum())
        for label, items in (("faltando", missing), ("fora do desenho", extra),
                             ("repetidas", repeated.index)):
            if len(items):
                details.append(f"`{machine}`: {len(items)} medições {label}, ex.: {list(items[:3])}")
        if n_warm != warmup:
            details.append(f"`{machine}`: {n_warm} rodadas de aquecimento (esperado {warmup})")
    n_cells = len(PROJECTS) * len(SCENARIOS) * len(MANAGERS)
    summary = (f"{df['machine'].nunique()} máquinas × {n_cells} células × {reps} repetições "
               f"+ {warmup} aquecimentos por máquina")
    return Check("Desenho completo", ERROR if details else INFO, summary, details)


def check_versions(df: pd.DataFrame) -> Check:
    """Mesma versão de cada gerenciador e do Node em todas as máquinas."""
    details = []
    for manager, rows in df.groupby("manager"):
        versions = sorted(rows["manager_version"].unique())
        if len(versions) != 1:
            details.append(f"`{manager}`: {versions}")
    nodes = sorted(df["node_version"].unique())
    if len(nodes) != 1:
        details.append(f"Node: {nodes}")
    found = ", ".join(f"{m} {df.loc[df['manager'] == m, 'manager_version'].iloc[0]}"
                      for m in MANAGERS if (df["manager"] == m).any())
    summary = f"Node {nodes[0]}; {found}" if not details else "versões divergentes entre linhas"
    return Check("Versões iguais nas máquinas", ERROR if details else INFO, summary, details)


def check_registry(df: pd.DataFrame) -> Check:
    bad = df[df["registry"] != DEFAULT_REGISTRY]
    details = [f"{len(bad)} linhas com registry {sorted(bad['registry'].unique())}"] if len(bad) else []
    return Check("Registry local", ERROR if details else INFO,
                 f"todas as linhas com registry `{DEFAULT_REGISTRY}`" if not details
                 else "linhas fora do registry local", details)


def check_failures(df: pd.DataFrame) -> Check:
    """Instalações que falharam (resultado à parte; nunca removidas)."""
    failed = df[(df["exit_code"] != 0) | (~df["build_ok"])]
    details = [f"`{r.machine}` {r.project} {r.scenario} {r.manager} rep {r.rep}: "
               f"exit_code={r.exit_code}, build_ok={r.build_ok}" for r in failed.itertuples()]
    return Check("Instalações válidas", WARNING if details else INFO,
                 f"{len(df) - len(failed)} de {len(df)} com `exit_code = 0` e `build_ok`", details)


def check_cold_tree(df: pd.DataFrame) -> Check:
    """`n_files` igual entre máquinas em cada célula (ameaça I1: mesma árvore resolvida)."""
    measured = df[~df["warmup"]]
    per_cell = measured.groupby(["project", "scenario", "manager"])["n_files"].nunique()
    diff = per_cell[per_cell > 1]
    details = [f"{p} {s} {m}" for p, s, m in diff.index]
    return Check("Mesma árvore instalada nas máquinas (I1)", WARNING if details else INFO,
                 f"`n_files` igual entre as máquinas em {len(per_cell) - len(diff)} de "
                 f"{len(per_cell)} células", details)


def outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Medições acima de `OUTLIER_FACTOR` × a mediana da célula na mesma máquina."""
    measured = df[~df["warmup"]].copy()
    keys = ["machine", "project", "scenario", "manager"]
    measured["cell_median"] = measured.groupby(keys)["wall_s"].transform("median")
    mask = ((measured["cell_median"] >= OUTLIER_MIN_MEDIAN_S)
            & (measured["wall_s"] > OUTLIER_FACTOR * measured["cell_median"]))
    return measured[mask]


def check_outliers(df: pd.DataFrame) -> Check:
    found = outliers(df)
    measured = df[~df["warmup"]]
    keys = ["machine", "project", "scenario", "manager"]
    eligible = (measured.groupby(keys)["wall_s"].transform("median") >= OUTLIER_MIN_MEDIAN_S).sum()
    details = [f"`{r.machine}` {r.project} {r.scenario} {r.manager} rep {r.rep}: "
               f"{r.wall_s:.2f} s (mediana {r.cell_median:.2f} s, {r.wall_s / r.cell_median:.1f}×)"
               for r in found.itertuples()]
    return Check("Medições extremas (registradas, mantidas)", WARNING if details else INFO,
                 f"{len(found)} de {eligible} medições em células com mediana ≥ "
                 f"{OUTLIER_MIN_MEDIAN_S:g} s passaram de {OUTLIER_FACTOR:g}× a mediana", details)


def gaps(df: pd.DataFrame) -> pd.DataFrame:
    """Lacunas maiores que `GAP_MIN` entre inícios seguidos no mesmo bloco."""
    rows = []
    for machine, block in df.groupby("machine"):
        start = pd.to_datetime(block["timestamp"], format="ISO8601").reset_index(drop=True)
        ordered = block.reset_index(drop=True).assign(start=start).sort_values("start")
        delta = ordered["start"].diff().dt.total_seconds() / 60
        for idx in delta[delta > GAP_MIN].index:
            pos = ordered.index.get_loc(idx)
            before, after = ordered.iloc[pos - 1], ordered.iloc[pos]
            rows.append({"machine": machine, "minutes": float(delta[idx]),
                         "before": before["timestamp"], "after": after["timestamp"],
                         "next_cell": f"{after['project']} {after['scenario']} {after['manager']} "
                                      f"rep {after['rep']}",
                         "next_wall_s": float(after["wall_s"])})
    return pd.DataFrame(rows)


def check_gaps(df: pd.DataFrame) -> Check:
    found = gaps(df)
    details = [f"`{g.machine}`: {g.minutes:.1f} min entre {g.before} e {g.after}; a medição "
               f"seguinte ({g.next_cell}) levou {g.next_wall_s:.2f} s"
               for g in found.itertuples()]
    return Check("Pausas durante a coleta", WARNING if details else INFO,
                 f"{len(found)} lacuna(s) de mais de {GAP_MIN:g} min entre duas medições seguidas",
                 details)


def run_checks(df: pd.DataFrame) -> list[Check]:
    return [check_design(df), check_versions(df), check_registry(df), check_failures(df),
            check_cold_tree(df), check_outliers(df), check_gaps(df)]


# --- saídas -------------------------------------------------------------------------------------

def machine_summary(df: pd.DataFrame, dirs: list[Path]) -> list[dict]:
    rows = []
    for d in dirs:
        block = df[df["machine"] == d.name]
        specs_path = d / SPECS_FILENAME
        specs = json.loads(specs_path.read_text(encoding="utf-8")) if specs_path.exists() else {}
        rows.append({
            "machine": d.name,
            "rows": int(len(block)),
            "start": block["timestamp"].min(),
            "end": block["timestamp"].max(),
            "cpu": specs.get("cpu", {}).get("model", ""),
            "ram_gb": specs.get("ram", {}).get("total_gb"),
            "ram_free_gb": specs.get("ram", {}).get("available_gb"),
            "os_build": specs.get("os", {}).get("build", ""),
            "power_plan": specs.get("checklist", {}).get("power_plan", ""),
            "disk": specs.get("disk", {}).get("media_type", ""),
        })
    return rows


def build_manifest(df: pd.DataFrame, dirs: list[Path], checks: list[Check]) -> dict:
    sources = {}
    for d in dirs:
        for name in (RUNS_FILENAME, SPECS_FILENAME):
            if (d / name).exists():
                sources[_rel(d / name)] = file_sha256(d / name)
    return {
        "dataset": _rel(RUNS_ALL),
        "sha256": file_sha256(RUNS_ALL),
        "rows": int(len(df)),
        "measured_rows": int((~df["warmup"]).sum()),
        "machines": sorted(df["machine"].unique().tolist()),
        "sources": sources,
        "checks": [{"name": c.name, "status": c.status, "summary": c.summary} for c in checks],
    }


def render_report(df: pd.DataFrame, dirs: list[Path], checks: list[Check], manifest: dict) -> str:
    status_label = {INFO: "ok", WARNING: "aviso", ERROR: "**erro**"}
    lines = [
        "# Validação da coleta completa (T13, #110)",
        "",
        "Gerado por `uv run lab05 validate` (`src/validate.py`). Não edite à mão.",
        "",
        f"Dataset congelado: `{manifest['dataset']}`, {manifest['rows']} linhas "
        f"({manifest['measured_rows']} medidas e {manifest['rows'] - manifest['measured_rows']} "
        f"de aquecimento), sha256 `{manifest['sha256']}`. Os hashes das fontes estão em "
        f"`{_rel(MANIFEST)}`; `uv run lab05 validate --check` confere se nada mudou.",
        "",
        "Nenhuma linha foi removida. Falhas e medições extremas ficam no dataset e são só "
        "registradas aqui (ver C2 em `ameacas.md`).",
        "",
        "## Máquinas",
        "",
        "| Máquina | Linhas | Início | Fim | CPU | RAM (livre no início) | Build | Energia | Disco |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for m in machine_summary(df, dirs):
        lines.append(f"| `{m['machine']}` | {m['rows']} | {m['start']} | {m['end']} | {m['cpu']} | "
                     f"{m['ram_gb']} GB ({m['ram_free_gb']} GB) | {m['os_build']} | "
                     f"{m['power_plan']} | {m['disk']} |")
    lines += ["", "## Checagens", "", "| Checagem | Situação | Resultado |", "|---|---|---|"]
    for c in checks:
        lines.append(f"| {c.name} | {status_label[c.status]} | {c.summary} |")
    for c in checks:
        if c.details:
            lines += ["", f"### {c.name}", ""] + [f"- {d}" for d in c.details]
    return "\n".join(lines) + "\n"


def verify_manifest(manifest_path: Path = MANIFEST) -> list[str]:
    """Diferenças entre o manifesto e os arquivos atuais (vazio = tudo bate)."""
    if not manifest_path.exists():
        return [f"{_rel(manifest_path)} não existe; rode `uv run lab05 validate`"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    problems = []
    for rel, digest in {manifest["dataset"]: manifest["sha256"], **manifest["sources"]}.items():
        path = ROOT / rel
        if not path.exists():
            problems.append(f"{rel} não existe")
        elif file_sha256(path) != digest:
            problems.append(f"{rel} mudou desde a validação")
    return problems


def validate_and_freeze(raw: Path = DATA_RAW) -> tuple[list[Check], dict]:
    dirs = machine_dirs(raw)
    if not dirs:
        raise SystemExit("[lab05] nenhuma coleta em data/raw/<maquina>/runs.csv")
    df = load_all(raw)
    checks = run_checks(df)
    schema.write_runs(df, RUNS_ALL)
    manifest = build_manifest(df, dirs, checks)
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(render_report(df, dirs, checks, manifest), encoding="utf-8")
    return checks, manifest


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Valida e congela o dataset da coleta (T13).")
    parser.add_argument("--check", action="store_true",
                        help="só confere se o manifesto bate com os arquivos atuais")
    args = parser.parse_args(argv)
    if args.check:
        problems = verify_manifest()
        for p in problems:
            print(f"[lab05] {p}")
        print("[lab05] manifesto confere" if not problems else "[lab05] manifesto NÃO confere")
        raise SystemExit(1 if problems else 0)

    checks, manifest = validate_and_freeze()
    for c in checks:
        print(f"[{c.status:>5}] {c.name}: {c.summary}")
        for d in c.details:
            print(f"        - {d}")
    print(f"[lab05] {manifest['rows']} linhas em {manifest['dataset']} "
          f"(sha256 {manifest['sha256'][:12]}…); relatório em {_rel(REPORT)}")
    if any(c.status == ERROR for c in checks):
        raise SystemExit(1)

