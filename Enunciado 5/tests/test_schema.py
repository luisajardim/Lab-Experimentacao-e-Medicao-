"""Testes do schema de `runs.csv` e do CSV sintético (T01, #96)."""

import pandas as pd
import pytest

import schema
import synthetic
from config import MANAGERS, PROJECTS, SCENARIOS


@pytest.fixture(scope="module")
def df():
    return synthetic.generate(reps=2)


def test_synthetic_follows_schema(df):
    assert tuple(df.columns) == schema.COLUMN_NAMES
    assert schema.validate(df) is not None


def test_synthetic_covers_full_design(df):
    real = df[~df["warmup"]]
    n_cells = len(MANAGERS) * len(SCENARIOS) * len(PROJECTS)
    assert len(real) == len(synthetic.MACHINES) * n_cells * 2
    counts = real.groupby(["machine", "project", "scenario", "manager"]).size()
    assert len(counts) == len(synthetic.MACHINES) * n_cells and (counts == 2).all()


def test_synthetic_is_reproducible():
    a, b = synthetic.generate(reps=1), synthetic.generate(reps=1)
    pd.testing.assert_frame_equal(a, b)


def test_order_is_a_permutation_per_machine(df):
    for _, block in df.groupby("machine"):
        assert sorted(block["order"]) == list(range(1, len(block) + 1))


def test_validate_reports_missing_and_bad_values(df):
    with pytest.raises(schema.SchemaError, match="colunas faltando"):
        schema.validate(df.drop(columns=["wall_s"]))
    bad = df.copy()
    bad.loc[bad.index[0], "manager"] = "pip"
    bad.loc[bad.index[1], "wall_s"] = -1.0
    with pytest.raises(schema.SchemaError) as exc:
        schema.validate(bad)
    assert "manager" in str(exc.value) and "wall_s" in str(exc.value)


def test_validate_rejects_duplicated_run_id(df):
    dup = pd.concat([df.head(1), df.head(1)], ignore_index=True)
    with pytest.raises(schema.SchemaError, match="run_id duplicado"):
        schema.validate(dup)


def test_roundtrip_and_load_runs(df, tmp_path):
    schema.write_runs(df, tmp_path / "maq1" / "runs.csv")
    schema.write_runs(df.assign(run_id=df["run_id"] + "-s"), tmp_path / "synthetic" / "runs.csv")

    loaded = schema.load_runs(tmp_path)
    assert set(loaded["machine"]) == set(df["machine"])
    assert not loaded["warmup"].any()
    assert len(loaded) == (~df["warmup"]).sum()

    with_synth = schema.load_runs(tmp_path, include_synthetic=True, include_warmup=True)
    assert len(with_synth) == 2 * len(df)


def test_load_runs_ignora_piloto_por_padrao(df, tmp_path):
    schema.write_runs(df, tmp_path / "maq1" / "runs.csv")
    schema.write_runs(df.assign(run_id=df["run_id"] + "-p"), tmp_path / "pilot" / "runs.csv")
    schema.write_runs(df.assign(run_id=df["run_id"] + "-s"), tmp_path / "synthetic" / "runs.csv")

    assert len(schema.load_runs(tmp_path, include_warmup=True)) == len(df)
    with_pilot = schema.load_runs(tmp_path, include_pilot=True, include_warmup=True)
    assert len(with_pilot) == 2 * len(df)
    everything = schema.load_runs(tmp_path, include_synthetic=True, include_pilot=True,
                                  include_warmup=True)
    assert len(everything) == 3 * len(df)


def test_load_runs_empty_dir_returns_typed_empty_frame(tmp_path):
    empty = schema.load_runs(tmp_path)
    assert empty.empty and tuple(empty.columns) == schema.COLUMN_NAMES
