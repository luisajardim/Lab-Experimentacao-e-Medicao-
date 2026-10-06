"""Testes do coletor de busca de candidatos (T04, sem rede)."""

import csv
from pathlib import Path

from _fakes import FakeResponse, FakeSession

from collector.search import collect_candidates
from github.rest import GitHubRESTClient


CONFIG_BASE = """
[search]
star_slices = ["1000..2000"]
languages = []
max_candidates = 10
per_page = 100

[paths]
raw_dir = "raw"
meta_dir = "meta"
candidates_csv = "raw/candidates.csv"
"""


def _client(responses, **kwargs):
    kwargs.setdefault("wall_clock", lambda: 1000.0)
    kwargs.setdefault("sleeper", lambda _seconds: None)
    session = FakeSession(responses)
    return GitHubRESTClient("token", session=session, **kwargs), session


def _item(full_name, stars, language="Python", default_branch="main", created_at="2020-01-01T00:00:00Z"):
    return {
        "full_name": full_name,
        "stargazers_count": stars,
        "language": language,
        "default_branch": default_branch,
        "created_at": created_at,
        "html_url": f"https://github.com/{full_name}",
    }


def _search_response(items, next_url=None):
    headers = {}
    if next_url:
        headers["Link"] = f"<{next_url}>; rel=\"next\""
    return FakeResponse(json_data={"items": items}, headers=headers)


def test_returns_candidates_and_saves_csv(tmp_path):
    config = tmp_path / "config.toml"
    config.write_text(CONFIG_BASE, encoding="utf-8")

    items = [
        _item("a/a", 1500),
        _item("b/b", 2000),
    ]
    client, _ = _client([_search_response(items)])

    candidates = collect_candidates(client, config)

    assert len(candidates) == 2
    assert candidates[0].full_name == "a/a"
    assert candidates[0].stars == 1500
    assert candidates[0].language == "Python"
    assert candidates[0].default_branch == "main"
    assert candidates[1].full_name == "b/b"

    csv_path = tmp_path / "raw" / "candidates.csv"
    assert csv_path.exists()
    with open(csv_path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 2
    assert rows[0]["full_name"] == "a/a"
    assert rows[0]["stars"] == "1500"
    assert rows[0]["language"] == "Python"


def test_deduplicates_by_full_name(tmp_path):
    config = tmp_path / "config.toml"
    config.write_text(CONFIG_BASE, encoding="utf-8")

    items = [
        _item("a/a", 1500),
        _item("b/b", 2000),
        _item("a/a", 3000),
    ]
    client, _ = _client([_search_response(items)])

    candidates = collect_candidates(client, config)

    assert [c.full_name for c in candidates] == ["a/a", "b/b"]


def test_respects_max_candidates(tmp_path):
    config = tmp_path / "config.toml"
    config.write_text(
        CONFIG_BASE.replace("max_candidates = 10", "max_candidates = 2"),
        encoding="utf-8",
    )

    items = [_item(f"r{i}", 1000 + i) for i in range(10)]
    client, _ = _client([_search_response(items)])

    candidates = collect_candidates(client, config)

    assert len(candidates) == 2


def test_stops_at_max_candidates_across_queries(tmp_path):
    config = tmp_path / "config.toml"
    config.write_text(
        """
[search]
star_slices = ["1000..2000", "2000..5000"]
languages = []
max_candidates = 3
per_page = 100

[paths]
raw_dir = "raw"
meta_dir = "meta"
candidates_csv = "raw/candidates.csv"
""",
        encoding="utf-8",
    )

    items1 = [_item(f"a{i}", 1000 + i) for i in range(5)]
    items2 = [_item(f"b{i}", 3000 + i) for i in range(5)]
    client, session = _client([_search_response(items1), _search_response(items2)])

    candidates = collect_candidates(client, config)

    assert len(candidates) == 3
    assert len(session.requests) == 1
    assert session.requests[0]["params"]["q"] == "stars:1000..2000"


def test_language_slices_generate_separate_queries(tmp_path):
    config = tmp_path / "config.toml"
    config.write_text(
        """
[search]
star_slices = ["1000..2000"]
languages = ["python", "javascript"]
max_candidates = 10
per_page = 100

[paths]
raw_dir = "raw"
meta_dir = "meta"
candidates_csv = "raw/candidates.csv"
""",
        encoding="utf-8",
    )

    items = [_item("a/a", 1500)]
    client, _ = _client([_search_response(items), _search_response(items)])

    collect_candidates(client, config)

    queries_dir = tmp_path / "meta" / "search_queries"
    assert queries_dir.exists()
    files = sorted(queries_dir.iterdir())
    assert len(files) == 2
    assert "stars:1000..2000+language:python" in files[0].read_text()
    assert "stars:1000..2000+language:javascript" in files[1].read_text()


def test_empty_search_returns_empty_list(tmp_path):
    config = tmp_path / "config.toml"
    config.write_text(CONFIG_BASE, encoding="utf-8")

    client, _ = _client([_search_response([])])

    candidates = collect_candidates(client, config)

    assert candidates == []

    csv_path = tmp_path / "raw" / "candidates.csv"
    assert csv_path.exists()
    with open(csv_path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows == []
