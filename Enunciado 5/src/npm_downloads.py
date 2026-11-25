"""Séries históricas de downloads dos gerenciadores na API pública do npm (2º caminho).

Este é o caminho "analisar dados de operação" da proposta (§3.3): enquanto o experimento mede
desempenho nas 3 máquinas do grupo, aqui medimos **adoção** pela série diária de downloads de
`npm`, `pnpm`, `yarn`, `@yarnpkg/cli` e `bun` no registry público.

O que o módulo garante:

- **Janela em blocos.** A API aceita no máximo ~550 dias por chamada e, acima disso, **corta sem
  avisar**: pedir `2022-01-01:2023-12-31` devolve `start = 2022-06-30`. Por isso a janela é
  partida em blocos de `BLOCK_DAYS` (500) e cada bloco é conferido contra o que foi pedido.
- **≤ 1 requisição por segundo** (`SLEEP_S`), com `retry` e espera crescente em 429/5xx.
- **Cache em CSV.** `data/npm_downloads/downloads_daily.csv` é a verdade; rodar de novo só busca
  os dias que faltam (da última linha de cada pacote até ontem). `--refresh` refaz tudo.
- **Data da coleta registrada** em `downloads_meta.csv` (`fetched_at`, por pacote).

Ameaça de construto (documentada em `docs/fonte_downloads.md`): **download do pacote ≠ uso do
gerenciador**. O caso mais grave é o próprio `npm`, que **já vem junto com o Node.js** — quem usa
npm quase nunca baixa o pacote `npm`. A série do npm é, portanto, um piso grosseiro, e a
comparação direta de níveis entre o npm e os demais não se sustenta.

Uso: `uv run lab05 downloads [--refresh] [--since 2015-01-10] [--until 2026-11-23]`

Issue: #112 (T15).
"""

from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Iterator
from datetime import date, datetime, timedelta
from pathlib import Path

from config import DATA_DOWNLOADS

SCHEMA_VERSION = 1

API = "https://api.npmjs.org/downloads/range"
USER_AGENT = "lab05-academic-research (+leitura; 1 req/s)"

# Pacotes consultados -> como eles se ligam aos tratamentos do experimento.
# `treatments` tem mais de um id quando o pacote não distingue as variantes (o linker do Berry é
# configuração, não pacote).
#
# `tool_from` é o dia em que o **nome** passou a servir a ferramenta que medimos. Três dos cinco
# nomes já existiam no registry, ocupados por pacotes sem nenhuma relação, e só foram assumidos
# anos depois — `bun` foi criado em 2013-03-13 e o Bun 1.0.0 saiu em 2023-09-08. Os downloads
# anteriores são de outro software e **não** são adoção do gerenciador. A coleta guarda a série
# inteira (não apagamos dado bruto) e marca cada dia na coluna `tool_era`; a análise filtra.
# Datas obtidas do campo `time` de `https://registry.npmjs.org/<pacote>`, no primeiro release
# depois do hiato de anos: pnpm 0.16.0 (hiato de 1059 dias), yarn 0.15.1 (1624 dias),
# bun 1.0.0, @yarnpkg/cli 2.0.0-rc.4.
PACKAGES: dict[str, dict] = {
    "npm": {
        "label": "npm",
        "family": "npm",
        "treatments": ("npm",),
        "tool_from": date(2013, 7, 12),       # antes do início dos dados da API
        "caveat": "Já vem instalado com o Node.js: a série subestima muito o uso real.",
    },
    "pnpm": {
        "label": "pnpm",
        "family": "pnpm",
        "treatments": ("pnpm",),
        "tool_from": date(2016, 2, 1),        # 0.16.0; o 0.0.1 de 2013 é de outro pacote
        "caveat": "Também é instalável por Corepack e por script standalone, fora do registry.",
    },
    "bun": {
        "label": "Bun",
        "family": "bun",
        "treatments": ("bun",),
        "tool_from": date(2023, 9, 8),        # 1.0.0; o nome era de outro pacote desde 2013
        "caveat": "O caminho recomendado de instalação é o script oficial / Homebrew, não o npm.",
    },
    "yarn": {
        "label": "Yarn (pacote 1.x)",
        "family": "yarn",
        "treatments": ("yarn-classic",),
        "tool_from": date(2016, 10, 11),      # 0.15.1, o lançamento público; o 0.1.0 de 2012 é outro
        "caveat": "É o pacote da linha 1.x, mas também é o atalho que o Berry usa; mistura os dois.",
    },
    "@yarnpkg/cli": {
        "label": "Yarn Berry (CLI)",
        "family": "yarn",
        "treatments": ("yarn-berry-nm", "yarn-berry-pnp"),
        "tool_from": date(2019, 9, 5),        # 2.0.0-rc.4, primeiro release do escopo
        "caveat": "O Berry costuma ser fixado por `yarnPath`/Corepack, sem passar pelo registry.",
    },
}

