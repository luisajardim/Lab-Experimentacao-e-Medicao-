"""Testes da validação e do congelamento do dataset (T13, #110)."""

import json

import pandas as pd
import pytest

import schema
import synthetic
import validate


@pytest.fixture(scope="module")
def full():
    """Desenho completo (3 máquinas × 72 células × 10 reps + 2 aquecimentos) com dados sintéticos."""
    df = synthetic.generate(reps=validate.EXPECTED_REPS)
    df["registry"] = "local"
    return df


def by_name(checks):
    return {c.name: c for c in checks}


def test_complete_design_passes(full):
    checks = by_name(validate.run_checks(full))
    assert checks["Desenho completo"].status == validate.INFO
    assert checks["Registry local"].status == validate.INFO


def test_missing_and_repeated_cells_are_errors(full):
    broken = full.drop(full[~full["warmup"]].index[:3])
    assert validate.check_design(broken).status == validate.ERROR
    dup = full[~full["warmup"]].iloc[[0]].assign(run_id="dup")
    assert validate.check_design(pd.concat([full, dup])).status == validate.ERROR


def test_divergent_version_is_error(full):
    df = full.copy()
    df.loc[df.index[0], "manager_version"] = "0.0.1"
    check = validate.check_versions(df)
    assert check.status == validate.ERROR and check.details


def test_failures_are_reported_not_removed(full):
    df = full.copy()
    df.loc[df.index[5], "exit_code"] = 124
    check = validate.check_failures(df)
    assert check.status == validate.WARNING and "exit_code=124" in check.details[0]


def test_outlier_needs_median_above_one_second():
    base = dict(machine="m", project="express-api", scenario="cold", manager="npm", warmup=False)
    slow = pd.DataFrame([{**base, "rep": i, "wall_s": w} for i, w in enumerate([2, 2, 2, 7], 1)])
    fast = slow.assign(scenario="reinstall", wall_s=[0.1, 0.1, 0.1, 0.9])
    found = validate.outliers(pd.concat([slow, fast]))
    assert list(found["wall_s"]) == [7]


def test_gap_detects_pause():
    ts = ["2026-11-24T14:13:33-03:00", "2026-11-24T14:14:08-03:00", "2026-11-24T14:53:49-03:00"]
    df = pd.DataFrame({"machine": "m", "timestamp": ts, "project": "next-app", "scenario": "ci",
                       "manager": "npm", "rep": [1, 2, 3], "wall_s": [1.0, 1.0, 21.2]})
    found = validate.gaps(df)
    assert len(found) == 1 and found.iloc[0]["minutes"] == pytest.approx(39.7, abs=0.1)
    assert found.iloc[0]["next_wall_s"] == 21.2


def test_freeze_writes_dataset_manifest_and_report(full, tmp_path, monkeypatch):
    raw = tmp_path / "data" / "raw"
    for machine, block in full.groupby("machine"):
        schema.write_runs(block, raw / machine / "runs.csv")
    monkeypatch.setattr(validate, "ROOT", tmp_path)
    monkeypatch.setattr(validate, "RUNS_ALL", tmp_path / "data" / "processed" / "runs_all.csv")
    monkeypatch.setattr(validate, "MANIFEST", tmp_path / "data" / "processed" / "manifest.json")
    monkeypatch.setattr(validate, "REPORT", tmp_path / "docs" / "validacao.md")
    (tmp_path / "docs").mkdir()

    checks, manifest = validate.validate_and_freeze(raw)
    assert not [c for c in checks if c.status == validate.ERROR]
    assert manifest["rows"] == len(full)
    assert len(manifest["sources"]) == full["machine"].nunique()
    assert validate.verify_manifest(validate.MANIFEST) == []
    assert "Desenho completo" in validate.REPORT.read_text(encoding="utf-8")
    assert len(schema.load_dataset(validate.RUNS_ALL)) == (~full["warmup"]).sum()

    with validate.RUNS_ALL.open("a", encoding="utf-8") as fh:
        fh.write("\n")
    assert validate.verify_manifest(validate.MANIFEST) == ["data/processed/runs_all.csv mudou desde a validação"]
    assert json.loads(validate.MANIFEST.read_text())["dataset"] == "data/processed/runs_all.csv"


def test_load_dataset_missing_file_is_empty(tmp_path):
    assert schema.load_dataset(tmp_path / "nada.csv").empty
