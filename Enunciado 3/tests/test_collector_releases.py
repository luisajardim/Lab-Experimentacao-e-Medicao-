"""Testes do coletor de releases (sem rede)."""

from _fakes import FakeResponse, FakeSession

from collector.releases import collect_releases
from github.rest import GitHubRESTClient


def _client(responses):
    session = FakeSession(responses)
    return GitHubRESTClient("token", session=session, wall_clock=lambda: 1000.0), session


def _release(tag_name, published_at, *, draft=False, prerelease=False, id_=1):
    return {
        "id": id_,
        "tag_name": tag_name,
        "name": tag_name,
        "draft": draft,
        "prerelease": prerelease,
        "published_at": published_at,
        "html_url": f"https://github.com/o/r/releases/{tag_name}",
    }


def test_filters_out_draft_releases():
    client, _ = _client(
        [
            FakeResponse(
                json_data=[
                    _release("v1.0.0", "2026-01-01T00:00:00Z"),
                    _release("v1.1.0", "2026-02-01T00:00:00Z", draft=True),
                ]
            )
        ]
    )
    releases = collect_releases(client, "o", "r")
    assert [r.tag_name for r in releases] == ["v1.0.0"]


def test_keeps_prereleases():
    client, _ = _client(
        [
            FakeResponse(
                json_data=[_release("v2.0.0-rc1", "2026-01-01T00:00:00Z", prerelease=True)]
            )
        ]
    )
    releases = collect_releases(client, "o", "r")
    assert len(releases) == 1
    assert releases[0].prerelease is True


def test_sorts_by_published_at_ascending():
    client, _ = _client(
        [
            FakeResponse(
                json_data=[
                    _release("v2.0.0", "2026-03-01T00:00:00Z"),
                    _release("v1.0.0", "2026-01-01T00:00:00Z"),
                    _release("v1.5.0", "2026-02-01T00:00:00Z"),
                ]
            )
        ]
    )
    releases = collect_releases(client, "o", "r")
    assert [r.tag_name for r in releases] == ["v1.0.0", "v1.5.0", "v2.0.0"]


def test_empty_releases_returns_empty_list():
    client, _ = _client([FakeResponse(json_data=[])])
    assert collect_releases(client, "o", "r") == []
