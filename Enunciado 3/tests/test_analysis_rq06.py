import json
from itertools import product

import numpy as np
import pandas as pd
import pytest

from analysis.rq06_kruskal import (
    cliffs_delta,
    compare,
    delta_magnitude,
    dunn,
    epsilon_magnitude,
    epsilon_squared,
    main,
)


def test_cliffs_delta_matches_definition():
    x, y = [1, 2, 3, 3, 8], [2, 3, 4, 5]
    brute = (sum(a > b for a, b in product(x, y)) - sum(a < b for a, b in product(x, y))) / (
        len(x) * len(y)
    )
    assert cliffs_delta(x, y) == pytest.approx(brute)
    assert cliffs_delta([5, 6], [1, 2]) == pytest.approx(1.0)


@pytest.mark.parametrize(
    ("delta", "label"),
    [(0.1, "desprezível"), (-0.2, "pequeno"), (0.33, "médio"), (-0.474, "grande")],
)
def test_delta_magnitude_romano(delta, label):
    assert delta_magnitude(delta) == label


@pytest.mark.parametrize(
    ("epsilon", "label"),
    [(0.005, "desprezível"), (0.02, "fraco"), (0.1, "moderado"), (0.2, "relativamente forte"),
     (0.5, "forte"), (0.7, "muito forte")],
)
def test_epsilon_magnitude(epsilon, label):
    assert epsilon_magnitude(epsilon) == label


def test_epsilon_squared():
    assert epsilon_squared(9.0, 10) == pytest.approx(1.0)


def test_dunn_z_by_hand():
    # sem empates: ranks 1..6; médias A=2, B=5; sigma² = 6·7/12 = 3,5
    rows = dunn({"A": np.array([1.0, 2, 3]), "B": np.array([4.0, 5, 6])})
    assert len(rows) == 1
    assert rows[0]["z"] == pytest.approx((2 - 5) / np.sqrt(3.5 * (1 / 3 + 1 / 3)))
    assert rows[0]["cliffs_delta"] == pytest.approx(-1.0)
    assert rows[0]["p_holm"] == pytest.approx(rows[0]["p_value"])  # uma comparação só


def test_compare_uses_mann_whitney_for_two_groups():
    frame = pd.DataFrame({"f": ["a"] * 4 + ["b"] * 4, "m": [1, 2, 3, 4, 5, 6, 7, 8]})
    row, _ = compare(frame, "f", "m")
    assert row["test"] == "Mann-Whitney"
    assert row["effect"] == pytest.approx(-1.0)
    assert row["effect_magnitude"] == "grande"


def test_main_writes_outputs(tmp_path):
    rng = np.random.default_rng(0)
    n = 80
    names = [f"o/r{i}" for i in range(n)]
    metrics = pd.DataFrame(
        {
            "full_name": names,
            "stars": rng.integers(100, 10_000, n),
            "language": ["Go"] * 30 + ["Python"] * 30 + ["C"] * 20,
            "deployment_frequency_per_week": np.r_[rng.uniform(0, 1, 30), rng.uniform(2, 3, 50)],
            "lead_time_a_hours": rng.uniform(1, 100, n),
            "cfr_a": rng.uniform(0, 1, n),
            "recovery_hours": rng.uniform(1, 50, n),
        }
    )
    metrics_path = tmp_path / "metrics.csv"
    metrics.to_csv(metrics_path, index=False)
    pd.DataFrame({"full_name": names, "cfr_b": rng.uniform(0, 1, n)}).to_csv(
        tmp_path / "cfr_b.csv", index=False
    )
    gold = tmp_path / "gold" / "o"
    gold.mkdir(parents=True)
    for i, name in enumerate(names):
        created = f"{2015 + i % 10}-01-01T00:00:00Z"
        (gold / f"r{i}.json").write_text(
            json.dumps({"repository": {"full_name": name, "created_at": created}}),
            encoding="utf-8",
        )
    out = tmp_path / "out"
    assert main([
        "--metrics", str(metrics_path), "--gold-dir", str(tmp_path / "gold"),
        "--consensus", str(tmp_path / "missing.csv"), "--cfr-b", str(tmp_path / "cfr_b.csv"),
        "--output-dir", str(out),
    ]) == 0

    tests = pd.read_csv(out / "rq06_tests.csv")
    assert len(tests) == 20  # 4 fatores × 5 métricas
    assert set(tests.loc[tests["factor"] == "tipo", "test"]) == {"insuficiente"}
    df_language = tests[(tests["factor"] == "linguagem")
                        & (tests["metric"] == "deployment_frequency_per_week")].iloc[0]
    assert df_language["significant"]
    assert (tests["p_holm"].dropna() >= tests["p_value"].dropna()).all()
    assert (out / "rq06_dunn.csv").exists()
    assert "Dunn post-hoc" in (out / "rq06_kruskal.md").read_text(encoding="utf-8")
