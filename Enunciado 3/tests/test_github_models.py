"""Testes dos modelos de dados (parsing puro, sem rede)."""

import pytest

from github.models import Commit, Release, Repository, Tag, Workflow, WorkflowRun


def _repo_payload(**overrides):
    payload = {
        "full_name": "octocat/Hello-World",
        "html_url": "https://github.com/octocat/Hello-World",
        "stargazers_count": 1234,
        "language": "Python",
        "default_branch": "main",
        "created_at": "2011-01-26T19:01:12Z",
        "pushed_at": "2026-01-01T00:00:00Z",
    }
    payload.update(overrides)
    return payload


def test_repository_from_api():
    repo = Repository.from_api(_repo_payload())
    assert repo.full_name == "octocat/Hello-World"
    assert repo.stars == 1234
    assert repo.language == "Python"
    assert repo.default_branch == "main"
    assert repo.created_at == "2011-01-26T19:01:12Z"
    assert repo.pushed_at == "2026-01-01T00:00:00Z"


def test_repository_without_language():
    repo = Repository.from_api(_repo_payload(language=None))
    assert repo.language is None


def test_repository_from_graphql():
    repo = Repository.from_graphql(
        {
            "nameWithOwner": "octocat/Hello-World",
            "url": "https://github.com/octocat/Hello-World",
            "stargazerCount": 1234,
            "primaryLanguage": {"name": "Python"},
            "defaultBranchRef": {"name": "main"},
            "createdAt": "2011-01-26T19:01:12Z",
            "pushedAt": "2026-01-01T00:00:00Z",
        }
    )
    assert repo.full_name == "octocat/Hello-World"
    assert repo.stars == 1234
    assert repo.default_branch == "main"


def test_release_from_api():
    release = Release.from_api(
        {
            "id": 151,
            "tag_name": "v2.3.1",
            "name": "fix: crash",
            "draft": False,
            "prerelease": False,
            "published_at": "2026-03-15T10:00:00Z",
            "html_url": "https://github.com/o/r/releases/tag/v2.3.1",
        }
    )
    assert release.tag_name == "v2.3.1"
    assert release.draft is False
    assert release.prerelease is False
    assert release.published_at == "2026-03-15T10:00:00Z"


def test_commit_uses_author_date():
    commit = Commit.from_api(
        {
            "sha": "abc123",
            "html_url": "https://github.com/o/r/commit/abc123",
            "commit": {
                "message": "fix: crash ao abrir arquivo",
                "author": {"date": "2026-03-02T12:00:00Z", "name": "A"},
            },
        }
    )
    assert commit.sha == "abc123"
    assert commit.author_date == "2026-03-02T12:00:00Z"
    assert commit.message == "fix: crash ao abrir arquivo"


def test_workflow_run_from_api():
    run = WorkflowRun.from_api(
        {
            "id": 9001,
            "name": "CI",
            "workflow_id": 77,
            "head_branch": "main",
            "event": "push",
            "status": "completed",
            "conclusion": "failure",
            "run_started_at": "2026-05-10T10:00:00Z",
            "updated_at": "2026-05-10T11:20:00Z",
            "html_url": "https://github.com/o/r/actions/runs/9001",
        }
    )
    assert run.branch == "main"
    assert run.event == "push"
    assert run.conclusion == "failure"
    assert run.run_started_at == "2026-05-10T10:00:00Z"


def test_tag_from_api():
    tag = Tag.from_api({"name": "v1.0.0", "commit": {"sha": "deadbeef", "url": "u"}})
    assert tag.name == "v1.0.0"
    assert tag.sha == "deadbeef"


def test_workflow_from_api():
    workflow = Workflow.from_api(
        {
            "id": 77,
            "name": "CI",
            "path": ".github/workflows/ci.yml",
            "state": "active",
        }
    )
    assert workflow.name == "CI"
    assert workflow.state == "active"


def test_models_are_immutable():
    from dataclasses import FrozenInstanceError

    repo = Repository.from_api(_repo_payload())
    with pytest.raises(FrozenInstanceError):
        repo.stars = 9999
