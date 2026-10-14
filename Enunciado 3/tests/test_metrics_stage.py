"""Testa o estágio `metrics` do CLI: geração de dora_c1/c2/c3.csv."""

import csv
import json

from pipeline.cli import DORA_VARIANT_COLUMNS, _dora_to_dict, _run_metrics
from metrics import DORAVariant, classify_dora


def _write_config(tmp_path):
    config = tmp_path / "config.toml"
    config.write_text(
        '[window]\nstart = "2025-10-01"\nend = "2026-09-30"\nweeks = 52.1\n'
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
        assert rows[0]["dora_category"] == "Medium/Low"


def test_dora_to_dict_includes_category_and_variant():
    result = classify_dora(DORAVariant.C1, 0.5, 0.5, 0.1, 0.5, 8.0, 8.0)
    data = _dora_to_dict(result)
    assert data["category"] == "Elite"
    assert data["variant"] == "C1"
