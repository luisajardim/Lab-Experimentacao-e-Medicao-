from __future__ import annotations

import csv
import importlib.util
import math
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))  # agreement importa label_tool da mesma pasta
SPEC = importlib.util.spec_from_file_location("agreement", SCRIPTS_DIR / "agreement.py")
assert SPEC and SPEC.loader
agreement = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = agreement
SPEC.loader.exec_module(agreement)

COLUMNS = [
    "full_name",
    "project_type",
    "delivers_to_user",
    *(f"release_url_{i}" for i in range(1, 6)),
    *(f"corrective_{i}" for i in range(1, 6)),
    "notes",
]


def _row(name: str, project_type: str, delivers: str, corrective: str = "sim") -> dict[str, str]:
    return {
        "full_name": name,
        "project_type": project_type,
        "delivers_to_user": delivers,
        **{f"release_url_{i}": f"https://github.com/{name}/releases/tag/v{i}" for i in range(1, 6)},
        **{f"corrective_{i}": corrective for i in range(1, 6)},
        "notes": "",
    }


def _write(path: Path, rows: list[dict[str, str]]) -> Path:
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    return path


@pytest.mark.parametrize(
    ("kappa", "expected"),
    [
        (-0.1, "pobre"),
        (0.0, "leve"),
        (0.20, "leve"),
        (0.21, "razoável"),
        (0.55, "moderada"),
        (0.80, "substancial"),
        (0.81, "quase perfeita"),
        (1.0, "quase perfeita"),
    ],
)
def test_landis_koch_scale(kappa: float, expected: str) -> None:
    assert agreement.landis_koch(kappa) == expected


def test_fleiss_matches_reference_values() -> None:
    perfect = [("sim", "sim", "sim"), ("não", "não", "não")]
    assert agreement.fleiss(perfect, ["sim", "não"]) == pytest.approx(1.0)

    # Calculado à mão: P̄ = 7/9, P̄e = (5/9)² + (4/9)² = 41/81 -> κ = 22/40.
    mixed = [("sim", "sim", "sim"), ("não", "não", "não"), ("sim", "sim", "não")]
    assert agreement.fleiss(mixed, ["sim", "não"]) == pytest.approx(0.55)


def test_fleiss_without_variation_is_undefined() -> None:
    kappa = agreement.fleiss([("sim", "sim", "sim")] * 3, ["sim", "não"])
    assert math.isnan(kappa)
    assert agreement.landis_koch(kappa).startswith("indefinido")


def test_majority() -> None:
    assert agreement.majority(("sim", "não", "sim")) == "sim"
    assert agreement.majority(("outro", "outro", "outro")) == "outro"
    assert agreement.majority(("sim", "não", "incerto")) is None


def test_parse_decisions_reads_only_decision_table(tmp_path: Path) -> None:
    protocol = tmp_path / "protocol.md"
    protocol.write_text(
        "| Dimensão | Coluna(s) |\n|---|---|\n| tipo | `project_type` |\n\n"
        "| full_name | coluna | decisão | justificativa |\n"
        "|---|---|---|---|\n"
        "| org/a | project_type | ferramenta CLI | binário de terminal |\n"
        "| org/b | `delivers_to_user` | incerto | |\n",
        encoding="utf-8",
    )
    assert agreement.parse_decisions(protocol) == {
        ("org/a", "project_type"): "ferramenta CLI",
        ("org/b", "delivers_to_user"): "incerto",
    }
    assert agreement.parse_decisions(tmp_path / "missing.md") == {}


