"""Cache SQLite content-addressed para respostas da API GitHub (PLAN T03).

Permite que uma coleta interrompida (rate limit, rede, Ctrl+C) retome sem
repetir chamadas já concluídas, e produz um relatório de *staleness*
(repositórios cuja assinatura mudou desde a última coleta de um estágio).

Chave de cache = hash de ``método + URL + body`` (``compute_url_hash``).
Estágios (``stage``) são uma etiqueta de texto livre definida pelo chamador
(ex.: ``"collect"``, ``"collect:releases"``) usada para retomada e limpeza
seletivas.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

Clock = Callable[[], str]


def _default_clock() -> str:
    return datetime.now(UTC).isoformat()


def compute_url_hash(method: str, url: str, body: str | None = None) -> str:
    """Hash content-addressed de ``método + URL + body``."""
    payload = f"{method.upper()}\n{url}\n{body or ''}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class CachedResponse:
    """Uma linha da tabela ``responses``."""

    url_hash: str
    url: str
    method: str
    body: str | None
    status: int
    response_body: str
    stage: str
    fetched_at: str


@dataclass(frozen=True)
class StalenessReport:
    """Resultado de ``write_staleness_report``: quantos itens mudaram."""

    stage: str
    total: int
    stale_count: int
    stale_keys: list[str]
    generated_at: str

    def to_dict(self) -> dict:
        return asdict(self)


class SQLiteStore:
    """Cache content-addressed + controle de retomada por estágio."""

    def __init__(self, db_path: str | Path, *, clock: Clock | None = None) -> None:
        self._path = Path(db_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._clock = clock or _default_clock
        self._conn = sqlite3.connect(self._path)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS responses (
                url_hash TEXT PRIMARY KEY,
                url TEXT NOT NULL,
                method TEXT NOT NULL,
                body TEXT,
                status INTEGER NOT NULL,
                response_body TEXT NOT NULL,
                stage TEXT NOT NULL,
                fetched_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_responses_stage ON responses(stage);

            CREATE TABLE IF NOT EXISTS stages (
                name TEXT PRIMARY KEY,
                completed_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS signatures (
                stage TEXT NOT NULL,
                key TEXT NOT NULL,
                signature TEXT NOT NULL,
                recorded_at TEXT NOT NULL,
                PRIMARY KEY (stage, key)
            );
            """
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> SQLiteStore:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    # --- cache content-addressed ----------------------------------------

    def get(self, method: str, url: str, body: str | None = None) -> CachedResponse | None:
        """Devolve a resposta em cache para ``método+URL+body``, se houver."""
        url_hash = compute_url_hash(method, url, body)
        row = self._conn.execute(
            "SELECT url_hash, url, method, body, status, response_body, stage, fetched_at "
            "FROM responses WHERE url_hash = ?",
            (url_hash,),
        ).fetchone()
        if row is None:
            return None
        return CachedResponse(**dict(row))

    def put(
        self,
        method: str,
        url: str,
        body: str | None,
        status: int,
        response_body: str,
        *,
        stage: str,
    ) -> CachedResponse:
        """Persiste (ou substitui) a resposta para ``método+URL+body``."""
        url_hash = compute_url_hash(method, url, body)
        fetched_at = self._clock()
        self._conn.execute(
            """
            INSERT INTO responses
                (url_hash, url, method, body, status, response_body, stage, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(url_hash) DO UPDATE SET
                status = excluded.status,
                response_body = excluded.response_body,
                stage = excluded.stage,
                fetched_at = excluded.fetched_at
            """,
            (url_hash, url, method.upper(), body, status, response_body, stage, fetched_at),
        )
        self._conn.commit()
        return CachedResponse(
            url_hash=url_hash,
            url=url,
            method=method.upper(),
            body=body,
            status=status,
            response_body=response_body,
            stage=stage,
            fetched_at=fetched_at,
        )

    # --- retomada por estágio --------------------------------------------

    def is_stage_complete(self, stage: str) -> bool:
        """``True`` se ``mark_stage_complete(stage)`` já foi chamado."""
        row = self._conn.execute(
            "SELECT 1 FROM stages WHERE name = ?", (stage,)
        ).fetchone()
        return row is not None

    def mark_stage_complete(self, stage: str) -> None:
        """Marca um estágio como concluído (retomadas futuras o pulam)."""
        self._conn.execute(
            "INSERT INTO stages (name, completed_at) VALUES (?, ?) "
            "ON CONFLICT(name) DO UPDATE SET completed_at = excluded.completed_at",
            (stage, self._clock()),
        )
        self._conn.commit()

    def clear_stage(self, stage: str) -> None:
        """Remove respostas, assinaturas e a marca de conclusão de um estágio."""
        self._conn.execute("DELETE FROM responses WHERE stage = ?", (stage,))
        self._conn.execute("DELETE FROM signatures WHERE stage = ?", (stage,))
        self._conn.execute("DELETE FROM stages WHERE name = ?", (stage,))
        self._conn.commit()

    # --- staleness --------------------------------------------------------

    def record_signature(self, stage: str, key: str, signature: str) -> None:
        """Registra a assinatura atual (ex.: ``pushed_at``) de ``key`` no estágio.

        Chamar ao final de uma coleta bem-sucedida, para servir de base de
        comparação na próxima execução de ``get_stale``/``write_staleness_report``.
        """
        self._conn.execute(
            "INSERT INTO signatures (stage, key, signature, recorded_at) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(stage, key) DO UPDATE SET "
            "signature = excluded.signature, recorded_at = excluded.recorded_at",
            (stage, key, signature, self._clock()),
        )
        self._conn.commit()

    def get_stale(self, stage: str, current_signatures: dict[str, str]) -> list[str]:
        """Chaves novas ou cuja assinatura mudou desde o último ``record_signature``."""
        rows = self._conn.execute(
            "SELECT key, signature FROM signatures WHERE stage = ?", (stage,)
        ).fetchall()
        previous = {row["key"]: row["signature"] for row in rows}
        stale = [
            key
            for key, signature in current_signatures.items()
            if previous.get(key) != signature
        ]
        return sorted(stale)

    def write_staleness_report(
        self, path: str | Path, stage: str, current_signatures: dict[str, str]
    ) -> StalenessReport:
        """Calcula a staleness do estágio e grava o relatório em ``path`` (JSON)."""
        stale_keys = self.get_stale(stage, current_signatures)
        report = StalenessReport(
            stage=stage,
            total=len(current_signatures),
            stale_count=len(stale_keys),
            stale_keys=stale_keys,
            generated_at=self._clock(),
        )
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return report
