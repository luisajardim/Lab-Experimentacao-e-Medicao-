import pandas as pd
import pytest

from analysis.rq05_spearman import spearman_with_ci, summarize


def test_spearman_with_ci_monotone():
    stats = spearman_with_ci([1, 2, 3, 4, 5, 6, 7, 8], [0.1, 0.2, 0.25, 0.3, 0.5, 0.6, 0.8, 0.9])
    assert stats["n"] == 8
    assert stats["rho"] == pytest.approx(1.0)
    assert stats["p_value"] < 0.001


def test_spearman_with_ci_drops_missing_and_handles_small_n():
    assert spearman_with_ci([1, 2, None], [0.1, None, 0.3])["rho"] is None
    stats = spearman_with_ci([1, 2, 3, 4, 5, None], [5, 4, 3, 2, 1, 0])
    assert stats["n"] == 5
    assert stats["rho"] == pytest.approx(-1.0)


def test_summarize_reports_both_variants():
    merged = pd.DataFrame(
        {
            "deployment_frequency_per_week": [0.1, 0.5, 1, 2, 4, 8],
            "cfr_a": [0.3, 0.1, 0.2, 0.05, 0.4, 0.1],
            "cfr_b": [0.0, 0.1, 0.3, 0.4, 0.6, 0.9],
        }
    )
    summary = summarize(merged)
    assert list(summary["variant"]) == ["a", "b"]
    assert summary.loc[1, "rho"] == pytest.approx(1.0)
    assert {"n", "rho", "p_value", "ci_low", "ci_high"} <= set(summary.columns)
