"""Testes do runner de instalação com um gerenciador falso, sem rede (T04, #99)."""

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

import runner
import schema
from config import MANAGERS, SCENARIOS

FIXTURES = Path(__file__).parent / "fixtures"
FAKE = str(FIXTURES / "fake_pm.py")
PROJECT = "express-api"
FAKE_FILES, FAKE_SIZE = 8, 64 * 1024


def fake_spec(*extra: str) -> runner.ManagerSpec:
    return runner.ManagerSpec(program=(sys.executable, FAKE, *extra), install_cold=("install",),
                              install_frozen=("ci",), install_reinstall=("install", "--again"))


COMMANDS = {"npm": fake_spec(), "pnpm": fake_spec(), "bun": fake_spec("--fail")}


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "_registry_env", lambda manager, registry: {})
    log = tmp_path / "fake.log"
    monkeypatch.setenv("FAKE_LOG", str(log))
    monkeypatch.setenv("FAKE_FILES", str(FAKE_FILES))
    monkeypatch.setenv("FAKE_FILE_SIZE", str(FAKE_SIZE))
    return tmp_path, log


def make_collector(tmp_path, machine="teste"):
    return runner.Collector(machine=machine, projects_dir=FIXTURES / "projects",
                            workdir=tmp_path / "work", commands=dict(COMMANDS),
                            log=lambda s: None)


def run_collect(tmp_path, managers=("npm", "pnpm", "bun"), reps=2, warmup=1, out=None):
    out = out or tmp_path / "out" / "runs.csv"
    n = runner.collect("teste", projects=(PROJECT,), scenarios=tuple(SCENARIOS),
                       managers=managers, reps=reps, warmup=warmup, out=out,
                       collector=make_collector(tmp_path), log=lambda s: None,
                       verify_versions=False)   # o fake imprime 9.9.9
    return n, out


# ---------------------------------------------------------------- sequência


def test_sequence_is_reproducible_and_permuted_per_rep():
    kw = dict(projects=("express-api", "next-app"), scenarios=("cold", "ci"),
              managers=tuple(MANAGERS), reps=3, warmup=2)
    a = runner.build_sequence("bernardo", **kw)
    assert a == runner.build_sequence("bernardo", **kw)
    assert a != runner.build_sequence("luisa", **kw)
    n_cells = 2 * 2 * len(MANAGERS)
    assert len(a) == 2 + 3 * n_cells
    assert [c["order"] for c in a] == list(range(1, len(a) + 1))
    assert all(c["warmup"] and c["rep"] == 0 for c in a[:2])
    for rep in (1, 2, 3):
        cells = [(c["project"], c["scenario"], c["manager"]) for c in a if c["rep"] == rep]
        assert len(set(cells)) == n_cells
    first = [c["manager"] for c in a if c["rep"] == 1]
    second = [c["manager"] for c in a if c["rep"] == 2]
    assert first != second


def test_machine_seed_is_stable():
    assert runner.machine_seed("pedro") == runner.machine_seed("pedro")
    assert runner.machine_seed("pedro") != runner.machine_seed("luisa")


def test_install_args_and_cache_env(tmp_path):
    npm = runner.COMMANDS["npm"]
    assert npm.install_args("cold")[0] == "install"
    assert npm.install_args("ci")[0] == "ci" and npm.install_args("warm-cache")[0] == "ci"
    assert npm.install_args("reinstall")[0] == "install"
    assert "--immutable" in runner.COMMANDS["yarn-berry-pnp"].install_args("ci")
    assert "--frozen-lockfile" in runner.COMMANDS["pnpm"].install_args("warm-cache")
    for manager in MANAGERS:
        env = runner.cache_env(manager, tmp_path / manager)
        assert env["LAB05_CACHE_DIR"] == str(tmp_path / manager)
        assert len(env) >= 2
    assert runner.cache_env("yarn-berry-nm", tmp_path)["YARN_ENABLE_GLOBAL_CACHE"] == "true"


# ---------------------------------------------------------------- coleta ponta a ponta


