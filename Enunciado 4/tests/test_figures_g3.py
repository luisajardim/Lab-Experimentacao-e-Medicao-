"""Testes do gráfico G3 e do texto de erro tipo I (T09, #84)."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pytest

from config import COLOR_PEARSON, COLOR_SPEARMAN, OUTLIER_RATE, SITUATIONS
from figures import fig_g3, g3_text, mc_band, type1_table
from generate import latent_normal, to_kc1_marginals
from simulate import cell_rng, load_pvalues, load_summary


def test_mc_band_is_043_pp_at_5_percent_with_10000_reps():
    low, high = mc_band(0.05, 10_000)
    assert high - 0.05 == pytest.approx(0.0043, abs=5e-5)
    assert 0.05 - low == pytest.approx(high - 0.05)
    assert mc_band(0.01, 10_000)[1] - 0.01 == pytest.approx(0.00195, abs=5e-5)


@pytest.mark.parametrize("alpha", [0.05, 0.01])
def test_type1_table_matches_simulation_summary(alpha):
    table = type1_table(alpha)
    summary = load_summary().query("rho == 0 and alpha == @alpha")
    summary = summary.assign(test=summary["test"].str.capitalize())
    merged = summary.merge(table, on=["situation", "test"], suffixes=("_summary", ""))
    assert len(merged) == len(table) == 2 * len(SITUATIONS)
    np.testing.assert_allclose(merged["rate"], merged["reject_rate"])
    np.testing.assert_array_equal(merged["n_nan"], merged["n_nan_summary"])
    # As duas caudas somam a taxa (p NaN não rejeita e coeficiente 0 não rejeita).
    np.testing.assert_allclose(table["right"] + table["left"], table["rate"])


def _null(rates: dict[str, float], reps: int = 1000) -> pd.DataFrame:
    """Réplicas sintéticas com ρ = 0: a fração `rate` de cada teste rejeita com coeficiente > 0."""
    rows = []
    for situation, rate in rates.items():
        k = int(rate * reps)
        p = np.r_[np.full(k, 0.001), np.full(reps - k, 0.5)]
        rows.append(pd.DataFrame({"situation": situation, "r": 0.4, "p_pearson": p,
                                  "rho_s": 0.4, "p_spearman": p}))
    return pd.concat(rows, ignore_index=True)


def test_verdict_uses_the_monte_carlo_band():
    table = type1_table(0.05, null=_null({"S-base": 0.05, "S-real": 0.20, "S-real-n10": 0.01}))
    verdicts = table.groupby("situation")["verdict"].first().to_dict()
    assert verdicts == {"S-base": "perto", "S-real": "liberal", "S-real-n10": "conservador"}


def test_real_results_classify_each_test_and_situation():
    verdict = type1_table(0.05).set_index(["situation", "test"])["verdict"]
    assert verdict[("S-base", "Pearson")] == verdict[("S-base", "Spearman")] == "perto"
    assert verdict[("S-real-n10", "Pearson")] == verdict[("S-outlier", "Pearson")] == "liberal"
    assert (verdict.xs("Spearman", level="test") == "perto").all()


def test_fig_g3_points_band_and_alpha_line():
    alpha = 0.05
    table = type1_table(alpha)
    fig = fig_g3(alpha=alpha)
    assert isinstance(fig, go.Figure)
    x_max = fig.layout.xaxis.range[1]
    for name, color in (("Pearson", COLOR_PEARSON), ("Spearman", COLOR_SPEARMAN)):
        trace = next(t for t in fig.data if t.name == name)
        assert trace.marker.color == color
        rates = table[table["test"] == name]["rate"].to_numpy()
        beyond = rates > 3.5 * alpha
        xs = np.asarray(trace.x, dtype=float)
        np.testing.assert_allclose(xs[~beyond], rates[~beyond])
        assert (xs[beyond] < x_max).all()  # na borda, dentro do eixo
        # o valor real continua no hover e no rótulo
        assert [c[0] for c in trace.customdata] == [
            f"{100 * v:.2f}%".replace(".", ",") for v in rates
        ]
    labels = [a.text for a in fig.layout.annotations]
    assert "Pearson: 20,14% · liberal (fora da escala)" in labels
    assert "Spearman: 4,82% · perto de α" in labels
    band = fig.layout.shapes[0]
    assert (band.x0, band.x1) == pytest.approx(mc_band(alpha, 10_000))
    line = next(t for t in fig.data if t.name.startswith("α ="))
    assert set(line.x) == {alpha}
    assert "G3" in fig.layout.title.text
    assert "ρ = 0" in fig.layout.xaxis.title.text
    assert list(fig.layout.yaxis.ticktext)[0].startswith("S-base")


def test_fig_g3_band_follows_alpha():
    fig = fig_g3(alpha=0.01)
    assert (fig.layout.shapes[0].x0, fig.layout.shapes[0].x1) == pytest.approx(
        mc_band(0.01, 10_000)
    )


@pytest.mark.parametrize("alpha", [0.05, 0.01])
def test_text_reports_every_rate_and_verdict(alpha):
    table = type1_table(alpha)
    text = g3_text(alpha)
    for row in table.itertuples():
        assert f"{row.test} {100 * row.rate:.2f}%".replace(".", ",") in text
    for term in ("liberal", "conservador", "faixa cinza", "Por quê", "S-outlier", "cauda direita"):
        assert term in text


def test_text_at_1_percent_admits_spearman_leaves_the_band():
    assert "sai da faixa em S-real-n10" in g3_text(0.01)
    assert "O Spearman fica perto de α em todas as situações" in g3_text(0.05)


def _outlier_cell():
    """Refaz a célula S-outlier, ρ = 0 com o mesmo stream do motor para saber quais amostras
    receberam uma classe extrema (mesma ordem de sorteio de `generate.contaminate`)."""
    rng = cell_rng("S-outlier", 0.0)
    z1, z2 = latent_normal(0.0, SITUATIONS["S-outlier"][1], 10_000, rng)
    x, y = to_kc1_marginals(z1, z2)
    return rng.uniform(size=x.shape) < OUTLIER_RATE


@pytest.mark.parametrize("alpha", [0.05, 0.01])
def test_outlier_claims_in_the_text(alpha):
    contaminated = _outlier_cell().any(axis=1)
    pvalues = load_pvalues()
    cell = pvalues[(pvalues["situation"] == "S-outlier") & (pvalues["rho"] == 0)].sort_values("rep")
    reject = cell["p_pearson"].to_numpy() < alpha
    # "cerca de 19% das amostras recebem uma classe extrema"
    assert contaminated.mean() == pytest.approx(0.19, abs=0.01)
    # "vêm principalmente dessas amostras, em que ele rejeita na maior parte das vezes"
    # (α = 5%: 81% das rejeições e 86% dessas amostras; α = 1%: 89% e 73%)
    assert contaminated[reject].mean() > 0.7
    assert reject[contaminated].mean() > 0.6
    assert "19%" in g3_text(alpha)
