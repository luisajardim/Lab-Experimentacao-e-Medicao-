"""Testes do dashboard base e do comando único `lab04` (T07, #82)."""

import sys

from streamlit.testing.v1 import AppTest

import cli
from config import COLOR_PEARSON, COLOR_SPEARMAN, PALETTE, ROOT
from figures import G2_TEXT, g3_text

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
    # As 7 seções do enunciado vêm primeiro e na ordem; extras opcionais (#91) só depois delas.
    assert headers[: len(app.SECTIONS)] == list(app.SECTIONS)
    assert headers[len(app.SECTIONS):] in ([], ["Para discutir: tamanho da amostra"])
    assert len(at.selectbox) >= 1


def test_section3_shows_interpreted_example_and_follows_alpha():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
    at.run()
    assert not at.exception
    assert any(s.value.startswith("Exemplo: um conjunto simulado") for s in at.subheader)
    texts = [m.value for m in at.markdown]
    assert any("com α = 0,05" in t and "S-real, n = 30" in t for t in texts)

    at.selectbox[0].set_value(0.01).run()
    assert not at.exception
    assert any("com α = 0,01" in m.value for m in at.markdown)


def test_section3_renders_g2_with_its_text():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
    at.run()
    assert not at.exception
    assert any(m.value == G2_TEXT for m in at.markdown)
    assert not any("T06b" in c.value for c in at.caption)


def test_section4_renders_g3_and_its_text_follows_alpha():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
    at.run()
    assert not at.exception
    assert any(m.value == g3_text(0.05) for m in at.markdown)
    assert not any("T09" in i.value for i in at.info)

    at.selectbox[0].set_value(0.01).run()
    assert not at.exception
    assert any(m.value == g3_text(0.01) for m in at.markdown)


def test_section6_renders_real_data_table_and_text():
    import stat_tests

    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
    at.run()
    assert not at.exception
    assert any(m.value == stat_tests.real_data_text(alpha=0.05) for m in at.markdown)
    assert any("Tamanho do efeito (IC 95%)" in list(df.value.columns) for df in at.dataframe)

    at.selectbox[0].set_value(0.01).run()
    assert not at.exception
    assert any("Conclusão (α = 0,01)" in list(df.value.columns) for df in at.dataframe)
