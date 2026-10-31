"""Testes da coleta dos dados reais (T02, #76).

Usam o ARFF versionado em `data/real/`, sem acessar a rede.
"""

import pandas as pd

from data import ARFF_PATH, FULL_CSV, SAMPLE_CSV, SAMPLE_SIZE, draw_sample, ensure_arff, load_kc1


def test_arff_checksum():
    assert ensure_arff() == ARFF_PATH


def test_load_kc1_shape_and_types():
    df = load_kc1()
    assert list(df.columns) == ["class_id", "loc", "defects"]
    assert len(df) == 145
    assert df["class_id"].tolist() == list(range(145))
    assert (df["loc"] > 0).all()
    assert (df["defects"] >= 0).all()


def test_sample_is_reproducible_and_without_replacement():
    df = load_kc1()
    a, b = draw_sample(df), draw_sample(df)
    pd.testing.assert_frame_equal(a, b)
    assert len(a) == SAMPLE_SIZE
    assert a["class_id"].is_unique
    assert a["class_id"].is_monotonic_increasing


def test_sample_changes_with_seed():
    df = load_kc1()
    assert not draw_sample(df, seed=1)["class_id"].equals(draw_sample(df)["class_id"])


def test_committed_csvs_match_regeneration():
    full = load_kc1()
    pd.testing.assert_frame_equal(pd.read_csv(FULL_CSV), full)
    pd.testing.assert_frame_equal(pd.read_csv(SAMPLE_CSV), draw_sample(full))
