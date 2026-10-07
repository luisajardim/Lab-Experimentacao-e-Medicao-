"""Testes do cliente GraphQL (batching por aliases) com sessão falsa."""

import pytest
from _fakes import FakeResponse, FakeSession

from github.gql import GitHubGraphQLClient, GraphQLResponseError
from github.rest import GitHubHTTPError


def _client(responses, **kwargs):
    kwargs.setdefault("max_retries", 5)
    kwargs.setdefault("wall_clock", lambda: 1000.0)
    session = FakeSession(responses)
    client = GitHubGraphQLClient("token", session=session, **kwargs)
    return client, session


def test_batch_query_combines_operations_with_aliases():
    session = FakeSession(
        [
            FakeResponse(
                json_data={
                    "data": {
                        "op0": {"nameWithOwner": "a/b"},
                        "op1": {"nameWithOwner": "c/d"},
                    }
                }
            )
        ]
    )
    client = GitHubGraphQLClient("token", session=session, wall_clock=lambda: 1000.0)
    operations = {
        "a/b": "repository(owner: $owner0, name: $name0) { nameWithOwner }",
        "c/d": "repository(owner: $owner1, name: $name1) { nameWithOwner }",
    }
    variables = {"owner0": "a", "name0": "b", "owner1": "c", "name1": "d"}
    result = client.query(operations, variables)
    assert result == {"a/b": {"nameWithOwner": "a/b"}, "c/d": {"nameWithOwner": "c/d"}}
    sent = session.requests[0]["json"]
    assert sent["variables"] == variables
    assert "op0: repository(owner: $owner0, name: $name0)" in sent["query"]
    assert "op1: repository(owner: $owner1, name: $name1)" in sent["query"]
    assert (
        "query($owner0: String!, $name0: String!, $owner1: String!, $name1: String!)"
        in sent["query"]
    )


def test_identifier_keys_are_used_as_aliases():
    session = FakeSession([FakeResponse(json_data={"data": {"repo0": {"v": 1}}})])
    client = GitHubGraphQLClient("token", session=session, wall_clock=lambda: 1000.0)
    result = client.query({"repo0": "rateLimit { remaining }"})
    assert result == {"repo0": {"v": 1}}
    assert "repo0: rateLimit" in session.requests[0]["json"]["query"]


def test_batch_query_splits_into_multiple_requests():
    session = FakeSession(
        [
            FakeResponse(json_data={"data": {"repo0": {"v": 0}, "repo1": {"v": 1}}}),
            FakeResponse(json_data={"data": {"repo2": {"v": 2}}}),
        ]
    )
    client = GitHubGraphQLClient(
        "token", session=session, batch_size=2, wall_clock=lambda: 1000.0
    )
    operations = {f"repo{i}": f"node(id: $id{i}) {{ id }}" for i in range(3)}
    variables = {f"id{i}": f"id{i}" for i in range(3)}
    result = client.query(operations, variables)
    assert result == {"repo0": {"v": 0}, "repo1": {"v": 1}, "repo2": {"v": 2}}
    assert len(session.requests) == 2
    assert session.requests[0]["json"]["variables"] == {"id0": "id0", "id1": "id1"}
    assert session.requests[1]["json"]["variables"] == {"id2": "id2"}


def test_query_lenient_mode_returns_partial_data():
    session = FakeSession(
        [
            FakeResponse(
                json_data={
                    "errors": [{"message": "repository not found"}],
                    "data": {"op0": None},
                }
            )
        ]
    )
    client = GitHubGraphQLClient("token", session=session, wall_clock=lambda: 1000.0)
    operations = {"a/b": "repository(owner: $owner0, name: $name0) { nameWithOwner }"}
    result = client.query(operations, {"owner0": "a", "name0": "b"})
    assert result == {"a/b": None}


def test_query_strict_mode_raises():
    session = FakeSession([FakeResponse(json_data={"errors": [{"message": "nope"}], "data": {}})])
    client = GitHubGraphQLClient("token", session=session, wall_clock=lambda: 1000.0)
    with pytest.raises(GraphQLResponseError) as ctx:
        client.query({"x": "rateLimit { remaining }"}, strict=True)
    assert ctx.value.errors == [{"message": "nope"}]


def test_query_raises_on_http_error():
    session = FakeSession([FakeResponse(status_code=500, text="boom")])
    client = GitHubGraphQLClient(
        "token", session=session, max_retries=0, wall_clock=lambda: 1000.0
    )
    with pytest.raises(GitHubHTTPError):
        client.query({"x": "rateLimit { remaining }"})


def test_repositories_batches_and_maps_by_full_name():
    session = FakeSession(
        [
            FakeResponse(
                json_data={
                    "data": {
                        "op0": {"nameWithOwner": "a/b"},
                        "op1": {"nameWithOwner": "c/d"},
                    }
                }
            ),
            FakeResponse(json_data={"data": {"op0": {"nameWithOwner": "e/f"}}}),
        ]
    )
    client = GitHubGraphQLClient(
        "token", session=session, batch_size=2, wall_clock=lambda: 1000.0
    )
    result = client.repositories(["a/b", "c/d", "e/f"])
    assert result == {
        "a/b": {"nameWithOwner": "a/b"},
        "c/d": {"nameWithOwner": "c/d"},
        "e/f": {"nameWithOwner": "e/f"},
    }
    first = session.requests[0]["json"]
    assert "op0: repository(owner: $owner0, name: $name0)" in first["query"]
    assert "op1: repository(owner: $owner1, name: $name1)" in first["query"]
    assert first["variables"] == {
        "owner0": "a",
        "name0": "b",
        "owner1": "c",
        "name1": "d",
    }


def test_repositories_empty_list():
    client, session = _client([])
    assert client.repositories([]) == {}
    assert session.requests == []
