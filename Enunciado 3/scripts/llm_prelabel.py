#!/usr/bin/env python3
"""Pré-rotula a amostra-ouro com uma LLM, a partir dos dossiês já gerados.

Para cada repositório do template, envia o dossiê (``build_dossiers.py``) à API
da Anthropic e grava a sugestão em ``llm_suggestions.json``:

    {"owner/repo": {"project_type": ..., "delivers_to_user": ...,
                    "corrective": ["sim"|"não" x5], "reason": "..."}}

As sugestões NÃO viram rótulo sozinhas: o ``label_tool.py --suggestions`` mostra
cada uma e o humano aceita (Enter) ou edita. Declare o uso de LLM no artigo
(metodologia / ameaças à validade).

Requisitos: variável de ambiente ``ANTHROPIC_API_KEY`` (chave da API, diferente
da assinatura do claude.ai). Só biblioteca padrão. Retoma de onde parou.

Uso
---
    export ANTHROPIC_API_KEY=sk-ant-...
    python scripts/llm_prelabel.py --limit 3        # teste barato
    python scripts/llm_prelabel.py                  # os 60
    python scripts/label_tool.py --member A --suggestions data/gold/llm_suggestions.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from build_dossiers import dossier_filename, read_template

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GOLD_DIR = PROJECT_ROOT / "data" / "gold"
DEFAULT_MODEL = "claude-haiku-5-5"
DEFAULT_API_URL = "https://api.anthropic.com/v1/messages"

PROJECT_TYPES = ("biblioteca/framework", "aplicação/serviço", "ferramenta CLI", "outro")

SYSTEM_PROMPT = """Você ajuda a rotular repositórios de software open-source para um estudo sobre métricas DORA.
Receberá um dossiê com metadados, trecho do README e 5 releases (notas, assets e commits desde a release anterior).
Responda SOMENTE com um objeto JSON, sem texto extra, neste formato:
{"project_type": "biblioteca/framework" | "aplicação/serviço" | "ferramenta CLI" | "outro",
 "delivers_to_user": "sim" | "não" | "incerto",
 "corrective": ["sim"|"não", ... exatamente 5 itens, na ordem Release 1 a Release 5],
 "reason": "uma frase curta"}

