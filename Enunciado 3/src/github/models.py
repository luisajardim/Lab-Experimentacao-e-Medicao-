"""Modelos de dados da API do GitHub (dataclasses + parsers puros)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Repository:
    """Metadados de repositório relevantes ao funil de seleção."""

    full_name: str
    html_url: str
    stars: int
    language: str | None
    default_branch: str
    created_at: str
    pushed_at: str | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Repository:
        return cls(
            full_name=data["full_name"],
            html_url=data["html_url"],
            stars=int(data["stargazers_count"]),
            language=data.get("language"),
            default_branch=data["default_branch"],
            created_at=data["created_at"],
            pushed_at=data.get("pushed_at"),
        )

    @classmethod
    def from_graphql(cls, data: dict[str, Any]) -> Repository:
        language = (data.get("primaryLanguage") or {}).get("name")
        branch = (data.get("defaultBranchRef") or {}).get("name") or "main"
        return cls(
            full_name=data["nameWithOwner"],
            html_url=data["url"],
            stars=int(data["stargazerCount"]),
            language=language,
            default_branch=branch,
            created_at=data["createdAt"],
            pushed_at=data.get("pushedAt"),
        )


@dataclass(frozen=True)
class Release:
    """Release; ``draft=false`` é a unidade de deploy (ENUNCIADO §3)."""

    id: int
    tag_name: str
    name: str | None
    draft: bool
    prerelease: bool
    published_at: str | None
    html_url: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Release:
        return cls(
            id=int(data["id"]),
            tag_name=data["tag_name"],
            name=data.get("name"),
            draft=bool(data["draft"]),
            prerelease=bool(data["prerelease"]),
            published_at=data.get("published_at"),
            html_url=data["html_url"],
        )


@dataclass(frozen=True)
class Commit:
    """Commit; ``author_date`` é ``commit.author.date`` (quando foi escrita)."""

    sha: str
    author_date: str
    message: str
    html_url: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Commit:
        commit = data.get("commit") or {}
        author = commit.get("author") or {}
        return cls(
            sha=data["sha"],
            author_date=author.get("date", ""),
            message=commit.get("message", ""),
            html_url=data.get("html_url", ""),
        )


@dataclass(frozen=True)
class Workflow:
    """Workflow (definição) de um repositório."""

    id: int
    name: str
    path: str
    state: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Workflow:
        return cls(
            id=int(data["id"]),
            name=data["name"],
            path=data["path"],
            state=data["state"],
        )


@dataclass(frozen=True)
class WorkflowRun:
    """Execução de workflow (CI) no default branch."""

    id: int
    name: str
    workflow_id: int
    branch: str
    event: str
    status: str
    conclusion: str | None
    run_started_at: str
    updated_at: str
    html_url: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> WorkflowRun:
        return cls(
            id=int(data["id"]),
            name=data["name"],
            workflow_id=int(data["workflow_id"]),
            branch=data.get("head_branch") or "",
            event=data["event"],
            status=data["status"],
            conclusion=data.get("conclusion"),
            run_started_at=data["run_started_at"],
            updated_at=data["updated_at"],
            html_url=data["html_url"],
        )


@dataclass(frozen=True)
class Tag:
    """Tag (não traz data: o coletor resolve via commit apontado)."""

    name: str
    sha: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Tag:
        commit = data.get("commit") or {}
        return cls(name=data["name"], sha=commit.get("sha", ""))


@dataclass(frozen=True)
class RateLimitStatus:
    """Cota de um recurso (ex.: ``core``, ``search``)."""

    limit: int
    remaining: int
    reset_epoch: int
    resource: str = "core"
