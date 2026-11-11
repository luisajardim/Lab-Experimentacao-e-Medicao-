"""Testes da porta de entrada do deploy no Streamlit Cloud (#93)."""

import re
import tomllib

from config import ROOT

DEPLOY = ROOT / "deploy"


def _pins(path):
    pins = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^([A-Za-z0-9_.\-]+)==([^\s;]+)", line)
        if match:
            pins[match.group(1).lower().replace("_", "-")] = match.group(2)
    return pins


def test_deploy_entry_points_to_the_dashboard():
    entry = (DEPLOY / "streamlit_app.py").read_text(encoding="utf-8")
    assert 'parents[1] / "app.py"' in entry
    assert (DEPLOY / "streamlit_app.py").resolve().parents[1] / "app.py" == ROOT / "app.py"
    assert (ROOT / "app.py").exists()


def test_deploy_requirements_match_the_lockfile():
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    locked = {p["name"].lower(): p["version"] for p in lock["package"] if "version" in p}
    pins = _pins(DEPLOY / "requirements.txt")
    # As dependências diretas do app precisam estar fixadas, com a versão do uv.lock.
    for name in ("streamlit", "numpy", "scipy", "pandas", "plotly", "pyarrow"):
        assert pins.get(name) == locked[name], f"{name}: regenere deploy/requirements.txt"
    # E nenhuma versão fixada pode divergir do lock.
    assert {name: v for name, v in pins.items() if locked.get(name) != v} == {}