def test_collect_end_to_end(env):
    tmp_path, log = env
    n, out = run_collect(tmp_path)
    assert n == 1 + 2 * 4 * 3
    df = schema.read_runs(out)
    assert len(df) == n and tuple(df.columns) == schema.COLUMN_NAMES
    assert sorted(df["order"]) == list(range(1, n + 1))
    assert df["warmup"].sum() == 1
    assert set(df["manager_version"]) == {"9.9.9"}

    ok = df[df["manager"] != "bun"]
    assert (ok["exit_code"] == 0).all() and ok["build_ok"].all()
    # Hard links do cache contados uma vez: o projeto tem 8 arquivos ligados ao cache + 1
    # próprio; o cache não soma nada além disso.
    expected_mb = (FAKE_FILES + 1) * FAKE_SIZE / (1024 * 1024)
    assert ok["disk_mb"].round(4).eq(round(expected_mb, 4)).all()
    assert (ok["cache_mb"] == 0).all()
    assert (ok["n_files"] == FAKE_FILES + 1).all()
    assert (ok["wall_s"] > 0).all()

    # Falha registrada sem interromper a coleta.
    bun = df[df["manager"] == "bun"]
    assert (bun["exit_code"] == 3).all() and not bun["build_ok"].any()
    assert (bun["disk_mb"] == 0).all()


def test_collect_resumes_without_duplicates(env):
    tmp_path, _ = env
    out = tmp_path / "out" / "runs.csv"
    n1, _ = run_collect(tmp_path, managers=("npm",), reps=1, warmup=0, out=out)
    rows = pd.read_csv(out)
    # Simula interrupção: apaga as 2 últimas linhas e retoma.
    rows.iloc[:-2].to_csv(out, index=False)
    n2, _ = run_collect(tmp_path, managers=("npm",), reps=1, warmup=0, out=out)
    n3, _ = run_collect(tmp_path, managers=("npm",), reps=1, warmup=0, out=out)
    assert (n1, n2, n3) == (4, 2, 0)
    df = schema.read_runs(out)
    assert len(df) == 4 and not df.duplicated(["scenario", "rep"]).any()


def test_scenarios_prepare_the_right_state(env):
    tmp_path, log = env
    run_collect(tmp_path, managers=("npm",), reps=1, warmup=0)
    calls = [json.loads(line) for line in log.read_text().splitlines()]
    measured = [c for c in calls if c["phase"] == "measure"]
    prep = [c for c in calls if c["phase"] == "prep"]
    by_args = {tuple(c["args"]): c for c in measured}
    assert len(measured) == 4 and len(prep) == 2   # warm-cache e reinstall têm preparação

    cold = by_args[("install",)]
    assert not cold["cache_had_files"] and not cold["lockfile"] and not cold["node_modules"]
    reinstall = by_args[("install", "--again")]
    assert reinstall["cache_had_files"] and reinstall["lockfile"] and reinstall["node_modules"]
    ci_like = [c for c in measured if c["args"] == ["ci"]]   # ci e warm-cache
    assert sorted(c["cache_had_files"] for c in ci_like) == [False, True]
    assert all(c["lockfile"] and not c["node_modules"] for c in ci_like)


def test_collect_reports_missing_manager(env):
    tmp_path, _ = env
    col = make_collector(tmp_path)
    col.commands["pnpm"] = runner.ManagerSpec("nao-existe-xyz", ("i",), ("i",), ("i",))
    with pytest.raises(SystemExit, match="pnpm"):
        runner.collect("teste", projects=(PROJECT,), managers=("npm", "pnpm"), reps=1,
                       out=tmp_path / "o.csv", collector=col, log=lambda s: None)


def test_timeout_is_recorded(env, tmp_path):
    col = make_collector(tmp_path)
    col.timeout_s = 0.3
    col.commands["npm"] = runner.ManagerSpec(
        (sys.executable, "-c", "import time, sys; sys.argv[-1] == '--version' or time.sleep(20)"),
        ("install",), ("ci",), ("install",))
    row = col.run_one(PROJECT, "cold", "npm", rep=1, order=1, warmup=False)
    assert row["exit_code"] == runner.metrics.TIMEOUT_EXIT_CODE and not row["build_ok"]


