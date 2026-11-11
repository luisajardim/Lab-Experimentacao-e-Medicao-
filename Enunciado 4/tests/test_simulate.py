"""Testes do motor de simulação (T08, #83)."""

import json
import sys

import numpy as np
import pandas as pd
import pytest

import simulate
from config import ALPHAS, EFFECT_GRID, ROOT, SITUATIONS
from simulate import (
    POPULATION_FILE,
    PVALUES_FILE,
    SUMMARY_FILE,
    cache_key,
    config_snapshot,
    load_population,
    load_pvalues,
    load_summary,
    run_simulations,
    simulate_cell,
    summarize,
)
from stat_tests import pearson, spearman

sys.path.insert(0, str(ROOT / "scripts"))
from parquet_to_csv import convert  # noqa: E402

COLUMNS = ["situation", "rho", "rep", "r", "p_pearson", "rho_s", "p_spearman"]


@pytest.fixture(scope="module")
def small_run(tmp_path_factory):
    """Rodada pequena (200 réplicas, POPULATION_N reduzido) num diretório temporário."""
    out = tmp_path_factory.mktemp("sim")
    with pytest.MonkeyPatch.context() as mp:  # só durante a rodada pequena
        mp.setattr(simulate, "POPULATION_N", 5_000)
        meta = run_simulations(reps=200, out_dir=out, verbose=False)
    return out, meta


def test_cell_schema_and_values_match_stat_tests():
    df = simulate_cell("S-real", 0.3, reps=50)
    assert list(df.columns) == COLUMNS
    assert len(df) == 50 and df["rep"].tolist() == list(range(50))
    x, y = simulate.generate("S-real", 0.3, reps=50, rng=simulate.cell_rng("S-real", 0.3))
    np.testing.assert_allclose(df["p_pearson"], pearson(x, y).p)
    np.testing.assert_allclose(df["rho_s"], spearman(x, y).coef)


def test_cells_are_reproducible_and_independent():
    a, b = simulate_cell("S-base", 0.2, 100), simulate_cell("S-base", 0.2, 100)
    pd.testing.assert_frame_equal(a, b)
    other = simulate_cell("S-base", 0.3, 100)
    assert not np.allclose(a["r"], other["r"])


def test_run_writes_all_cells(small_run):
    out, meta = small_run
    pv = load_pvalues(out)
    assert list(pv.columns) == COLUMNS
    assert len(pv) == len(SITUATIONS) * len(EFFECT_GRID) * 200
    assert set(pv["situation"]) == set(SITUATIONS)
    summary = load_summary(out)
    assert len(summary) == len(SITUATIONS) * len(EFFECT_GRID) * len(ALPHAS) * 2
    population = load_population(out)
    assert len(population) == len(SITUATIONS) * len(EFFECT_GRID)
    assert meta["config"]["reps"] == 200


def test_summary_matches_manual_count(small_run):
    out, _ = small_run
    pv, summary = load_pvalues(out), load_summary(out)
    cell = pv[(pv["situation"] == "S-real") & (pv["rho"] == 0.3)]
    row = summary.query("situation == 'S-real' and rho == 0.3 and alpha == 0.05 and test == 'spearman'")
    assert row["reject_rate"].item() == pytest.approx(np.mean(cell["p_spearman"] < 0.05))


def test_nan_pvalues_count_as_no_rejection():
    df = pd.DataFrame(
        {"situation": "S-real-n10", "rho": 0.0, "p_pearson": [np.nan, 0.01, 0.5, 0.2],
         "p_spearman": [np.nan, 0.01, 0.5, 0.2]}
    )
    s = summarize(df, alphas=(0.05,))
    assert (s["reject_rate"] == 0.25).all()
    assert (s["n_nan"] == 1).all()


def test_cache_skips_and_detects_changes(small_run, monkeypatch):
    out, meta = small_run
    calls = []
    monkeypatch.setattr(simulate, "simulate_cell", lambda *a, **k: calls.append(a))
    monkeypatch.setattr(simulate, "POPULATION_N", 5_000)
    run_simulations(reps=200, out_dir=out, verbose=False)
    assert calls == []  # cache válido: nada é re-simulado
    assert cache_key(config_snapshot(201)) != meta["cache_key"]


def test_committed_results_are_current_and_valid():
    meta = json.loads((simulate.DATA_SIM / simulate.META_FILE).read_text())
    assert meta["cache_key"] == cache_key(config_snapshot(meta["config"]["reps"]))
    assert meta["config"]["reps"] == simulate.REPS
    summary = load_summary()
    base_h0 = summary.query("situation == 'S-base' and rho == 0.0 and alpha == 0.05")
    # Na situação ideal, o erro tipo I dos dois testes fica perto de 5% (±3 erros padrão).
    assert (abs(base_h0["reject_rate"] - 0.05) < 3 * base_h0["mc_se"]).all()
    population = load_population().query("situation == 'S-base'")
    np.testing.assert_allclose(population["r_pop"], population["rho"], atol=0.01)


def test_parquet_to_csv_roundtrip(small_run, tmp_path):
    out, _ = small_run
    csv_path = convert(out / PVALUES_FILE, tmp_path / "pv.csv")
    back = pd.read_csv(csv_path)
    original = load_pvalues(out)
    assert list(back.columns) == COLUMNS
    np.testing.assert_allclose(back["p_pearson"], original["p_pearson"])


def test_outputs_have_expected_files(small_run):
    out, _ = small_run
    for name in (PVALUES_FILE, SUMMARY_FILE, POPULATION_FILE, simulate.META_FILE):
        assert (out / name).exists()


def test_population_is_shared_by_situations_with_the_same_generator(small_run):
    out, _ = small_run
    pop = load_population(out).set_index(["situation", "rho"])
    for rho in EFFECT_GRID:
        assert pop.loc[("S-real", rho)].equals(pop.loc[("S-real-n10", rho)])


def test_cell_seed_depends_on_name_not_position():
    from simulate import cell_rng

    a = cell_rng("S-real", 0.3).standard_normal(5)
    b = cell_rng("S-real", 0.3).standard_normal(5)
    c = cell_rng("S-outlier", 0.3).standard_normal(5)
    np.testing.assert_array_equal(a, b)
    assert not np.allclose(a, c)


def test_cache_key_tracks_code_files():
    snap = config_snapshot(simulate.REPS)
    assert set(snap["code_sha256"]) == set(simulate.CODE_FILES)


def test_file_hash_ignores_line_endings(tmp_path):
    # No Windows o checkout grava CRLF; o cache não pode re-simular por causa disso (#83).
    lf, crlf = tmp_path / "lf.py", tmp_path / "crlf.py"
    lf.write_bytes(b"x = 1\ny = 2\n")
    crlf.write_bytes(b"x = 1\r\ny = 2\r\n")
    assert simulate.file_sha256(lf) == simulate.file_sha256(crlf)
    other = tmp_path / "other.py"
    other.write_bytes(b"x = 1\ny = 3\n")
    assert simulate.file_sha256(other) != simulate.file_sha256(lf)
