"""Testes do cliente REST com sessão falsa (sem rede)."""

import httpx
import pytest

from _fakes import FakeResponse, FakeSession
from github.rest import (
    GitHubHTTPError,
    GitHubRESTClient,
    parse_link_header,
)


def _client(responses, **kwargs):
    kwargs.setdefault("max_retries", 5)
    kwargs.setdefault("backoff_base", 1.0)
    kwargs.setdefault("wall_clock", lambda: 1000.0)
    session = FakeSession(responses)
    client = GitHubRESTClient("token", session=session, **kwargs)
    return client, session


def test_get_json_returns_body():
    client, session = _client([FakeResponse(json_data={"ok": True})])
    assert client.get_json("/test") == {"ok": True}
    assert session.requests[0]["method"] == "GET"
    assert session.requests[0]["url"] == "/test"


def test_get_json_raises_on_404():
    client, _ = _client([FakeResponse(status_code=404, text="Not Found")])
    with pytest.raises(GitHubHTTPError) as ctx:
        client.get_json("/missing")
    assert ctx.value.status == 404


def test_retry_on_429_with_retry_after():
    slept = []
    client, session = _client(
        [
            FakeResponse(status_code=429, headers={"Retry-After": "0.5"}),
            FakeResponse(json_data={"ok": True}),
        ],
        sleeper=slept.append,
    )
    assert client.get_json("/test") == {"ok": True}
    assert len(session.requests) == 2
    assert slept == [0.5]


def test_backoff_is_exponential():
    slept = []
    client, session = _client(
        [FakeResponse(status_code=503)] * 3 + [FakeResponse(json_data={"ok": True})],
        sleeper=slept.append,
    )
    assert client.get_json("/test") == {"ok": True}
    assert slept == [1.0, 2.0, 4.0]


def test_gives_up_after_max_retries():
    slept = []
    client, session = _client(
        [FakeResponse(status_code=503)] * 10,
        max_retries=3,
        sleeper=slept.append,
    )
    with pytest.raises(GitHubHTTPError) as ctx:
        client.get_json("/test")
    assert ctx.value.status == 503
    assert len(session.requests) == 4
    assert slept == [1.0, 2.0, 4.0]


def test_retries_on_transport_error():
    slept = []
    client, session = _client(
        [httpx.TransportError("boom"), FakeResponse(json_data={"ok": True})],
        sleeper=slept.append,
    )
    assert client.get_json("/test") == {"ok": True}
    assert len(slept) == 1


def test_rate_limit_pause_when_exhausted():
    slept = []
    client, _ = _client(
        [
            FakeResponse(
                json_data={"ok": True},
                headers={"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "1030"},
            )
        ],
        sleeper=slept.append,
    )
    assert client.get_json("/test") == {"ok": True}
    assert slept == [31.0]


def test_no_pause_when_quota_remains():
    slept = []
    client, _ = _client(
        [
            FakeResponse(
                json_data={"ok": True},
                headers={"X-RateLimit-Remaining": "42", "X-RateLimit-Reset": "1030"},
            )
        ],
        sleeper=slept.append,
    )
    assert client.get_json("/test") == {"ok": True}
    assert slept == []


def test_rate_limit_endpoint():
    client, _ = _client(
        [
            FakeResponse(
                json_data={
                    "resources": {
                        "core": {"limit": 5000, "remaining": 4999, "reset": 1700000000}
                    }
                }
            )
        ]
    )
    status = client.rate_limit()
    assert status.resource == "core"
    assert status.limit == 5000
    assert status.remaining == 4999
    assert status.reset_epoch == 1700000000


def test_rate_limit_from_headers():
    status = GitHubRESTClient.rate_limit_from_headers(
        {
            "X-RateLimit-Limit": "60",
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": "1700000000",
        }
    )
    assert status is not None
    assert status.remaining == 0


def test_rate_limit_from_headers_absent():
    assert GitHubRESTClient.rate_limit_from_headers({}) is None


def test_paginate_follows_next_links():
    link = (
        '<https://api.github.com/repos/o/r/releases?page=2>; rel="next", '
        '<https://api.github.com/repos/o/r/releases?page=2>; rel="last"'
    )
    client, session = _client(
        [
            FakeResponse(json_data=[{"id": 1}], headers={"Link": link}),
            FakeResponse(json_data=[{"id": 2}]),
        ]
    )
    items = list(client.paginate("/repos/o/r/releases"))
    assert items == [{"id": 1}, {"id": 2}]
    assert session.requests[0]["params"]["per_page"] == 100
    assert session.requests[1]["url"] == (
        "https://api.github.com/repos/o/r/releases?page=2"
    )
    assert session.requests[1]["params"] is None


def test_paginate_stops_without_next_link():
    client, session = _client([FakeResponse(json_data=[{"id": 1}])])
    items = list(client.paginate("/repos/o/r/releases"))
    assert items == [{"id": 1}]
    assert len(session.requests) == 1


def test_paginate_unwraps_search_items():
    client, _ = _client(
        [FakeResponse(json_data={"total_count": 1, "items": [{"full_name": "a/b"}]})]
    )
    items = list(client.paginate("/search/repositories", params={"q": "stars:>1000"}))
    assert items == [{"full_name": "a/b"}]


def test_paginate_passes_custom_params():
    client, session = _client([FakeResponse(json_data=[])])
    list(client.paginate("/repos/o/r/runs", params={"event": "push"}, per_page=50))
    assert session.requests[0]["params"] == {"event": "push", "per_page": 50}


def test_paginate_field_follows_next_links():
    link = '<https://api.github.com/repos/o/r/compare/a...b?page=2>; rel="next"'
    client, session = _client(
        [
            FakeResponse(json_data={"commits": [{"sha": "1"}]}, headers={"Link": link}),
            FakeResponse(json_data={"commits": [{"sha": "2"}]}),
        ]
    )
    items = list(client.paginate_field("/repos/o/r/compare/a...b", "commits", per_page=250))
    assert items == [{"sha": "1"}, {"sha": "2"}]
    assert session.requests[0]["params"]["per_page"] == 250
    assert session.requests[1]["params"] is None


def test_paginate_field_raises_on_error_status():
    client, _ = _client([FakeResponse(status_code=404, text="Not Found")])
    with pytest.raises(GitHubHTTPError) as ctx:
        list(client.paginate_field("/repos/o/r/compare/a...b", "commits"))
    assert ctx.value.status == 404


def test_paginate_field_missing_key_yields_nothing():
    client, _ = _client([FakeResponse(json_data={"other": []})])
    assert list(client.paginate_field("/repos/o/r/compare/a...b", "commits")) == []


def test_parse_link_header():
    links = parse_link_header('<https://a>; rel="next", <https://b>; rel="last"')
    assert links == {"next": "https://a", "last": "https://b"}


def test_parse_link_header_empty():
    assert parse_link_header("") == {}
