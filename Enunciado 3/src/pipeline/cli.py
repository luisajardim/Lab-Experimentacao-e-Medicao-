"""Interface de linha de comando do pipeline (entrada única).

Esqueleto do T01; subcomandos são implementados em T08 e estágios
de coleta em T02-T06. Opções:

    python -m pipeline --config config.toml --stage collect --limit 2
    python -m pipeline doctor
"""

import argparse

STAGES = ("collect", "metrics", "report")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pipeline",
        description="Pipeline de mineração de métricas DORA (Lab03).",
    )
    parser.add_argument(
        "--config",
        default="config.toml",
        help="caminho do arquivo de configuração (padrão: config.toml)",
    )
    parser.add_argument(
        "--stage",
        choices=STAGES,
        help="executar apenas um estágio (collect | metrics | report)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="limite de repositórios processados (smoke tests)",
    )
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("doctor", help="valida token, config, cache e dependências")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None and args.stage is None:
        parser.print_help()
        return 0
    token_missing = not _has_token()
    if token_missing and (args.stage == "collect" or args.command is None):
        print("erro: defina a variável de ambiente GITHUB_TOKEN", flush=True)
        return 2
    print(f"[pipeline] estágio '{args.stage or args.command}' não implementado ainda (T02-T09).")
    return 0


def _has_token() -> bool:
    import os

    return bool(os.environ.get("GITHUB_TOKEN"))


if __name__ == "__main__":
    raise SystemExit(main())