def test_parse_decisions_rejects_invalid_value(tmp_path: Path) -> None:
    protocol = tmp_path / "protocol.md"
    protocol.write_text(
        "| full_name | coluna | decisão | justificativa |\n|---|---|---|---|\n"
        "| org/a | delivers_to_user | talvez | |\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="decisão inválida"):
        agreement.parse_decisions(protocol)


def test_load_labels_rejects_incomplete_and_mismatched(tmp_path: Path) -> None:
    a = _write(tmp_path / "a.csv", [_row("org/x", "outro", "sim")])
    b = _write(tmp_path / "b.csv", [_row("org/x", "", "sim")])
    c = _write(tmp_path / "c.csv", [_row("org/y", "outro", "sim")])
    with pytest.raises(ValueError) as error:
        agreement.load_labels([a, b, c])
    assert "project_type=''" in str(error.value)
    assert "repositórios diferentes" in str(error.value)


def test_build_consensus_applies_majority_and_meeting_decisions(tmp_path: Path) -> None:
    raters = [
        {"org/x": _row("org/x", "outro", "sim", "sim"), "org/y": _row("org/y", "outro", "sim")},
        {"org/x": _row("org/x", "outro", "não", "não"), "org/y": _row("org/y", "ferramenta CLI", "não")},
        {"org/x": _row("org/x", "outro", "não", "sim"), "org/y": _row("org/y", "aplicação/serviço", "incerto")},
    ]
    decisions = {
        ("org/y", "project_type"): "ferramenta CLI",
        ("org/x", "project_type"): "outro",  # não é empate: ignorada
    }
    result = agreement.build_consensus(raters, decisions)

    x, y = result.rows
    assert x["project_type"] == "outro"
    assert x["delivers_to_user"] == "não"
    assert x["corrective_1"] == "sim"
    assert x["meeting_decisions"] == ""
    assert y["project_type"] == "ferramenta CLI"
    assert y["delivers_to_user"] == ""
    assert y["meeting_decisions"] == "project_type"
    assert y["release_url_1"] == "https://github.com/org/y/releases/tag/v1"

    assert result.pending == [("org/y", "delivers_to_user", ("sim", "não", "incerto"))]
    assert result.unused_decisions == [("org/x", "project_type")]
    assert result.sources[("tipo", "unânime")] == 1
    assert result.sources[("tipo", "reunião")] == 1
    assert result.sources[("entrega", "maioria")] == 1
    assert result.sources[("entrega", "pendente")] == 1
    assert result.sources[("corretiva", "unânime")] == 5
    assert result.sources[("corretiva", "maioria")] == 5


def test_main_writes_consensus_and_report(tmp_path: Path) -> None:
    rows = {
        "A": [_row("org/x", "outro", "sim"), _row("org/y", "outro", "sim", "não")],
        "B": [_row("org/x", "outro", "sim"), _row("org/y", "ferramenta CLI", "não", "não")],
        "C": [_row("org/x", "outro", "não"), _row("org/y", "aplicação/serviço", "não", "sim")],
    }
    labels = [_write(tmp_path / f"labels_{m}.csv", r) for m, r in rows.items()]
    protocol = tmp_path / "protocol.md"
    protocol.write_text("sem decisões ainda\n", encoding="utf-8")
    output = tmp_path / "consensus.csv"
    report = tmp_path / "reports" / "agreement.md"
    arguments = [
        "--labels", *map(str, labels),
        "--protocol", str(protocol),
        "--output", str(output),
        "--report", str(report),
    ]

    assert agreement.main(arguments) == 1  # org/y project_type empatado 1-1-1
    text = report.read_text(encoding="utf-8")
    assert "| tipo | 2 |" in text
    assert "| corretiva | 10 |" in text
    assert "| org/y | project_type | outro, ferramenta CLI, aplicação/serviço |" in text

    protocol.write_text(
        "| full_name | coluna | decisão | justificativa |\n|---|---|---|---|\n"
        "| org/y | project_type | ferramenta CLI | decidido em reunião |\n",
        encoding="utf-8",
    )
    assert agreement.main(arguments) == 0
    with output.open(encoding="utf-8-sig", newline="") as file:
        consensus = list(csv.DictReader(file))
    assert list(consensus[0]) == list(agreement.CONSENSUS_COLUMNS)
    assert [r["project_type"] for r in consensus] == ["outro", "ferramenta CLI"]
    assert [r["delivers_to_user"] for r in consensus] == ["sim", "não"]
    assert consensus[1]["meeting_decisions"] == "project_type"
    assert "Nenhum." in report.read_text(encoding="utf-8")


def test_main_reports_invalid_labels(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    labels = [_write(tmp_path / f"{m}.csv", [_row("org/x", "", "sim")]) for m in "ABC"]
    assert agreement.main(["--labels", *map(str, labels), "--output", str(tmp_path / "o.csv"),
                           "--report", str(tmp_path / "r.md")]) == 2
    assert "inválido" in capsys.readouterr().err
