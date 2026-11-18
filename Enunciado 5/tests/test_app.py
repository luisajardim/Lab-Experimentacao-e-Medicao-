"""Testes do dashboard base e dos gráficos (T10, #105)."""

import sys

import plotly.graph_objects as go
from streamlit.testing.v1 import AppTest

import figures
import stats
from config import PALETTE, ROOT
from schema import load_runs

sys.path.insert(0, str(ROOT))
import app  # noqa: E402, I001


def test_figures_use_fixed_palette():
    df = load_runs()
    if df.empty:
        df = load_runs(include_synthetic=True)
    desc = stats.describe(df)
    fig = figures.fig_metric_by_scenario(desc)
    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0
    for trace in fig.data:
        assert trace.marker.color in PALETTE.values()

    vs_ctrl = stats.compare_to_control(df, n_resamples=100)
    fig_sp = figures.fig_speedup_vs_control(vs_ctrl)
    assert isinstance(fig_sp, go.Figure)
    for trace in fig_sp.data:
        if trace.marker and trace.marker.color:
            assert trace.marker.color in PALETTE.values()


def test_dashboard_renders_all_tabs_without_errors():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
    at.run()
    assert not at.exception
    tab_labels = [t.label for t in at.tabs]
    assert tab_labels == list(app.TABS)

