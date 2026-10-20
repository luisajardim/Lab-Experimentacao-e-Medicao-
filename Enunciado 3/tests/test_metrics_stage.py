"""Testa o estágio `metrics` do CLI: geração de dora_c1/c2/c3.csv."""

import csv
import json

from types import SimpleNamespace

from pipeline.cli import (
    DORA_VARIANT_COLUMNS,
    _commit_scope,
    _dora_to_dict,
    _in_window,
    _paired,
    _run_metrics,
    write_funnel_report,
)
from metrics import DORAVariant, classify_dora


def _write_config(tmp_path):
    config = tmp_path / "config.toml"
    config.write_text(
        '[window]\nstart = "2025-10-01"\nend = "2026-09-30"\nweeks = 52.1\n'
        '[filters]\nmin_releases = 2\nmin_workflow_runs = 3\n'
        '[paths]\ngold_dir = "gold"\ndatasets_dir = "datasets"\n',
        encoding="utf-8",
    )
    return config


def _write_repo(tmp_path):
    repo_dir = tmp_path / "gold" / "owner"
    repo_dir.mkdir(parents=True)
    runs = [
        {"workflow_id": 1, "conclusion": "success",
         "run_started_at": "2025-11-01T10:00:00Z", "updated_at": "2025-11-01T10:10:00Z"},
        {"workflow_id": 1, "conclusion": "failure",
         "run_started_at": "2025-11-02T10:00:00Z", "updated_at": "2025-11-02T10:10:00Z"},
        {"workflow_id": 1, "conclusion": "success",
         "run_started_at": "2025-11-02T12:00:00Z", "updated_at": "2025-11-02T12:10:00Z"},
    ]
    data = {
        "repository": {"full_name": "owner/repo", "stars": 1500, "language": "Python"},
        "releases": [
            {"tag_name": "v1", "published_at": "2025-10-10T00:00:00Z", "draft": False},
            {"tag_name": "v2", "published_at": "2025-11-10T00:00:00Z", "draft": False},
        ],
        "tags": [],
        "commits_between": [
            {"release": "v1", "ignored_reason": "no_previous_release", "commits": None},
            {"release": "v2", "ignored_reason": None,
             "commits": [{"author_date": "2025-11-09T00:00:00Z"}]},
        ],
        "runs_by_month": {"2025-11": runs},
    }
    (repo_dir / "repo.json").write_text(json.dumps(data), encoding="utf-8")