# A API não tem dados antes disto e responde "end date > start date" se pedirmos.
DATA_START = date(2015, 1, 10)
BLOCK_DAYS = 500          # a API corta acima de ~550 dias por chamada
SLEEP_S = 2.0             # bem acima do mínimo de 1 req/s: a API devolve 429 com 1,1 s
MAX_TRIES = 5
BACKOFF_S = 30.0          # espera depois de um 429, multiplicada a cada tentativa
TIMEOUT_S = 60

DAILY_CSV = DATA_DOWNLOADS / "downloads_daily.csv"
WEEKLY_CSV = DATA_DOWNLOADS / "downloads_weekly.csv"
META_CSV = DATA_DOWNLOADS / "downloads_meta.csv"

DAILY_COLUMNS = ("package", "day", "downloads", "tool_era")
WEEKLY_COLUMNS = ("package", "week_start", "downloads", "days", "complete_week", "tool_era")
META_COLUMNS = ("package", "label", "family", "treatments", "tool_from", "first_day", "last_day",
                "days", "total_downloads", "tool_era_days", "tool_era_downloads", "fetched_at",
                "schema_version", "source_url", "caveat")


# ---------------------------------------------------------------- linha da série


def tool_era(package: str, day: str | date) -> bool:
    """O dia já pertence à ferramenta que medimos, ou ainda é do pacote homônimo anterior?"""
    when = date.fromisoformat(day) if isinstance(day, str) else day
    info = PACKAGES.get(package)
    return True if info is None else when >= info["tool_from"]


def row(package: str, day: str, downloads: int) -> dict:
    """Uma linha diária, já com `tool_era` calculado a partir de `PACKAGES`."""
    return {"package": package, "day": day, "downloads": int(downloads),
            "tool_era": tool_era(package, day)}


# ---------------------------------------------------------------- HTTP


