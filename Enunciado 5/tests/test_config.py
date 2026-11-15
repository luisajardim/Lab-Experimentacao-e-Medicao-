"""Testes do .env e da pasta de trabalho (config.py)."""

import config


def test_load_env_parses_and_does_not_override(monkeypatch, tmp_path):
    env = tmp_path / ".env"
    env.write_text('# comentário\n\nLAB05_A="F:\\\\lab05\\\\work"\nexport LAB05_B=x\nLAB05_C=já\nlixo\n',
                   encoding="utf-8")
    monkeypatch.delenv("LAB05_A", raising=False)
    monkeypatch.delenv("LAB05_B", raising=False)
    monkeypatch.setenv("LAB05_C", "terminal")
    values = config.load_env(env)
    assert values == {"LAB05_A": "F:\\\\lab05\\\\work", "LAB05_B": "x", "LAB05_C": "já"}
    assert config.os.environ["LAB05_B"] == "x"
    assert config.os.environ["LAB05_C"] == "terminal"   # o terminal tem prioridade


def test_load_env_missing_file(tmp_path):
    assert config.load_env(tmp_path / "nao-existe") == {}


def test_workdir_default_is_inside_project(monkeypatch):
    monkeypatch.delenv(config.WORKDIR_ENV, raising=False)
    assert config.workdir() == config.ROOT / ".work"
    monkeypatch.setenv(config.WORKDIR_ENV, "  ")
    assert config.workdir() == config.ROOT / ".work"


def test_workdir_from_env(monkeypatch, tmp_path):
    monkeypatch.setenv(config.WORKDIR_ENV, str(tmp_path / "w"))
    assert config.workdir() == tmp_path / "w"
