"""Testes do cache SQLite content-addressed (sem rede)."""

import json

import pytest

from cache.sqlite_store import SQLiteStore, compute_url_hash


@pytest.fixture
def store(tmp_path):
    clock = iter(f"2026-01-01T00:00:{i:02d}Z" for i in range(1000))
    db_path = tmp_path / "cache" / "api_responses.db"
    with SQLiteStore(db_path, clock=lambda: next(clock)) as store:
        yield store


def test_compute_url_hash_is_stable():
    a = compute_url_hash("GET", "/repos/o/r")
    b = compute_url_hash("GET", "/repos/o/r")
    assert a == b
    assert a != compute_url_hash("GET", "/repos/o/other")


def test_compute_url_hash_normalizes_method_case():
    assert compute_url_hash("get", "/x") == compute_url_hash("GET", "/x")


def test_compute_url_hash_distinguishes_body():
    a = compute_url_hash("POST", "/graphql", '{"query":"a"}')
    b = compute_url_hash("POST", "/graphql", '{"query":"b"}')
    assert a != b


def test_get_misses_when_empty(store):
    assert store.get("GET", "/repos/o/r") is None


def test_put_then_get_round_trips(store):
    store.put("GET", "/repos/o/r", None, 200, '{"ok": true}', stage="collect")
    cached = store.get("GET", "/repos/o/r")
    assert cached is not None
    assert cached.status == 200
    assert cached.response_body == '{"ok": true}'
    assert cached.stage == "collect"
    assert cached.fetched_at


def test_put_is_keyed_by_method_url_and_body(store):
    store.put("GET", "/repos/o/r", None, 200, "a", stage="collect")
    assert store.get("POST", "/repos/o/r") is None
    assert store.get("GET", "/repos/o/r", body="{}") is None


def test_put_overwrites_previous_entry_for_same_key(store):
    store.put("GET", "/repos/o/r", None, 500, "erro", stage="collect")
    store.put("GET", "/repos/o/r", None, 200, "ok", stage="collect")
    cached = store.get("GET", "/repos/o/r")
    assert cached.status == 200
    assert cached.response_body == "ok"


def test_stage_not_complete_by_default(store):
    assert store.is_stage_complete("collect") is False


def test_mark_stage_complete(store):
    store.mark_stage_complete("collect")
    assert store.is_stage_complete("collect") is True
    assert store.is_stage_complete("metrics") is False


def test_resume_skips_requests_already_cached(store):
    """Simula retomada: um 'cliente' só chama a rede se o cache não tiver a resposta."""
    calls = []

    def fetch_with_cache(method, url):
        cached = store.get(method, url)
        if cached is not None:
            return cached.response_body
        calls.append((method, url))
        body = '{"fetched": true}'
        store.put(method, url, None, 200, body, stage="collect")
        return body

    fetch_with_cache("GET", "/repos/o/r/releases")
    fetch_with_cache("GET", "/repos/o/r/releases")  # retomada: não deve repetir a chamada

    assert calls == [("GET", "/repos/o/r/releases")]


def test_clear_stage_removes_responses_signatures_and_completion(store):
    store.put("GET", "/repos/o/r", None, 200, "ok", stage="collect")
    store.mark_stage_complete("collect")
    store.record_signature("collect", "o/r", "2026-01-01T00:00:00Z")

    store.clear_stage("collect")

    assert store.get("GET", "/repos/o/r") is None
    assert store.is_stage_complete("collect") is False
    assert store.get_stale("collect", {"o/r": "2026-01-01T00:00:00Z"}) == ["o/r"]


def test_clear_stage_only_affects_that_stage(store):
    store.put("GET", "/a", None, 200, "ok", stage="collect")
    store.put("GET", "/b", None, 200, "ok", stage="metrics")

    store.clear_stage("collect")

    assert store.get("GET", "/a") is None
    assert store.get("GET", "/b") is not None


def test_get_stale_reports_new_keys_as_stale(store):
    assert store.get_stale("collect", {"o/r": "sig-1"}) == ["o/r"]


def test_get_stale_reports_changed_signature(store):
    store.record_signature("collect", "o/r", "sig-1")
    assert store.get_stale("collect", {"o/r": "sig-2"}) == ["o/r"]


def test_get_stale_excludes_unchanged_signature(store):
    store.record_signature("collect", "o/r", "sig-1")
    assert store.get_stale("collect", {"o/r": "sig-1"}) == []


def test_get_stale_is_scoped_per_stage(store):
    store.record_signature("collect", "o/r", "sig-1")
    assert store.get_stale("metrics", {"o/r": "sig-1"}) == ["o/r"]


def test_write_staleness_report_creates_json_file(store, tmp_path):
    store.record_signature("collect", "o/r1", "sig-1")
    report_path = tmp_path / "reports" / "staleness_collect.json"

    report = store.write_staleness_report(
        report_path, "collect", {"o/r1": "sig-1", "o/r2": "sig-new"}
    )

    assert report.stage == "collect"
    assert report.total == 2
    assert report.stale_count == 1
    assert report.stale_keys == ["o/r2"]

    on_disk = json.loads(report_path.read_text(encoding="utf-8"))
    assert on_disk["stale_count"] == 1
    assert on_disk["stale_keys"] == ["o/r2"]


def test_store_persists_across_reopen(tmp_path):
    db_path = tmp_path / "cache" / "api_responses.db"
    with SQLiteStore(db_path) as store:
        store.put("GET", "/repos/o/r", None, 200, "ok", stage="collect")
        store.mark_stage_complete("collect")

    with SQLiteStore(db_path) as reopened:
        assert reopened.get("GET", "/repos/o/r").response_body == "ok"
        assert reopened.is_stage_complete("collect") is True
