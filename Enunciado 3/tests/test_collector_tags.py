"""Testes do coletor de tags (sem rede)."""

from _fakes import FakeResponse, FakeSession

from collector.tags import collect_tags
from github.rest import GitHubRESTClient


def _client(responses):
    session = FakeSession(responses)
    return GitHubRESTClient("token", session=session, wall_clock=lambda: 1000.0), session


def _commit_response(sha, date):
    return {
        "sha": sha,
        "commit": {"author": {"date": date}, "message": "msg"},
        "html_url": f"https://github.com/o/r/commit/{sha}",
    }


def test_resolves_date_for_each_tag():
    client, session = _client(
        [
            FakeResponse(
                json_data=[
                    {"name": "v1.0.0", "commit": {"sha": "aaa"}},
                    {"name": "v1.1.0", "commit": {"sha": "bbb"}},
                ]
            ),
            FakeResponse(json_data=_commit_response("aaa", "2026-01-01T00:00:00Z")),
            FakeResponse(json_data=_commit_response("bbb", "2026-02-01T00:00:00Z")),
        ]
    )
    tags = collect_tags(client, "o", "r")
    assert [(t.name, t.sha, t.date) for t in tags] == [
        ("v1.0.0", "aaa", "2026-01-01T00:00:00Z"),
        ("v1.1.0", "bbb", "2026-02-01T00:00:00Z"),
    ]
    assert session.requests[1]["url"] == "/repos/o/r/commits/aaa"
    assert session.requests[2]["url"] == "/repos/o/r/commits/bbb"


def test_skips_tags_without_sha():
    client, session = _client([FakeResponse(json_data=[{"name": "broken", "commit": {}}])])
    tags = collect_tags(client, "o", "r")
    assert tags == []
    assert len(session.requests) == 1  # não tenta resolver commit para sha vazio


def test_empty_tags_returns_empty_list():
    client, _ = _client([FakeResponse(json_data=[])])
    assert collect_tags(client, "o", "r") == []