def _get_json(url: str, timeout: float = TIMEOUT_S) -> dict:
    """GET com `User-Agent` genérico. Separado para os testes trocarem por um dublê."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                                   "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 (https fixo)
        return json.loads(response.read().decode("utf-8"))


def _retry_after(exc: urllib.error.HTTPError) -> float | None:
    """Segundos pedidos no cabeçalho `Retry-After`, quando o servidor manda um número."""
    raw = (exc.headers or {}).get("Retry-After") if getattr(exc, "headers", None) else None
    try:
        return max(1.0, float(str(raw).strip()))
    except (TypeError, ValueError):
        return None


def fetch_block(package: str, start: date, end: date, tries: int = MAX_TRIES) -> list[dict]:
    """Um bloco da série diária de `package`, entre `start` e `end` (ambos inclusive).

    Devolve `[{"day": "AAAA-MM-DD", "downloads": int}, ...]`, possivelmente vazio (pacote sem
    downloads nesse intervalo, ou anterior ao primeiro release). Erros de rede e 429/5xx são
    repetidos esperando o `Retry-After` da resposta, ou `BACKOFF_S` crescente quando ele não vem;
    o erro da própria API (campo `error`, que chega com HTTP 200) sobe como `RuntimeError`.
    """
    url = f"{API}/{start.isoformat()}:{end.isoformat()}/{urllib.parse.quote(package, safe='')}"
    for attempt in range(1, tries + 1):
        try:
            payload = _get_json(url)
            break
        except urllib.error.HTTPError as exc:
            if exc.code == 404:        # pacote sem dados na janela
                return []
            if exc.code not in (429, 500, 502, 503, 504) or attempt == tries:
                raise
            # o `Retry-After` da API costuma vir 0: ele pode aumentar a espera, nunca encurtá-la
            espera = max(_retry_after(exc) or 0.0, BACKOFF_S * attempt)
            print(f"[downloads] HTTP {exc.code} em {package} {start}: esperando {espera:.0f} s "
                  f"(tentativa {attempt}/{tries})")
            time.sleep(espera)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            if attempt == tries:
                raise
            time.sleep(BACKOFF_S * attempt)
    else:                              # pragma: no cover - o `break`/`raise` sempre sai antes
        return []

    if "error" in payload:
        message = str(payload["error"])
        if "no stats" in message.lower() or "not found" in message.lower():
            return []
        raise RuntimeError(f"{package} {start}:{end}: {message}")

    days = payload.get("downloads") or []
    return [{"day": d["day"], "downloads": int(d["downloads"] or 0)} for d in days]


def blocks(start: date, end: date, size: int = BLOCK_DAYS) -> Iterator[tuple[date, date]]:
    """Parte `[start, end]` em pedaços de no máximo `size` dias (a API corta acima de ~550)."""
    cursor = start
    while cursor <= end:
        stop = min(cursor + timedelta(days=size - 1), end)
        yield cursor, stop
        cursor = stop + timedelta(days=1)


def fetch_series(package: str, start: date, end: date, sleep_s: float = SLEEP_S,
                 verbose: bool = True,
                 on_block: Callable[[list[dict]], None] | None = None) -> list[dict]:
    """Série diária completa de `package` no intervalo, bloco por bloco, respeitando o limite.

    `on_block` recebe as linhas de cada bloco assim que ele chega, para quem chama poder salvar o
    progresso: se a API cortar a coleta no meio (429), o que já veio não se perde. Dias repetidos
    entre blocos (não deveria haver) ficam com o último valor lido, e o resultado sai ordenado
    por data.
    """
    by_day: dict[str, int] = {}
    for i, (block_start, block_end) in enumerate(blocks(start, end)):
        if i:
            time.sleep(sleep_s)
        rows = fetch_block(package, block_start, block_end)
        for item in rows:
            by_day[item["day"]] = item["downloads"]
        if on_block is not None:
            on_block([row(package, r["day"], r["downloads"]) for r in rows])
        if verbose:
            print(f"[downloads] {package:<13} {block_start}..{block_end}: {len(rows):>4} dias")
    return [row(package, day, by_day[day]) for day in sorted(by_day)]


# ---------------------------------------------------------------- cache em CSV


def read_daily(path: Path = DAILY_CSV) -> list[dict]:
    """O cache diário já coletado (vazio se o arquivo não existe), com `tool_era` recalculado."""
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        # `tool_era` é recalculado, nunca lido: se uma data de `PACKAGES` for corrigida, o CSV
        # antigo não carrega a marca errada para a frente.
        return [row(r["package"], r["day"], int(r["downloads"])) for r in csv.DictReader(handle)]


def last_day(rows: list[dict], package: str) -> date | None:
    """Último dia já em cache para `package`, ou `None` se não há nada dele."""
    days = [r["day"] for r in rows if r["package"] == package]
    return date.fromisoformat(max(days)) if days else None


def merge(cached: list[dict], fresh: list[dict]) -> list[dict]:
    """Une cache e coleta nova; em caso de empate (pacote, dia), a coleta nova vence."""
    by_key = {(r["package"], r["day"]): r for r in cached}
    by_key.update({(r["package"], r["day"]): r for r in fresh})
    return [by_key[k] for k in sorted(by_key, key=lambda k: (list(PACKAGES).index(k[0])
                                                             if k[0] in PACKAGES else 99, k[1]))]


def write_csv(path: Path, columns: tuple[str, ...], rows: list[dict]) -> Path:
    """Grava `rows` em CSV com `columns` na ordem dada, criando a pasta se preciso."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return path


