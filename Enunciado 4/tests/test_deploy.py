"""Testes da porta de entrada do deploy no Streamlit Cloud (#93)."""

import re
import sys
import tomllib
import types

from config import ROOT

DEPLOY = ROOT / "deploy"


def _pins(path):
    pins = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^([A-Za-z0-9_.\-]+)==([^\s;]+)", line)
        if match:
            pins[match.group(1).lower().replace("_", "-")] = match.group(2)
    return pins


def _entry_namespace():
    """Executa só as definições da porta de entrada (sem rodar o app)."""
    source = (DEPLOY / "streamlit_app.py").read_text(encoding="utf-8")
    source = source.replace("_forget_project_modules()\nrunpy.run_path", "pass  # runpy.run_path")
    namespace = {"__file__": str(DEPLOY / "streamlit_app.py")}
    exec(compile(source, "streamlit_app.py", "exec"), namespace)
    return namespace


def test_deploy_entry_points_to_the_dashboard():
    namespace = _entry_namespace()
    assert namespace["APP"] == ROOT / "app.py"
    assert namespace["SRC"] == ROOT / "src"
    assert (ROOT / "app.py").exists()


def test_deploy_entry_forgets_stale_project_modules(monkeypatch):
    # Depois de um push, o Cloud mantém em memória os módulos de `src/` da versão anterior.
    stale = types.ModuleType("figures")
    stale.__file__ = str(ROOT / "src" / "figures.py")
    monkeypatch.setitem(sys.modules, "figures", stale)
    _entry_namespace()["_forget_project_modules"]()
    assert "figures" not in sys.modules
    assert "pytest" in sys.modules  # pacotes de fora de `src/` ficam


def test_deploy_requirements_match_the_lockfile():
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    locked = {p["name"].lower(): p["version"] for p in lock["package"] if "version" in p}
    pins = _pins(DEPLOY / "requirements.txt")
    # As dependências diretas do app precisam estar fixadas, com a versão do uv.lock.
    for name in ("streamlit", "numpy", "scipy", "pandas", "plotly", "pyarrow"):
        assert pins.get(name) == locked[name], f"{name}: regenere deploy/requirements.txt"
    # E nenhuma versão fixada pode divergir do lock.
    assert {name: v for name, v in pins.items() if locked.get(name) != v} == {}
