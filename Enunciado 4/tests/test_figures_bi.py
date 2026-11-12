"""Gráficos que só existem no painel: dispersão real, efeito com IC 95% e vantagem de poder."""

import numpy as np
import pandas as pd
import pytest

import simulate
import stat_tests
from config import COLOR_PEARSON, COLOR_SPEARMAN, SITUATIONS
from data import FULL_CSV, SAMPLE_CSV
from figures import fig_power_gap, fig_real_effect, fig_real_scatter, power_gap_table


def test_real_scatter_shows_both_datasets_and_marks_the_influential_class():
    fig = fig_real_scatter()
    assert [len(t.x) for t in fig.data] == [len(pd.read_csv(FULL_CSV)), len(pd.read_csv(SAMPLE_CSV))]
    assert fig.layout.xaxis.type == "log"
    a = stat_tests.real_sample_analysis()
    (label,) = fig.layout.annotations
    assert label.x == pytest.approx(np.log10(a.influential_loc))
    assert label.y == a.influential_defects


def test_real_effect_has_each_coefficient_with_its_interval():
    a = stat_tests.real_sample_analysis()
    fig = fig_real_effect(a)
    pearson, spearman, without = fig.data
    assert pearson.marker.color == COLOR_PEARSON and spearman.marker.color == COLOR_SPEARMAN
    for trace, result, (low, high) in ((pearson, a.pearson, a.pearson_ci),
                                       (spearman, a.spearman, a.spearman_ci)):
        coef = trace.x[0]
        assert coef == pytest.approx(float(result.coef))
        assert coef - trace.error_x.arrayminus[0] == pytest.approx(low)
        assert coef + trace.error_x.array[0] == pytest.approx(high)
    assert list(without.x) == pytest.approx([a.r_without_influential, a.rho_s_without_influential])


@pytest.mark.parametrize("alpha", [0.05, 0.01])
def test_power_gap_is_spearman_minus_pearson_in_points(alpha):
    summary = simulate.load_summary()
    gap = power_gap_table(alpha, summary)
    assert list(gap.index) == list(SITUATIONS)
    cell = summary[(summary["situation"] == "S-real") & np.isclose(summary["rho"], 0.6)
                   & np.isclose(summary["alpha"], alpha)].set_index("test")["reject_rate"]
    assert gap.loc["S-real", 0.6] == pytest.approx(100 * (cell["spearman"] - cell["pearson"]))


def test_power_gap_colors_are_symmetric_around_zero():
    fig = fig_power_gap(0.05)
    heat = fig.data[0]
    assert heat.zmin == -heat.zmax
    assert heat.colorscale[0][1] == COLOR_PEARSON and heat.colorscale[-1][1] == COLOR_SPEARMAN
    assert "−0" not in {t for row in heat.text for t in row}