Critérios:
- project_type: o que o projeto é, pelo README/descrição.
- delivers_to_user: "sim" se as releases entregam algo a quem usa o software (binários/instaladores nos assets, pacote em registry como pip/npm/Maven/crates, imagem Docker, app instalável); "não" se a release é só marco interno/tag sem entrega; "incerto" se não der para saber.
- corrective: "sim" se o objetivo PRINCIPAL da release é corrigir um defeito recente (bugfix/hotfix/revert, notas dominadas por correções); "não" para releases de funcionalidades, refatoração, dependências ou mistas sem foco em correção.
Baseie-se apenas no dossiê."""


def normalize(data: Any) -> dict[str, Any] | None:
    """Validate/clean one model answer; None if unusable."""
    if not isinstance(data, dict):
        return None

    def clean(value: Any) -> str:
        text = str(value).strip().lower()
        return {"nao": "não"}.get(text, text)

    project_type_raw = str(data.get("project_type", "")).strip().lower()
    project_type = {
        "biblioteca/framework": "biblioteca/framework",
        "biblioteca / framework": "biblioteca/framework",
        "library/framework": "biblioteca/framework",
        "library / framework": "biblioteca/framework",
        "aplicação/serviço": "aplicação/serviço",
        "aplicação / serviço": "aplicação/serviço",
        "aplicacao/servico": "aplicação/serviço",
        "aplicacao / servico": "aplicação/serviço",
        "application/service": "aplicação/serviço",
        "application / service": "aplicação/serviço",
        "ferramenta cli": "ferramenta CLI",
        "ferramenta de linha de comando": "ferramenta CLI",
        "cli tool": "ferramenta CLI",
        "command-line tool": "ferramenta CLI",
        "outro": "outro",
        "other": "outro",
    }.get(project_type_raw, project_type_raw)
    delivers = clean(data.get("delivers_to_user", ""))
    corrective = data.get("corrective")
    if project_type not in PROJECT_TYPES or delivers not in {"sim", "não", "incerto"}:
        return None
    if not isinstance(corrective, list) or len(corrective) != 5:
        return None
    corrective = [clean(item) for item in corrective]
    if any(item not in {"sim", "não"} for item in corrective):
        return None
    return {
        "project_type": project_type,
        "delivers_to_user": delivers,
        "corrective": corrective,
        "reason": str(data.get("reason", "")).strip(),
    }


def call_llm(
    api_url: str,
    api_key: str,
    model: str,
    dossier: str,
    api_format: str = "anthropic",
    debug_response: bool = False,
) -> dict[str, Any] | None:
    if api_format == "openai":  # Gemini, DeepSeek, Kilo, OpenRouter... (chat/completions)
        payload_dict: dict[str, Any] = {
            "model": model,
            "max_tokens": 2000,  # folga para modelos que "pensam" antes de responder
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": dossier},
            ],
        }
        headers = {"content-type": "application/json", "authorization": f"Bearer {api_key}"}
    else:
        payload_dict = {
            "model": model,
            "max_tokens": 600,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": dossier}],
        }
        headers = {
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        }
    request = urllib.request.Request(api_url, data=json.dumps(payload_dict).encode(), headers=headers)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                body = json.loads(response.read().decode())
            break
        except urllib.error.HTTPError as error:
            if error.code in (429, 500, 502, 503, 529) and attempt < 4:
                # 429 em plano grátis costuma ser limite por minuto: espera mais
                time.sleep(15 * (attempt + 1) if error.code == 429 else 2**attempt)
                continue
            raise
        except urllib.error.URLError:
            if attempt < 4:
                time.sleep(2**attempt)
                continue
            raise
    if api_format == "openai":
        choices = body.get("choices") or [{}]
        text = (choices[0].get("message") or {}).get("content") or ""
    else:
        text = "".join(
            block.get("text", "") for block in body.get("content", []) if block.get("type") == "text"
        )
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        if debug_response:
            print(f"resposta bruta sem JSON: {text[:2000]!r}", file=sys.stderr)
        return None
    try:
        suggestion = normalize(json.loads(text[start : end + 1]))
    except json.JSONDecodeError:
        if debug_response:
            print(f"resposta bruta com JSON inválido: {text[:2000]!r}", file=sys.stderr)
        return None
    if suggestion is None and debug_response:
        print(f"resposta bruta fora do esquema: {text[:2000]!r}", file=sys.stderr)
    return suggestion


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--template", type=Path, default=GOLD_DIR / "labels_template.csv")
    parser.add_argument("--dossier-dir", type=Path, default=GOLD_DIR / "dossiers")
    parser.add_argument("--output", type=Path, default=GOLD_DIR / "llm_suggestions.json")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--api-url", default=DEFAULT_API_URL)
    parser.add_argument(
        "--format",
        dest="api_format",
        choices=["anthropic", "openai"],
        default="anthropic",
        help="formato da API: 'openai' = chat/completions (Gemini, DeepSeek, Kilo...)",
    )
    parser.add_argument(
        "--api-key-env",
        default="ANTHROPIC_API_KEY",
        help="nome da variável de ambiente com a chave (ex.: GEMINI_API_KEY)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.0,
        help="segundos de pausa entre chamadas (planos grátis com ~5 req/min: use 13)",
    )
    parser.add_argument("--limit", type=int, help="processa só N repositórios pendentes (teste)")
    parser.add_argument(
        "--debug-response",
        action="store_true",
        help="mostra uma prévia da resposta bruta quando ela não passa na validação",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    api_key = os.environ.get(args.api_key_env)
    if not api_key:
        print(f"erro: defina {args.api_key_env}", file=sys.stderr)
        return 2

    try:
        rows = read_template(args.template)
    except OSError as error:
        print(f"erro: {error}", file=sys.stderr)
        return 2

    results: dict[str, Any] = {}
    if args.output.exists():
        results = json.loads(args.output.read_text(encoding="utf-8"))

    pending = [r for r in rows if r["full_name"] not in results]
    if args.limit:
        pending = pending[: args.limit]
    print(f"{len(results)} já feitos; {len(pending)} a processar com {args.model}")

    failed = 0
    for number, row in enumerate(pending, start=1):
        name = row["full_name"]
        dossier_path = args.dossier_dir / dossier_filename(name)
        if not dossier_path.exists():
            print(f"[{number}/{len(pending)}] {name}: sem dossiê, pulando")
            failed += 1
            continue
        try:
            suggestion = call_llm(
                args.api_url,
                api_key,
                args.model,
                dossier_path.read_text(encoding="utf-8"),
                args.api_format,
                args.debug_response,
            )
        except (urllib.error.URLError, OSError) as error:
            print(f"[{number}/{len(pending)}] {name}: erro de API ({error})")
            failed += 1
            continue
        if suggestion is None:
            print(f"[{number}/{len(pending)}] {name}: resposta inválida, pulando")
            failed += 1
            continue
        results[name] = suggestion
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[{number}/{len(pending)}] {name}: ok")
        if args.delay and number < len(pending):
            time.sleep(args.delay)

    print(f"Concluído: {len(results)}/{len(rows)} com sugestão, {failed} falhas (rode de novo para retentar).")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
