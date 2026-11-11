"""Testes de Pearson e Spearman vetorizados (T05, #79)."""

import re
import warnings
from dataclasses import replace

import numpy as np
import pandas as pd
import pytest
from scipy import stats

import stat_tests
from config import SEED, SITUATIONS
from data import SAMPLE_CSV
from generate import generate
from stat_tests import (
    CorrelationResult,
    analyze_real,
    bootstrap_ci,
    cohen_label,
    fisher_ci,
    interpret_example,
    pearson,
    real_data_table,
    real_data_text,
    real_sample_analysis,
    run_example,
    spearman,
)


def _scipy_row(fn, x_row, y_row):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", stats.ConstantInputWarning)
        result = fn(x_row, y_row)
    return result.statistic, result.pvalue


@pytest.mark.parametrize("situation", list(SITUATIONS))
@pytest.mark.parametrize("rho", [0.0, 0.3, 0.6])
@pytest.mark.parametrize(
    ("ours", "reference"), [(pearson, stats.pearsonr), (spearman, stats.spearmanr)]
)
def test_batch_matches_scipy_row_by_row(situation, rho, ours, reference):
    x, y = generate(situation, rho, reps=300, rng=np.random.default_rng(SEED))
    result = ours(x, y)
    expected = np.array([_scipy_row(reference, *row) for row in zip(x, y, strict=True)])
    np.testing.assert_allclose(result.coef, expected[:, 0], rtol=1e-9, atol=1e-12)
    np.testing.assert_allclose(result.p, expected[:, 1], rtol=1e-8, atol=1e-12)
    assert result.coef.shape == result.t.shape == result.p.shape == (300,)
    assert result.df == SITUATIONS[situation][1] - 2


def test_pearson_by_hand():
    # dx·dy = 8, Σdx² = Σdy² = 10 -> r = 0,8; t = 0,8·√(3/0,36)
    result = pearson([1, 2, 3, 4, 5], [2, 1, 4, 3, 5])
    assert result.coef == pytest.approx(0.8)
    assert result.t == pytest.approx(0.8 * np.sqrt(3 / 0.36))
    assert result.p == pytest.approx(2 * stats.t.sf(result.t, 3))
    assert result.df == 3


def test_spearman_is_pearson_on_average_ranks():
    x, y = [10, 20, 20, 30, 500], [0, 0, 1, 5, 7]
    expected = pearson([1, 2.5, 2.5, 4, 5], [1.5, 1.5, 3, 4, 5])
    result = spearman(x, y)
    assert result.coef == pytest.approx(expected.coef)
    assert result.t == pytest.approx(expected.t)
    assert result.p == pytest.approx(expected.p)


def test_spearman_ignores_monotonic_transform_but_pearson_does_not():
    x = np.array([1.0, 2, 3, 4, 5, 6, 7, 8])
    y = np.array([2.0, 1, 4, 3, 6, 5, 8, 7])
    assert spearman(x**4, y).coef == pytest.approx(spearman(x, y).coef)
    assert pearson(x**4, y).coef != pytest.approx(pearson(x, y).coef)


def test_single_outlier_inflates_pearson_more_than_spearman():
    x = [1.0, 2, 3, 4, 5, 6, 7, 8, 9, 1000]
    y = [5.0, 3, 8, 1, 7, 2, 6, 4, 9, 1000]
    assert pearson(x, y).coef > 0.99
    assert spearman(x, y).coef < 0.6


@pytest.mark.parametrize("fn", [pearson, spearman])
def test_perfect_association_gives_infinite_t_and_zero_p(fn):
    up, down = fn([1, 2, 3, 4], [2, 4, 6, 8]), fn([1, 2, 3, 4], [8, 6, 4, 2])
    assert (up.coef, up.t, up.p) == (1.0, np.inf, 0.0)
    assert (down.coef, down.t, down.p) == (-1.0, -np.inf, 0.0)


