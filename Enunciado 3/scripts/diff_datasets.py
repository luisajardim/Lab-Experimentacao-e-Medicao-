"""Compara dois datasets CSV (replicação cruzada) e gera ``diff_report.md``.

Uso:
    python scripts/diff_datasets.py esperado.csv obtido.csv
    python scripts/diff_datasets.py esperado.csv obtido.csv --out reports/diff_report.md \
        --issue-out reports/issue_replicacao.md --command "uv run python -m pipeline --stage metrics"

Regras:
- Colunas numéricas: diferença relativa |a-b| / max(|a|,|b|) (0 quando ambos são 0).
- Colunas de classificação DORA (``*_category``): % de linhas com a mesma categoria.
- Linhas são pareadas pela coluna chave (padrão: ``full_name``).
"""

from __future__ import annotations

import argparse
import csv
import statistics
import sys
from datetime import datetime
from pathlib import Path
from string import Template

DEFAULT_KEY = "full_name"
DEFAULT_TOLERANCE = 0.05
CATEGORY_SUFFIX = "_category"
TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "issue_replicacao.md"


def read_csv(path: Path, key: str) -> tuple[list[str], dict[str, dict[str, str]]]:
    """Lê um CSV e indexa as linhas pela coluna chave."""
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = list(reader.fieldnames or [])
        if key not in columns:
            raise SystemExit(f"Erro: coluna chave '{key}' ausente em {path}")
        rows = {row[key]: row for row in reader}
    return columns, rows


def to_float(value: str | None) -> float | None:
    if value is None or value.strip() == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def relative_diff(a: float, b: float) -> float:
    """Diferença relativa |a-b|/max(|a|,|b|); 0 se ambos forem 0."""
    denom = max(abs(a), abs(b))
    return 0.0 if denom == 0 else abs(a - b) / denom


def is_numeric_column(column: str, rows_a: dict, rows_b: dict) -> bool:
    """Coluna é numérica se todos os valores não vazios de ambos os lados forem números."""
    seen = False
    for rows in (rows_a, rows_b):
        for row in rows.values():
            raw = row.get(column, "")
            if raw is None or raw.strip() == "":
                continue
            if to_float(raw) is None:
                return False
            seen = True
    return seen


def compare(
    path_a: Path, path_b: Path, key: str = DEFAULT_KEY, tolerance: float = DEFAULT_TOLERANCE
) -> dict:
    """Compara os datasets e retorna as estatísticas por coluna."""
    cols_a, rows_a = read_csv(path_a, key)
    cols_b, rows_b = read_csv(path_b, key)

    common_keys = sorted(set(rows_a) & set(rows_b))
    common_cols = [c for c in cols_a if c in cols_b and c != key]

    numeric: dict[str, dict] = {}
    categorical: dict[str, dict] = {}
    divergences: list[tuple[float, str, str, str, str]] = []

    for col in common_cols:
        if col.endswith(CATEGORY_SUFFIX):
            same = total = 0
            for k in common_keys:
                va = (rows_a[k].get(col) or "").strip()
                vb = (rows_b[k].get(col) or "").strip()
                total += 1
                same += va == vb
            categorical[col] = {"total": total, "same": same}
        elif is_numeric_column(col, rows_a, rows_b):
            diffs: list[float] = []
            missing_mismatch = 0
            for k in common_keys:
                fa = to_float(rows_a[k].get(col))
                fb = to_float(rows_b[k].get(col))
                if fa is None and fb is None:
                    continue
                if fa is None or fb is None:
                    missing_mismatch += 1
                    continue
                d = relative_diff(fa, fb)
                diffs.append(d)
                if d > tolerance:
                    divergences.append((d, k, col, rows_a[k][col], rows_b[k][col]))
            numeric[col] = {
                "n": len(diffs),
                "missing_mismatch": missing_mismatch,
                "mean": statistics.fmean(diffs) if diffs else None,
                "median": statistics.median(diffs) if diffs else None,
                "max": max(diffs) if diffs else None,
                "within": sum(1 for d in diffs if d <= tolerance),
            }

    divergences.sort(reverse=True)
    return {
        "path_a": path_a,
        "path_b": path_b,
        "key": key,
        "tolerance": tolerance,
        "n_a": len(rows_a),
        "n_b": len(rows_b),
        "n_common": len(common_keys),
        "only_a": sorted(set(rows_a) - set(rows_b)),
        "only_b": sorted(set(rows_b) - set(rows_a)),
        "cols_only_a": [c for c in cols_a if c not in cols_b],
        "cols_only_b": [c for c in cols_b if c not in cols_a],
        "numeric": numeric,
        "categorical": categorical,
        "divergences": divergences,
    }


def _fmt(value: float | None) -> str:
    return "-" if value is None else f"{value:.4f}"


def _pct(part: int, total: int) -> str:
    return "-" if total == 0 else f"{100 * part / total:.1f}%"


