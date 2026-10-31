"""Teste do piloto nos dados reais (T03, #77)."""

import json
import sys

import pandas as pd
import pytest

from config import ROOT
from data import FULL_CSV

sys.path.insert(0, str(ROOT / "scripts"))
from piloto import PILOT_JSON, run_pilot  # noqa: E402


def test_committed_pilot_matches_regeneration():
    committed = json.loads(PILOT_JSON.read_text())
    fresh = run_pilot(pd.read_csv(FULL_CSV))
    assert fresh.keys() == committed.keys()
    for key, value in committed.items():
        assert fresh[key] == pytest.approx(value), key