@pytest.mark.parametrize("fn", [pearson, spearman])
def test_constant_row_is_nan_without_warning_and_does_not_touch_other_rows(fn):
    x = np.array([[1.0, 2, 3, 4], [1, 2, 3, 4], [0.1, 0.1, 0.1, 0.1]])
    y = np.array([[0.0, 0, 0, 0], [1, 3, 2, 4], [1, 3, 2, 4]])
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        result = fn(x, y)
    assert np.isnan(result.coef[[0, 2]]).all() and np.isnan(result.p[[0, 2]]).all()
    assert result.coef[1] == pytest.approx(0.8)
    # NaN nunca conta como rejeição na taxa da simulação.
    assert (result.p < 0.05).tolist() == [False, False, False]


def test_real_simulated_constant_samples_are_nan_like_scipy():
    x, y = generate("S-real-n10", 0.0, reps=3000, rng=np.random.default_rng(SEED))
    constant = y.max(axis=1) == y.min(axis=1)
    assert constant.any()
    np.testing.assert_array_equal(np.isnan(pearson(x, y).p), constant)
    np.testing.assert_array_equal(np.isnan(spearman(x, y).p), constant)


def test_single_sample_returns_scalars():
    result = pearson([1, 2, 3, 4], [1, 3, 2, 4])
    assert np.ndim(result.coef) == np.ndim(result.t) == np.ndim(result.p) == 0


@pytest.mark.parametrize("fn", [pearson, spearman])
@pytest.mark.parametrize(
    ("x", "y"),
    [([1, 2, 3], [1, 2]), ([1, 2], [1, 2]), (1.0, 2.0)],
)
def test_invalid_shapes_are_rejected(fn, x, y):
    with pytest.raises(ValueError):
        fn(x, y)


def test_example_is_reproducible_and_matches_scipy():
    first, second = run_example(), run_example()
    np.testing.assert_array_equal(first.x, second.x)
    np.testing.assert_array_equal(first.y, second.y)
    assert (first.situation, first.rho, first.n) == ("S-real", stat_tests.EXAMPLE_RHO, 30)
    assert first.pearson.p == pytest.approx(stats.pearsonr(first.x, first.y).pvalue)
    assert first.spearman.p == pytest.approx(stats.spearmanr(first.x, first.y).pvalue)


def test_interpretation_reports_the_computed_values():
    example = run_example()
    text = interpret_example(example)
    for value in (example.pearson.coef, example.spearman.coef):
        assert f"{value:.3f}".replace(".", ",") in text
    assert "não é a probabilidade de H₀ ser verdadeira" in text
    assert "S-real, n = 30" in text


def _fake_example(p_pearson, p_spearman, rho=0.3):
    base = run_example()
    return replace(
        base,
        rho=rho,
        pearson=CorrelationResult(0.5, 2.0, p_pearson, 28),
        spearman=CorrelationResult(0.4, 1.5, p_spearman, 28),
    )


@pytest.mark.parametrize(
    ("p_pearson", "p_spearman", "rho", "expected"),
    [
        (0.01, 0.02, 0.3, "os dois testes acertam"),
        (0.2, 0.3, 0.3, "os dois testes cometem erro tipo II"),
        (0.2, 0.01, 0.3, "o Spearman acerta e o Pearson comete erro tipo II"),
        (0.01, 0.2, 0.3, "o Pearson acerta e o Spearman comete erro tipo II"),
        (0.2, 0.3, 0.0, "os dois testes acertam"),
        (0.01, 0.02, 0.0, "os dois testes cometem erro tipo I "),
        (0.01, 0.2, 0.0, "o Spearman acerta e o Pearson comete erro tipo I "),
    ],
)
def test_interpretation_names_the_right_decision(p_pearson, p_spearman, rho, expected):
    assert expected in interpret_example(_fake_example(p_pearson, p_spearman, rho))


def test_interpretation_follows_alpha():
    example = _fake_example(0.03, 0.03)
    assert "rejeita H₀ com α = 0,05" in interpret_example(example, alpha=0.05)
    assert "não rejeita H₀" not in interpret_example(example, alpha=0.05)
    assert "não rejeita H₀ com α = 0,01" in interpret_example(example, alpha=0.01)


def test_very_small_p_is_written_as_inequality():
    assert "p < 0,001" in interpret_example(_fake_example(1e-9, 1e-9))


