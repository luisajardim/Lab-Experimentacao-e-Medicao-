import json
from pathlib import Path

import pandas as pd
import pytest

from analysis.rq08_bonus import (
    is_release_corrective,
    main,
    process_repository,
    run_mann_kendall,
)
from metrics.cfr_release import DEFAULT_KEYWORDS, keyword_pattern


def test_mann_kendall_detects_significant_trends():
    inc = [1, 3, 5, 8, 12, 17, 25, 33, 45, 60]
    res_inc = run_mann_kendall(inc)
    assert res_inc.trend == "increasing"
    assert res_inc.p_value < 0.05

    dec = list(reversed(inc))
    res_dec = run_mann_kendall(dec)
    assert res_dec.trend == "decreasing"
    assert res_dec.p_value < 0.05


def test_mann_kendall_handles_flat_or_short_series():
    flat = [5, 5, 5, 5]
    res_flat = run_mann_kendall(flat)
    assert res_flat.trend == "negligible"

    short = [1, 2]
    res_short = run_mann_kendall(short)
    assert res_short.trend == "negligible"


def test_is_release_corrective():
    pattern = keyword_pattern(DEFAULT_KEYWORDS, whole_word=True)
    payload = {
        "releases": [
            {"tag_name": "v1.0.0", "html_url": "u1", "published_at": "2025-10-01T00:00:00Z"},
            {"tag_name": "v1.0.1", "html_url": "u2", "published_at": "2025-10-05T00:00:00Z"},
            {"tag_name": "v1.1.0", "html_url": "u3", "published_at": "2025-10-10T00:00:00Z"},
        ],
        "commits_between": [
            {"release": "v1.0.1", "commits": [{"commit": {"message": "fix: critical bug"}}]},
            {"release": "v1.1.0", "commits": [{"commit": {"message": "feat: new feature"}}]},
        ],
    }

    # v1.0.1 é patch bump e tem commit com fix -> corretiva
    assert is_release_corrective(payload, payload["releases"][1], pattern) is True
    # v1.1.0 é minor bump e commit feat -> não corretiva
    assert is_release_corrective(payload, payload["releases"][2], pattern) is False


def test_process_repository_computes_rework_and_quarterly():
    pattern = keyword_pattern(DEFAULT_KEYWORDS, whole_word=True)
    payload = {
        "repository": {"full_name": "owner/repo"},
        "releases": [
            {"tag_name": "v1.0.0", "html_url": "u1", "published_at": "2025-10-10T00:00:00Z"},
            {"tag_name": "v1.0.1", "html_url": "u2", "published_at": "2025-11-10T00:00:00Z"},
            {"tag_name": "v1.0.2", "html_url": "u3", "published_at": "2026-02-10T00:00:00Z"},
        ],
        "commits_between": [
            {"release": "v1.0.1", "commits": [{"commit": {"message": "fix: bug"}}]},
            {"release": "v1.0.2", "commits": [{"commit": {"message": "fix: patch"}}]},
        ],
        "runs_by_month": {
            "2025-10": [{"conclusion": "success"}, {"conclusion": "failure"}],
            "2025-11": [{"conclusion": "success"}],
        },
    }

    res = process_repository("owner/repo", payload, pattern)
    assert res["full_name"] == "owner/repo"
    assert res["total_releases_window"] == 3
    # v1.0.1 e v1.0.2 são corretivas
    assert res["corrective_releases_window"] == 2
    assert res["rework_rate_window"] == pytest.approx(2 / 3)
    assert res["q1_releases"] == 2  # 2025-10 e 2025-11
    assert res["q2_releases"] == 1  # 2026-02
    assert res["q3_releases"] == 0
    assert res["deploy_trend_quarterly"] in ("increasing", "decreasing", "negligible")


def test_main_generates_all_output_csvs(tmp_path: Path):
    gold_dir = tmp_path / "gold"
    (gold_dir / "owner").mkdir(parents=True)
    repo_json = gold_dir / "owner" / "test-repo.json"
    repo_payload = {
        "repository": {"full_name": "owner/test-repo"},
        "releases": [
            {"tag_name": "v1.0.0", "html_url": "u1", "published_at": "2025-10-10T00:00:00Z"},
            {"tag_name": "v1.0.1", "html_url": "u2", "published_at": "2025-11-10T00:00:00Z"},
        ],
        "runs_by_month": {},
    }
    repo_json.write_text(json.dumps(repo_payload), encoding="utf-8")

    metrics_csv = tmp_path / "metrics.csv"
    pd.DataFrame([{
        "full_name": "owner/test-repo",
        "cfr_a": 0.05,
        "stars": 100,
        "language": "Python",
    }]).to_csv(metrics_csv, index=False)

    out_dir = tmp_path / "output"
    argv = [
        "--metrics", str(metrics_csv),
        "--gold-dir", str(gold_dir),
        "--output-dir", str(out_dir),
    ]

    assert main(argv) == 0
    assert (out_dir / "rq08_rework_rate.csv").exists()
    assert (out_dir / "rq08_temporal_trend.csv").exists()
    assert (out_dir / "rq08_summary.csv").exists()
    assert (out_dir / "rq08_bonus.md").exists()
