"""Testes do coletor de commits entre releases (sem rede)."""

import pytest
from _fakes import FakeResponse, FakeSession

from collector.commits import (
    COMPARE_NOT_FOUND,
    NO_PREVIOUS_RELEASE,
    collect_commits_between,
)
from github.models import Release
from github.rest import GitHubHTTPError, GitHubRESTClient


def _client(responses, **kwargs):
    kwargs.setdefault("wall_clock", lambda: 1000.0)
    kwargs.setdefault("sleeper", lambda _seconds: None)
    session = FakeSession(responses)
    return GitHubRESTClient("token", session=session, **kwargs), session


def _release(tag_name, published_at):
    return Release(
        id=1,
        tag_name=tag_name,
        name=tag_name,
        draft=False,
        prerelease=False,
        published_at=published_at,
        html_url=f"https://github.com/o/r/releases/{tag_name}",
    )


def _compare_response(shas):
    return {
        "commits": [
            {
                "sha": sha,
                "commit": {"author": {"date": "2026-01-01T00:00:00Z"}, "message": "m"},
                "html_url": f"https://github.com/o/r/commit/{sha}",
            }
            for sha in shas
        ]
    }


def test_first_release_has_no_previous_and_is_ignored():
    client, session = _client([])
    releases = [_release("v1.0.0", "2026-01-01T00:00:00Z")]

    results = collect_commits_between(client, "o", "r", releases)

    assert len(results) == 1
    assert results[0].release == "v1.0.0"
    assert results[0].previous_release is None
    assert results[0].commits is None
    assert results[0].ignored_reason == NO_PREVIOUS_RELEASE
    assert results[0].ignored is True
    assert session.requests == []  # nenhuma chamada de compare foi feita


def test_second_release_compares_against_first():
    client, session = _client(
        [FakeResponse(json_data=_compare_response(["a", "b"]))]
    )
    releases = [
        _release("v1.0.0", "2026-01-01T00:00:00Z"),
        _release("v1.1.0", "2026-02-01T00:00:00Z"),
    ]

    results = collect_commits_between(client, "o", "r", releases)

    assert len(results) == 2
    assert results[0].ignored_reason == NO_PREVIOUS_RELEASE

    second = results[1]
    assert second.release == "v1.1.0"
    assert second.previous_release == "v1.0.0"
    assert second.ignored_reason is None
    assert second.ignored is False
    assert [c.sha for c in second.commits] == ["a", "b"]
    assert session.requests[0]["url"] == "/repos/o/r/compare/v1.0.0...v1.1.0"
    assert session.requests[0]["params"]["per_page"] == 250


def test_compare_404_is_registered_and_ignored():
    client, _ = _client([FakeResponse(status_code=404, text="Not Found")])
    releases = [
        _release("v1.0.0", "2026-01-01T00:00:00Z"),
        _release("v1.1.0", "2026-02-01T00:00:00Z"),
    ]

    results = collect_commits_between(client, "o", "r", releases)

    second = results[1]
    assert second.commits is None
    assert second.ignored_reason == COMPARE_NOT_FOUND
    assert second.ignored is True


def test_compare_non_404_error_propagates():
    client, _ = _client([FakeResponse(status_code=500, text="boom")], max_retries=0)
    releases = [
        _release("v1.0.0", "2026-01-01T00:00:00Z"),
        _release("v1.1.0", "2026-02-01T00:00:00Z"),
    ]

    with pytest.raises(GitHubHTTPError) as ctx:
        collect_commits_between(client, "o", "r", releases)
    assert ctx.value.status == 500


def test_three_releases_use_previous_as_base_each_time():
    client, session = _client(
        [
            FakeResponse(json_data=_compare_response(["a"])),
            FakeResponse(json_data=_compare_response(["b", "c"])),
        ]
    )
    releases = [
        _release("v1.0.0", "2026-01-01T00:00:00Z"),
        _release("v1.1.0", "2026-02-01T00:00:00Z"),
        _release("v1.2.0", "2026-03-01T00:00:00Z"),
    ]

    results = collect_commits_between(client, "o", "r", releases)

    assert session.requests[0]["url"] == "/repos/o/r/compare/v1.0.0...v1.1.0"
    assert session.requests[1]["url"] == "/repos/o/r/compare/v1.1.0...v1.2.0"
    assert [c.sha for c in results[2].commits] == ["b", "c"]


def test_empty_releases_returns_empty_list():
    client, _ = _client([])
    assert collect_commits_between(client, "o", "r", []) == []