def test_metrics_stage_generates_one_csv_per_variant(tmp_path):
    config = _write_config(tmp_path)
    _write_repo(tmp_path)

    assert _run_metrics(str(config)) == 0

    for variant in ("c1", "c2", "c3"):
        path = tmp_path / "datasets" / f"dora_{variant}.csv"
        assert path.exists()
        with open(path, newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            assert reader.fieldnames == DORA_VARIANT_COLUMNS
            rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["full_name"] == "owner/repo"
        assert rows[0]["dora_category"] == "Medium"


def test_dora_to_dict_includes_category_and_variant():
    result = classify_dora(DORAVariant.C1, 0.5, 0.5, 0.1, 0.5, 8.0, 8.0)
    data = _dora_to_dict(result)
    assert data["category"] == "Elite"
    assert data["variant"] == "C1"


def test_in_window_is_inclusive_and_handles_none():
    assert _in_window("2025-10-01T00:00:00Z", "2025-10-01", "2026-09-30")
    assert _in_window("2026-09-30T23:59:59Z", "2025-10-01", "2026-09-30")
    assert not _in_window("2025-09-30T23:59:59Z", "2025-10-01", "2026-09-30")
    assert not _in_window("2026-10-01T00:00:00Z", "2025-10-01", "2026-09-30")
    assert not _in_window(None, "2025-10-01", "2026-09-30")


def test_commit_scope_keeps_previous_release_outside_window():
    dates = ["2025-08-01", "2025-09-15", "2025-10-10", "2025-12-01", "2026-10-05"]
    releases = [SimpleNamespace(published_at=f"{d}T00:00:00Z") for d in dates]
    scope = _commit_scope(releases, "2025-10-01", "2026-09-30")
    assert [r.published_at[:10] for r in scope] == ["2025-09-15", "2025-10-10", "2025-12-01"]
    assert _commit_scope([], "2025-10-01", "2026-09-30") == []


def test_paired_keeps_same_repo_and_drops_missing():
    rows = [
        {"x": 1.0, "y": 10.0},
        {"x": None, "y": 20.0},
        {"x": 3.0, "y": None},
        {"x": 4.0, "y": 40.0},
    ]
    assert _paired(rows, "x", "y") == ([1.0, 4.0], [10.0, 40.0])


def test_metrics_stage_discards_repo_with_releases_outside_window(tmp_path):
    config = _write_config(tmp_path)
    _write_repo(tmp_path)
    path = tmp_path / "gold" / "owner" / "repo.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["releases"][1]["published_at"] = "2024-01-01T00:00:00Z"  # fora da janela
    path.write_text(json.dumps(data), encoding="utf-8")

    assert _run_metrics(str(config)) == 0

    with open(tmp_path / "datasets" / "dora_c1.csv", newline="", encoding="utf-8") as handle:
        assert list(csv.DictReader(handle)) == []


def test_metrics_stage_discards_prereleases_from_principal_definition(tmp_path):
    config = _write_config(tmp_path)
    _write_repo(tmp_path)
    path = tmp_path / "gold" / "owner" / "repo.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["releases"][1]["prerelease"] = True
    path.write_text(json.dumps(data), encoding="utf-8")

    assert _run_metrics(str(config)) == 0

    with open(tmp_path / "datasets" / "dora_c1.csv", newline="", encoding="utf-8") as handle:
        assert list(csv.DictReader(handle)) == []


def test_metrics_stage_keeps_censored_episodes_for_survival(tmp_path):
    config = _write_config(tmp_path)
    _write_repo(tmp_path)
    path = tmp_path / "gold" / "owner" / "repo.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["runs_by_month"]["2025-11"][2]["conclusion"] = "failure"
    path.write_text(json.dumps(data), encoding="utf-8")

    assert _run_metrics(str(config)) == 0

    with open(tmp_path / "datasets" / "metrics.csv", newline="", encoding="utf-8") as handle:
        row = next(csv.DictReader(handle))
    assert row["survival_n_censored"] == "1"


def test_metrics_stage_uses_only_the_versioned_manifest(tmp_path):
    config = _write_config(tmp_path)
    config.write_text(
        config.read_text(encoding="utf-8").replace(
            'datasets_dir = "datasets"',
            'datasets_dir = "datasets"\ncandidate_manifest_csv = "raw/manifest.csv"',
        ),
        encoding="utf-8",
    )
    _write_repo(tmp_path)
    manifest = tmp_path / "raw" / "manifest.csv"
    manifest.parent.mkdir()
    manifest.write_text(
        "full_name,stars,language,default_branch,created_at\nother/repo,1,,,\n",
        encoding="utf-8",
    )

    assert _run_metrics(str(config)) == 0

    assert not (tmp_path / "datasets" / "metrics.csv").exists()


def test_write_funnel_report_generates_markdown_table(tmp_path):
    report_file = tmp_path / "reports" / "funnel.md"
    write_funnel_report(
        report_file,
        total_candidates=1000,
        few_releases=200,
        no_actions=300,
        few_runs=100,
        final_sample=400,
    )

    assert report_file.exists()
    content = report_file.read_text(encoding="utf-8")
    assert "1000" in content
    assert "800" in content
    assert "500" in content
    assert "400" in content
    assert "| **1. Candidatos Iniciais**" in content
    assert "| **5. Amostra Final**" in content
