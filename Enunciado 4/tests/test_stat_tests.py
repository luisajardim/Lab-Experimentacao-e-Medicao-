"""Testes de Pearson e Spearman vetorizados (T05, #79)."""

import warnings
from dataclasses import replace

import numpy as np
import pytest
from scipy import stats

import stat_tests
from config import SEED, SITUATIONS
from generate import generate
from stat_tests import CorrelationResult, interpret_example, pearson, run_example, spearman


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
