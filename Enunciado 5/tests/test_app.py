"""Testes do dashboard base e dos gráficos (T10, #105)."""

import sys

import plotly.graph_objects as go
import pytest
from streamlit.testing.v1 import AppTest

import adoption
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
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
    at.run()
    assert not at.exception
    # `at.tabs` traz também as abas aninhadas, intercaladas (a de Adoção tem "Valores
    # absolutos" e "Participação (%)" dentro dela). As 5 de primeiro nível têm de estar
    # todas presentes e na ordem certa entre si.
    tab_labels = [t.label for t in at.tabs]
    assert set(app.TABS) <= set(tab_labels)
    posicoes = [tab_labels.index(t) for t in app.TABS]
    assert posicoes == sorted(posicoes)


def test_aba_de_adocao_desenha_os_graficos():
    """Com os CSVs da T15 presentes, a aba sai do estado de espera e mostra as figuras."""
    if not adoption.available():
        pytest.skip("sem data/npm_downloads/: rode `uv run lab05 downloads`")
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
    at.run()
    assert not at.exception
    assert len(at.get("plotly_chart")) >= 4   # as outras abas + as 4 figuras da adoção
    textos = " ".join(m.value for m in at.markdown)
    assert "Séries históricas de downloads" in textos
    assert "Crescimento no último ano" in textos
    assert "Adoção × speedup medido" in textos
    # a limitação central não pode sumir da tela
    avisos = " ".join(e.value for e in at.error)
    assert "download não é uso" in avisos.lower() or "já vem instalado" in avisos

