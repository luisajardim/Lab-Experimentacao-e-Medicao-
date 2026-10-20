from __future__ import annotations

import pandas as pd

from analysis.bootstrap import bca_interval
from analysis.recovery_survival import episode_frame, fit_survival
from analysis.rq01_rq04 import describe_c1, describe_metrics


def test_bca_interval_is_deterministic_and_uses_requested_resamples():
    values = [1.0, 2.0, 3.0, 4.0, 8.0, 13.0, 21.0, 34.0]
    first = bca_interval(values, n_resamples=200, random_state=7)
    second = bca_interval(values, n_resamples=200, random_state=7)
    assert first == second
    assert first is not None
    assert first.n == len(values)
    assert first.n_resamples == 200
    assert first.low <= 4.0 <= first.high


def test_descriptive_summary_and_c1_keep_missing_categories_explicit():
    frame = pd.DataFrame(
        {
            "deployment_frequency_per_week": [0.5, 1.0, 2.0],
            "lead_time_a_hours": [1.0, 2.0, 3.0],
            "lead_time_b_hours": [2.0, 3.0, 4.0],
            "cfr_a": [0.1, 0.2, 0.3],
            "recovery_hours": [4.0, 5.0, 6.0],
            "censored_proportion": [0.0, 0.0, 0.5],
            "dora_c1_category": ["Elite", "High", None],
        }
    )
    summary = describe_metrics(frame)
    c1 = describe_c1(frame)
    assert set(summary["metric"]) >= {"cfr_a", "recovery_hours"}
    assert summary.loc[summary["metric"] == "cfr_a", "n_repositories"].item() == 3
    assert c1.loc[c1["dora_c1_category"] == "Não classificável", "n_repositories"].item() == 1


def test_survival_uses_censored_episodes():
    episodes = episode_frame(
        [
            {
                "repository": {"full_name": "org/repo"},
                "recovery_episodes": [
                    {"duration_hours": 1.0, "censored": False},
                    {"duration_hours": 4.0, "censored": True},
                ],
            }
        ]
    )
    model = fit_survival(episodes)
    assert len(episodes) == 2
    assert int(model.event_table["observed"].sum()) == 1