def render_report(result: dict, top: int = 20) -> str:
    """Gera o Markdown do relatório de diferenças."""
    tol = result["tolerance"]
    lines = [
        "# Relatório de Diferenças entre Datasets (Replicação Cruzada)",
        "",
        f"- Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Esperado (A): `{result['path_a']}` ({result['n_a']} linhas)",
        f"- Obtido (B): `{result['path_b']}` ({result['n_b']} linhas)",
        f"- Chave de pareamento: `{result['key']}`",
        f"- Linhas em comum: {result['n_common']}",
        f"- Tolerância relativa: {tol:.2%}",
        "",
    ]

    lines += ["## Cobertura", ""]
    lines.append(f"- Apenas em A: {len(result['only_a'])}")
    lines.append(f"- Apenas em B: {len(result['only_b'])}")
    for label, items in (("Apenas em A", result["only_a"]), ("Apenas em B", result["only_b"])):
        if items:
            shown = ", ".join(f"`{i}`" for i in items[:10])
            extra = f" … (+{len(items) - 10})" if len(items) > 10 else ""
            lines.append(f"  - {label}: {shown}{extra}")
    if result["cols_only_a"] or result["cols_only_b"]:
        lines.append(f"- Colunas apenas em A: {', '.join(result['cols_only_a']) or '-'}")
        lines.append(f"- Colunas apenas em B: {', '.join(result['cols_only_b']) or '-'}")
    lines.append("")

    lines += [
        "## Colunas numéricas (diferença relativa |a-b|/max(a,b))",
        "",
        "| Coluna | N | Média | Mediana | Máx | % dentro da tolerância | Ausência divergente |",
        "|---|---|---|---|---|---|---|",
    ]
    for col, s in result["numeric"].items():
        lines.append(
            f"| `{col}` | {s['n']} | {_fmt(s['mean'])} | {_fmt(s['median'])} | {_fmt(s['max'])} "
            f"| {_pct(s['within'], s['n'])} | {s['missing_mismatch']} |"
        )
    if not result["numeric"]:
        lines.append("| _(nenhuma)_ | | | | | | |")
    lines.append("")

    lines += [
        "## Classificação DORA (mesma categoria)",
        "",
        "| Coluna | Total | Iguais | % igual |",
        "|---|---|---|---|",
    ]
    for col, s in result["categorical"].items():
        lines.append(f"| `{col}` | {s['total']} | {s['same']} | {_pct(s['same'], s['total'])} |")
    if not result["categorical"]:
        lines.append("| _(nenhuma)_ | | | |")
    lines.append("")

    div = result["divergences"]
    lines += [f"## Maiores divergências (> {tol:.0%}) — top {min(top, len(div))} de {len(div)}", ""]
    if div:
        lines += ["| Repositório | Coluna | Esperado | Obtido | Dif. relativa |", "|---|---|---|---|---|"]
        for d, k, col, va, vb in div[:top]:
            lines.append(f"| `{k}` | `{col}` | {va} | {vb} | {d:.4f} |")
    else:
        lines.append("Nenhuma divergência acima da tolerância.")
    lines.append("")
    return "\n".join(lines)


def render_issue(result: dict, command: str, error: str) -> str:
    """Preenche o template de Issue de replicação com os resultados da comparação."""
    template = Template(TEMPLATE_PATH.read_text(encoding="utf-8"))
    expected_vs_obtained = []
    for d, k, col, va, vb in result["divergences"][:10]:
        expected_vs_obtained.append(f"| `{k}` | `{col}` | {va} | {vb} | {d:.4f} |")
    table = "\n".join(expected_vs_obtained) or "| _(sem divergências acima da tolerância)_ | | | | |"

    cat_lines = [
        f"- `{col}`: {_pct(s['same'], s['total'])} de mesma categoria"
        for col, s in result["categorical"].items()
    ]
    return template.safe_substitute(
        command=command or "_(informe o comando executado)_",
        error=error or "Nenhum erro.",
        n_common=result["n_common"],
        n_only_a=len(result["only_a"]),
        n_only_b=len(result["only_b"]),
        tolerance=f"{result['tolerance']:.0%}",
        divergence_table=table,
        category_summary="\n".join(cat_lines) or "- (sem colunas de categoria)",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compara dois datasets CSV de métricas DORA.")
    parser.add_argument("expected", type=Path, help="CSV esperado (A)")
    parser.add_argument("obtained", type=Path, help="CSV obtido na replicação (B)")
    parser.add_argument("--key", default=DEFAULT_KEY, help="Coluna chave (padrão: full_name)")
    parser.add_argument("--tolerance", type=float, default=DEFAULT_TOLERANCE,
                        help="Tolerância relativa para divergência (padrão: 0.05)")
    parser.add_argument("--out", type=Path, default=Path("diff_report.md"),
                        help="Arquivo do relatório (padrão: diff_report.md)")
    parser.add_argument("--issue-out", type=Path, default=None,
                        help="Se informado, gera também o rascunho de Issue de replicação")
    parser.add_argument("--command", default="", help="Comando executado (para a Issue)")
    parser.add_argument("--error", default="", help="Mensagem de erro, se houver (para a Issue)")
    parser.add_argument("--top", type=int, default=20, help="Qtde de divergências listadas")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    for path in (args.expected, args.obtained):
        if not path.exists():
            print(f"Erro: arquivo não encontrado: {path}", file=sys.stderr)
            return 1

    result = compare(args.expected, args.obtained, args.key, args.tolerance)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_report(result, args.top), encoding="utf-8")
    print(f"Relatório salvo em {args.out}")

    if args.issue_out:
        args.issue_out.parent.mkdir(parents=True, exist_ok=True)
        args.issue_out.write_text(render_issue(result, args.command, args.error), encoding="utf-8")
        print(f"Rascunho de Issue salvo em {args.issue_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
