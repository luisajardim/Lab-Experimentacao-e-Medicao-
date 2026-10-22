import pandas as pd
import pytest

from analysis.rq07_sensitivity import (
    compare_all,
    compare_pair,
    distribution,
    landis_koch,
    main,
    transition_matrix,
)


def _frame(c1, c2, c3):
    return pd.DataFrame(
        {
            "full_name": [f"o/r{i}" for i in range(len(c1))],
            "dora_c1_category": c1,
            "dora_c2_category": c2,
            "dora_c3_category": c3,
        }
    )


def test_identical_classifications_have_perfect_agreement():
    cats = ["Elite", "High", "Medium", "Low", "High"]
    result = compare_pair(_frame(cats, cats, cats), "C1", "C2")
    assert result.n_changed == 0
    assert result.pct_changed == 0
    assert result.kappa_linear == pytest.approx(1.0)
    assert result.interpretation == "quase perfeita"


def test_counts_changes_direction_and_jumps():
    c1 = ["Elite", "High", "Medium", "Low"]
    c2 = ["High", "High", "Elite", "Medium"]  # down 1, same, up 2, up 1
    result = compare_pair(_frame(c1, c2, c1), "C1", "C2")
    assert result.n_compared == 4
    assert result.n_changed == 3
    assert result.pct_changed == pytest.approx(0.75)
    assert result.n_down == 1
    assert result.n_up == 2
    assert result.n_jump_2plus == 1


def test_unclassifiable_rows_are_excluded_from_pair():
    c1 = ["Elite", None, "Medium", "", "High"]
    c2 = ["Elite", "High", None, "Low", "High"]
    result = compare_pair(_frame(c1, c2, c1), "C1", "C2")
    assert result.n_total == 5
    assert result.n_compared == 2
    assert result.n_excluded == 3


def test_linear_weights_penalize_far_disagreements_more():
    base = ["Elite", "High", "Medium", "Low"] * 5
    near = ["High", "High", "Medium", "Low"] * 5  # Elite -> High
    far = ["Low", "High", "Medium", "Low"] * 5  # Elite -> Low
    k_near = compare_pair(_frame(base, near, far), "C1", "C2").kappa_linear
    k_far = compare_pair(_frame(base, near, far), "C1", "C3").kappa_linear
    assert k_near > k_far


def test_transition_matrix_is_always_4x4_in_order():
    matrix = transition_matrix(pd.Series(["High"]), pd.Series(["Low"]))
    assert list(matrix.index) == ["Elite", "High", "Medium", "Low"]
    assert list(matrix.columns) == ["Elite", "High", "Medium", "Low"]
    assert matrix.loc["High", "Low"] == 1
    assert int(matrix.values.sum()) == 1


def test_compare_all_returns_three_pairs():
    cats = ["Elite", "High", "Medium", "Low"]
    pairs = [(r.first, r.second) for r in compare_all(_frame(cats, cats, cats))]
    assert pairs == [("C1", "C2"), ("C1", "C3"), ("C2", "C3")]


def test_distribution_keeps_unclassifiable():
    dist = distribution(_frame(["Elite", None], ["High", "High"], ["Low", "Bogus"]))
    assert dist.loc["Não classificável", "C1"] == 1
    assert dist.loc["High", "C2"] == 2
    assert dist.loc["Não classificável", "C3"] == 1


@pytest.mark.parametrize(
    ("kappa", "label"),
    [(-0.1, "pobre"), (0.1, "leve"), (0.3, "razoável"), (0.5, "moderada"),
     (0.7, "substancial"), (0.9, "quase perfeita"), (None, "indisponível")],
)
def test_landis_koch(kappa, label):
    assert landis_koch(kappa) == label


def test_main_writes_outputs(tmp_path):
    cats = ["Elite", "High", "Medium", "Low", "High", "Medium"]
    source = tmp_path / "metrics.csv"
    _frame(cats, list(reversed(cats)), cats).to_csv(source, index=False)
    out = tmp_path / "out"
    assert main(["--metrics", str(source), "--output-dir", str(out)]) == 0
    assert (out / "rq07_sensitivity.md").exists()
    assert len(pd.read_csv(out / "rq07_sensitivity.csv")) == 3
    for pair in ("c1_c2", "c1_c3", "c2_c3"):
        assert (out / f"rq07_transition_{pair}.csv").exists()