def test_interpretation_refuses_undefined_coefficient():
    example = _fake_example(0.5, 0.5)
    nan_result = CorrelationResult(np.nan, np.nan, np.nan, 28)
    with pytest.raises(ValueError):
        interpret_example(replace(example, pearson=nan_result))


# --- Dados reais (T11, #86) ---------------------------------------------------

def test_fisher_ci_by_hand():
    low, high = fisher_ci(0.5, 30)
    half = 1.959963984540054 / np.sqrt(27)
    z = np.arctanh(0.5)
    assert (low, high) == pytest.approx((np.tanh(z - half), np.tanh(z + half)))
    assert low < 0.5 < high


@pytest.mark.parametrize(
    ("coef", "label"),
    [(0.05, "desprezível"), (-0.2, "pequeno"), (0.3, "moderado"), (0.51, "grande")],
)
def test_cohen_labels(coef, label):
    assert cohen_label(coef) == label


def test_bootstrap_ci_is_reproducible_and_contains_the_estimate():
    rng = np.random.default_rng(0)
    x = rng.normal(size=40)
    y = x + rng.normal(size=40)
    first, second = bootstrap_ci(x, y, n_resamples=2000), bootstrap_ci(x, y, n_resamples=2000)
    assert first == second
    assert first[0] < spearman(x, y).coef < first[1]


def test_analyze_real_finds_the_influential_class_and_practical_numbers():
    x = np.array([10.0, 20, 30, 40, 50, 60, 70, 80, 90, 5000])
    y = np.array([0.0, 1, 0, 2, 1, 3, 0, 2, 4, 100])
    a = analyze_real(x, y)
    assert (a.influential_loc, a.influential_defects) == (5000, 100)
    assert a.r_without_influential == pytest.approx(pearson(x[:-1], y[:-1]).coef)
    assert a.rho_s_without_influential == pytest.approx(spearman(x[:-1], y[:-1]).coef)
    larger = x > np.median(x)
    assert a.share_defects_larger_half == pytest.approx(y[larger].sum() / y.sum())
    assert a.any_defect_smaller_half == pytest.approx((y[~larger] > 0).mean())
    assert a.pearson_ci == pytest.approx(fisher_ci(a.pearson.coef, 10))


def test_real_sample_matches_scipy():
    a = real_sample_analysis()
    sample = pd.read_csv(SAMPLE_CSV)
    assert a.n == 30
    assert a.pearson.p == pytest.approx(stats.pearsonr(sample["loc"], sample["defects"]).pvalue)
    assert a.spearman.p == pytest.approx(stats.spearmanr(sample["loc"], sample["defects"]).pvalue)


def test_real_table_has_required_columns_and_conclusions_follow_alpha():
    table = real_data_table(alpha=0.05)
    assert list(table["Teste"]) == ["Pearson", "Spearman"]
    for column in ("Estatística", "t (28 g.l.)", "p-valor", "Tamanho do efeito (IC 95%)",
                   "Método do IC", "Conclusão (α = 0,05)"):
        assert column in table
    assert table["Método do IC"].str.contains("Fisher").iloc[0]
    assert table["Método do IC"].str.contains("bootstrap").iloc[1]
    a = real_sample_analysis()
    fake = replace(a, spearman=a.spearman._replace(p=0.03))
    conclusions = real_data_table(fake, alpha=0.01)["Conclusão (α = 0,01)"]
    assert conclusions.iloc[0].startswith("Rejeita")
    assert conclusions.iloc[1].startswith("Não rejeita")
    assert "Conclusões diferentes" in real_data_text(fake, alpha=0.01)


def test_real_text_reports_computed_numbers():
    a = real_sample_analysis()
    text = real_data_text(alpha=0.05)
    assert "Mesma conclusão" in text
    for value in (a.spearman.coef, *a.spearman_ci, a.r_without_influential):
        assert f"{value:.2f}".replace(".", ",") in text
    assert f"{100 * a.share_defects_larger_half:.0f}%" in text
    assert "2.883 LOC e 101 defeitos" in text
    # Decimais sempre com vírgula (o ponto só aparece como separador de milhar, ex.: 2.883).
    assert re.search(r"\d\.\d{2}(?!\d)", text) is None
