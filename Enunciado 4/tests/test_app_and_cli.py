"""Testes do dashboard (painel só com gráficos) e do comando único `lab04` (T07, #82; #87)."""

import sys

import pytest
from streamlit.testing.v1 import AppTest

import cli
import simulate
from config import COLOR_PEARSON, COLOR_SPEARMAN, PALETTE, ROOT, SITUATIONS

sys.path.insert(0, str(ROOT))
import app  # noqa: E402, I001


def test_palette_has_distinct_colors_for_both_tests():
    assert PALETTE["Pearson"] == COLOR_PEARSON
    assert PALETTE["Spearman"] == COLOR_SPEARMAN
    assert COLOR_PEARSON != COLOR_SPEARMAN


def test_cli_prepare_only_succeeds():
    rc = cli.main(["--prepare-only"])
    assert rc == 0


@pytest.fixture(scope="module")
def dashboard() -> AppTest:
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120)
    at.run()
    assert not at.exception
    return at


def test_dashboard_is_only_charts_and_indicators(dashboard):
    # Nada de seções, parágrafos ou tabelas: só o título, os filtros, os indicadores e os gráficos.
    assert not dashboard.header and not dashboard.subheader
    assert not dashboard.dataframe and not dashboard.info and not dashboard.expander
    assert [m.value for m in dashboard.markdown if not m.value.startswith("<style>")] == [
        f"### {app.TITLE}"
    ]
    assert len(dashboard.metric) == 6
    expected = len(app.CHARTS) - (0 if app.sample_size.load() is not None else 1)
    assert len(dashboard.get("plotly_chart")) == expected


def test_dashboard_has_the_two_filters(dashboard):
    assert dashboard.segmented_control(key="alpha").value == 0.05
    assert dashboard.multiselect(key="situations").value == list(SITUATIONS)


def test_alpha_filter_updates_the_indicators():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120)
    at.run()
    before = [m.value for m in at.metric]
    at.segmented_control(key="alpha").set_value(0.01).run()
    assert not at.exception
    after = [m.value for m in at.metric]
    summary = simulate.load_summary()
    assert after[2] == app._pct(app.rate(summary, "S-outlier", 0.0, "pearson", 0.01))
    assert after[:2] == before[:2]  # correlação da amostra real não depende de α
    assert after[2:] != before[2:]


def test_situation_filter_keeps_only_the_chosen_panels():
    summary = simulate.load_summary()
    fig = app.chart_g4(0.05, summary, ["S-real", "S-outlier"])
    assert [a.text for a in fig.layout.annotations] == ["S-real", "S-outlier"]
    gap = app.chart_gap(0.05, summary, ["S-real", "S-outlier"])
    assert list(gap.data[0].y) == ["S-real", "S-outlier"]
    g3 = app.chart_g3(0.05, ["S-base"])
    assert set(g3.data[-1].y.round()) == {0}


def test_every_chart_has_a_short_label_and_no_long_text():
    sample_df, full_df, summary = app.get_data()
    analysis = app.get_analysis()
    situations = list(SITUATIONS)
    figs = {
        "g1": app.chart_g1(sample_df, full_df),
        "scatter": app.chart_scatter(sample_df, full_df, analysis),
        "g2": app.chart_g2(0.05),
        "effect": app.chart_effect(analysis),
        "g3": app.chart_g3(0.05, situations),
        "gap": app.chart_gap(0.05, summary, situations),
        "g4": app.chart_g4(0.05, summary, situations),
    }
    for key, fig in figs.items():
        assert fig.layout.title.text == app.CHARTS[key]
        assert len(fig.layout.title.text) <= 45
        for annotation in fig.layout.annotations:
            assert len(annotation.text) <= 40, (key, annotation.text)


def test_offscale_point_in_g3_gets_its_value():
    fig = app.chart_g3(0.05, list(SITUATIONS))
    summary = simulate.load_summary()
    value = app._pct(app.rate(summary, "S-outlier", 0.0, "pearson", 0.05))
    assert [a.text for a in fig.layout.annotations] == [value]
