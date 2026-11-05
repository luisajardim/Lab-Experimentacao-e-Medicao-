"""Testes do gráfico G1 (T06a, #80)."""

import numpy as np
import plotly.graph_objects as go

from figures import G1_TEXT, fig_g1


def test_fig_g1_returns_plotly_figure_with_traces():
    fig = fig_g1()
    assert isinstance(fig, go.Figure)
    # 4 séries × 2 painéis (LOC e defeitos) = 8 traces de histograma
    assert len(fig.data) == 8
    trace_names = {t.name for t in fig.data}
    assert any("Amostra (n = 30)" in name for name in trace_names)
    assert any("KC1 completo" in name for name in trace_names)
    assert any("S-real" in name for name in trace_names)


def test_fig_g1_has_title_units_and_legend():
    fig = fig_g1()
    assert fig.layout.title.text and "G1" in fig.layout.title.text
    assert "LOC" in fig.layout.xaxis.title.text
    assert "linhas de código" in fig.layout.xaxis.title.text
    assert "defeitos" in fig.layout.xaxis2.title.text.lower()
    assert "%" in fig.layout.yaxis.title.text
    assert any(t.showlegend for t in fig.data)


def test_fig_g1_is_reproducible_with_seed():
    f1 = fig_g1(seed=42)
    f2 = fig_g1(seed=42)
    for t1, t2 in zip(f1.data, f2.data, strict=True):
        np.testing.assert_array_equal(t1.x, t2.x)


def test_g1_text_covers_shape_and_distributions():
    sentences = [s.strip() for s in G1_TEXT.split(".") if s.strip()]
    # Texto curto de 2 a 4 frases (cuidado com decimais com vírgula em português)
    assert 2 <= len(sentences) <= 4
    lower = G1_TEXT.lower()
    for term in ("assimetria", "zero", "gamma", "binomial negativa"):
        assert term in lower