# ---------------------------------------------------------------- CLI


def test_dry_run_and_args(capsys):
    assert runner.main(["--machine", "x", "--pilot", "--dry-run"]) == 0
    out = capsys.readouterr().out
    n = 2 + 5 * 2 * 3 * len(MANAGERS)
    assert f"{n} instalações" in out
    args = runner.parse_args(["--machine", "x"])
    assert args.reps == runner.DEFAULT_REPS and args.scenarios == tuple(SCENARIOS)
    with pytest.raises(SystemExit):
        runner.parse_args(["--machine", "x", "--managers", "pip"])


# ---------------------------------------------------------------- checagem de versões


def test_version_matches():
    assert runner.version_matches("1.22.22", "1.22")
    assert runner.version_matches("12", "12")
    assert not runner.version_matches("1.220.0", "1.22")
    assert not runner.version_matches("4.18.1", "1.22")
    assert not runner.version_matches("", "11")


def test_check_versions_aborts_on_wrong_version(env, monkeypatch):
    tmp_path, _ = env
    col = make_collector(tmp_path)
    monkeypatch.setattr(col, "node_version", lambda: runner.NODE_EXPECTED_VERSION + ".0.0")
    # O fake responde 9.9.9: é o caso de um Yarn Classic que virou Berry (outra versão).
    with pytest.raises(SystemExit, match=r"npm: esperado .*encontrado 9\.9\.9"):
        runner.check_versions(col, PROJECT, ("npm",))


def test_check_versions_passes_and_cleans_up(env, monkeypatch):
    tmp_path, _ = env
    col = make_collector(tmp_path)
    monkeypatch.setattr(col, "node_version", lambda: runner.NODE_EXPECTED_VERSION + ".1.2")
    monkeypatch.setitem(runner.MANAGERS, "npm", {**runner.MANAGERS["npm"], "expected_version": "9"})
    runner.check_versions(col, PROJECT, ("npm",))
    assert not col.project_dir(PROJECT, "npm").exists()


def test_check_versions_flags_node(env, monkeypatch):
    tmp_path, _ = env
    col = make_collector(tmp_path)
    monkeypatch.setattr(col, "node_version", lambda: "20.1.0")
    monkeypatch.setitem(runner.MANAGERS, "npm", {**runner.MANAGERS["npm"], "expected_version": "9"})
    with pytest.raises(SystemExit, match="node: esperado"):
        runner.check_versions(col, PROJECT, ("npm",))


# ---------------------------------------------------------------- cache/registry (piloto 17/11)

def test_pnpm_usa_variaveis_pnpm_config(tmp_path):
    # pnpm 11+ ignora npm_config_*: sem isto o store foi para F:\.pnpm-store no piloto.
    env = runner.cache_env("pnpm", tmp_path)
    assert env["pnpm_config_store_dir"] == str(tmp_path / "store")
    import registry
    assert registry.registry_env("pnpm")["pnpm_config_registry"] == registry.LOCAL_URL


def test_setup_problem_aceita_subpasta_do_cache_e_barra_final():
    cache = Path("F:/lab05/work/cache/pnpm")
    url = "http://localhost:4873/"
    assert runner.setup_problem("pnpm", "cache", "F:\\lab05\\work\\cache\\pnpm\\store\\v11\n",
                                cache, url) is None
    assert runner.setup_problem("yarn-berry-nm", "registry", "http://localhost:4873", cache,
                                url) is None


def test_setup_problem_pega_store_e_registry_errados():
    cache = Path("F:/lab05/work/cache/pnpm")
    url = "http://localhost:4873/"
    assert "esperado" in runner.setup_problem("pnpm", "cache", "F:\\.pnpm-store\\v11", cache, url)
    assert "npmjs" in runner.setup_problem("pnpm", "registry", "https://registry.npmjs.org/",
                                           cache, url)
    # Prefixo parecido não conta como subpasta.
    assert runner.setup_problem("npm", "cache", "F:/lab05/work/cache/pnpm-x", cache, url)