# ---------------------------------------------------------------- derivados


def weekly(rows: list[dict]) -> list[dict]:
    """Soma por semana ISO (segunda a domingo), com `complete_week` para as bordas.

    Semana incompleta não é apagada — a análise (T16) decide se usa; mas fica marcada, porque a
    primeira e a última semana da janela somam menos dias e enganam num gráfico de linha.
    `tool_era` vale para a segunda-feira da semana (ver `PACKAGES`).
    """
    buckets: dict[tuple[str, str], list[int]] = {}
    for item in rows:
        day = date.fromisoformat(item["day"])
        monday = (day - timedelta(days=day.weekday())).isoformat()
        buckets.setdefault((item["package"], monday), []).append(item["downloads"])
    return [
        {"package": package, "week_start": monday, "downloads": sum(values),
         "days": len(values), "complete_week": len(values) == 7,
         "tool_era": tool_era(package, monday)}
        for (package, monday), values in sorted(
            buckets.items(),
            key=lambda kv: (list(PACKAGES).index(kv[0][0]) if kv[0][0] in PACKAGES else 99,
                            kv[0][1]),
        )
    ]


def meta(rows: list[dict], fetched_at: str) -> list[dict]:
    """Uma linha por pacote: cobertura, totais (bruto e na era da ferramenta) e a data da coleta."""
    out = []
    for package, info in PACKAGES.items():
        meus = [r for r in rows if r["package"] == package]
        days = sorted(r["day"] for r in meus)
        era = [r for r in meus if tool_era(package, r["day"])]
        out.append({
            "package": package,
            "label": info["label"],
            "family": info["family"],
            "treatments": " ".join(info["treatments"]),
            "tool_from": info["tool_from"].isoformat(),
            "first_day": days[0] if days else "",
            "last_day": days[-1] if days else "",
            "days": len(days),
            "total_downloads": sum(r["downloads"] for r in meus),
            "tool_era_days": len(era),
            "tool_era_downloads": sum(r["downloads"] for r in era),
            "fetched_at": fetched_at,
            "schema_version": SCHEMA_VERSION,
            "source_url": f"{API}/<inicio>:<fim>/{package}",
            "caveat": info["caveat"],
        })
    return out


def gaps(rows: list[dict]) -> dict[str, int]:
    """Dias faltando entre o primeiro e o último dia de cada pacote (deveria ser 0)."""
    out = {}
    for package in PACKAGES:
        days = sorted(date.fromisoformat(r["day"]) for r in rows if r["package"] == package)
        if len(days) >= 2:
            esperados = (days[-1] - days[0]).days + 1
            if esperados != len(days):
                out[package] = esperados - len(days)
    return out


# ---------------------------------------------------------------- orquestração


