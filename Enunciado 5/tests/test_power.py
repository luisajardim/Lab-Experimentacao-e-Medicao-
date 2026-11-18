"""Testes da análise de poder (T09, #104)."""

import numpy as np
import pytest

import power


def test_simulate_power_increases_with_speedup_and_n():
    rng = np.random.default_rng(42)
    noise = rng.normal(0, 0.25, size=200)
    p_small = power.simulate_power(noise, n_pairs=15, speedup=1.1, alpha=0.01, sims=400)
    p_large = power.simulate_power(noise, n_pairs=30, speedup=1.5, alpha=0.01, sims=400)
    assert 0.0 <= p_small < p_large <= 1.0
    assert p_large > 0.8


def test_log_ratio_noise_is_centered_around_zero():
    pilot = power.load_pilot()
    noise = power.log_ratio_noise(pilot)
    assert ("next-app", "cold") in noise
    assert ("express-api", "warm-cache") in noise
    for arr in noise.values():
        assert len(arr) > 0
        assert abs(np.median(arr)) < 0.2


def test_power_table_and_choose_n_on_synthetic_noise():
    rng = np.random.default_rng(42)
    base = rng.normal(0, 0.15, size=100)
    noise = {("express-api", "cold"): base, ("express-api", "warm-cache"): base,
             ("react-vite", "cold"): base, ("react-vite", "warm-cache"): base,
             ("next-app", "cold"): base, ("next-app", "warm-cache"): base}
    table = power.power_table(noise, machines=3, n_grid=(3, 5, 10),
                              speedups=(1.2, 1.5), sims=300)
    assert set(table["scenario"]) == {"cold", "ci", "warm-cache", "reinstall"}
    assert len(table) == 3 * 4 * 2 * 3
    n = power.choose_n(table, speedup=1.2, target=0.80)
    assert n in (3, 5, 10)


def test_pilot_duration_and_collection_hours():
    sec = power.seconds_per_install()
    assert 5.0 < sec < 120.0
    hrs = power.collection_hours(10, sec)
    assert hrs == pytest.approx((6 * 4 * 3 * 10 + power.WARMUP) * sec / 3600)
