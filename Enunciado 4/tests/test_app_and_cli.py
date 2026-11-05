"""Testes do dashboard base e do comando único `lab04` (T07, #82)."""

import sys

from streamlit.testing.v1 import AppTest

import cli
from config import COLOR_PEARSON, COLOR_SPEARMAN, PALETTE, ROOT

sys.path.insert(0, str(ROOT))
import app  # noqa: E402, I001




def test_palette_has_distinct_colors_for_both_tests():
    assert PALETTE["Pearson"] == COLOR_PEARSON
    assert PALETTE["Spearman"] == COLOR_SPEARMAN
    assert COLOR_PEARSON != COLOR_SPEARMAN


def test_cli_prepare_only_succeeds():
    rc = cli.main(["--prepare-only"])
    assert rc == 0


def test_dashboard_renders_all_seven_sections_in_order():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
    at.run()
    assert not at.exception

    headers = [h.value for h in at.header]
    assert headers == list(app.SECTIONS)
    assert len(at.selectbox) >= 1