def collect(until: date | None = None, since: date = DATA_START, refresh: bool = False,
            sleep_s: float = SLEEP_S, path: Path = DAILY_CSV, verbose: bool = True,
            checkpoint: bool = True) -> list[dict]:
    """Coleta (ou completa) a série de todos os pacotes e devolve as linhas diárias unidas.

    Sem `refresh`, cada pacote é buscado só do dia seguinte ao último em cache até `until`, e um
    pacote já em dia não gera requisição nenhuma. Com `checkpoint`, o CSV é regravado a cada
    bloco: se a coleta morrer no meio (429 insistente, queda de rede), rodar de novo continua de
    onde parou em vez de recomeçar do zero.
    """
    end = until or date.today() - timedelta(days=1)   # a API só fecha o dia anterior
    cached = [] if refresh else read_daily(path)
    fresh: list[dict] = []

    def salvar(got: list[dict]) -> None:
        fresh.extend(got)
        if checkpoint:
            write_csv(path, DAILY_COLUMNS, merge(cached, fresh))

    for package in PACKAGES:
        known = None if refresh else last_day(cached, package)
        start = max(since, known + timedelta(days=1)) if known else since
        if start > end:
            if verbose:
                print(f"[downloads] {package:<13} em dia (até {known})")
            continue
        fetch_series(package, start, end, sleep_s=sleep_s, verbose=verbose, on_block=salvar)
    return merge(cached, fresh)


def _milhar(valor: int) -> str:
    """Número com ponto de milhar, como se escreve em português."""
    return f"{valor:,}".replace(",", ".")


def summary(rows: list[dict], meta_rows: list[dict]) -> str:
    """Resumo de uma linha por pacote, para o terminal."""
    lines = [f"[downloads] {len(rows)} linhas diárias em {len(PACKAGES)} pacotes"]
    for m in meta_rows:
        janela = f"{m['first_day']}..{m['last_day']}" if m["days"] else "sem dados"
        lines.append(f"  {m['package']:<13} {janela:<24} {m['days']:>5} dias  "
                     f"{_milhar(m['total_downloads']):>17} downloads  "
                     f"(era da ferramenta, de {m['tool_from']}: "
                     f"{_milhar(m['tool_era_downloads'])})")
    faltando = gaps(rows)
    if faltando:
        lines.append(f"  ATENÇÃO: dias faltando na série: {faltando}")
    return "\n".join(lines)


def _short(path: Path) -> str:
    """Caminho relativo à raiz do projeto, ou o caminho inteiro se estiver fora dela."""
    try:
        return str(path.relative_to(DATA_DOWNLOADS.parents[1]))
    except ValueError:
        return str(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="lab05 downloads",
        description="Séries de downloads dos gerenciadores na API pública do npm (T15, #112).",
    )
    parser.add_argument("--since", type=date.fromisoformat, default=DATA_START,
                        help=f"primeiro dia da janela (padrão: {DATA_START}, início dos dados)")
    parser.add_argument("--until", type=date.fromisoformat, default=None,
                        help="último dia da janela (padrão: ontem; a API não fecha o dia de hoje)")
    parser.add_argument("--refresh", action="store_true",
                        help="ignora o cache e recoleta a janela inteira")
    parser.add_argument("--sleep", type=float, default=SLEEP_S, dest="sleep_s",
                        help=f"espera entre requisições, em segundos (padrão: {SLEEP_S})")
    parser.add_argument("--quiet", action="store_true", help="não imprime bloco por bloco")
    args = parser.parse_args([] if argv is None else argv)

    if args.sleep_s < 1.0:
        parser.error("--sleep não pode ser menor que 1.0: a regra da T15 é ≤ 1 requisição/s")

    rows = collect(until=args.until, since=args.since, refresh=args.refresh,
                   sleep_s=args.sleep_s, verbose=not args.quiet)
    if not rows:
        print("[downloads] nada coletado: confira a conexão e a janela pedida")
        return 1

    fetched_at = datetime.now().astimezone().isoformat(timespec="seconds")
    meta_rows = meta(rows, fetched_at)
    write_csv(DAILY_CSV, DAILY_COLUMNS, rows)
    write_csv(WEEKLY_CSV, WEEKLY_COLUMNS, weekly(rows))
    write_csv(META_CSV, META_COLUMNS, meta_rows)

    print(summary(rows, meta_rows))
    for path in (DAILY_CSV, WEEKLY_CSV, META_CSV):
        print(f"[downloads] {_short(path)}")
    return 0


if __name__ == "__main__":
    import sys

    raise SystemExit(main(sys.argv[1:]))
