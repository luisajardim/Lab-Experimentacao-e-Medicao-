"""Interface de linha de comando do pipeline (entrada única).

Subcomandos: collect, metrics, report.
Lê config.toml, gerencia variável de ambiente GITHUB_TOKEN e configura logging estruturado.
"""

import argparse
import logging
import os
import sys

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # Para compatibilidade com Python < 3.11, se necessário. O projeto usa 3.12+ (uv.lock)

log = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pipeline",
        description="Pipeline de mineração de métricas DORA (Lab03).",
    )
    parser.add_argument(
        "--config",
        default="config.toml",
        help="Caminho do arquivo de configuração (padrão: config.toml)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limite de repositórios processados (para smoke tests)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Ativa logging detalhado (nível DEBUG)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="Estágio do pipeline")
    
    subparsers.add_parser("collect", help="Coleta dados do GitHub")
    subparsers.add_parser("metrics", help="Calcula métricas DORA")
    subparsers.add_parser("report", help="Gera relatórios da análise")
    subparsers.add_parser("doctor", help="Valida token, config, cache e dependências")

    return parser


def configure_logging(debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    
    # Se nenhum argumento for passado, exibe o help
    if argv is None and len(sys.argv) == 1:
        parser.print_help()
        return 0

    args = parser.parse_args(argv)

    configure_logging(args.debug)

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Erro: A variável de ambiente GITHUB_TOKEN não está definida.")
        print("Por favor, defina o token antes de rodar o pipeline. Ex:")
        print("  export GITHUB_TOKEN='seu_token_aqui'")
        return 1

    try:
        with open(args.config, "rb") as f:
            config = tomllib.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo de configuração '{args.config}' não encontrado.")
        return 1
    except Exception as e:
        print(f"Erro ao ler configuração: {e}")
        return 1

    log.info("Iniciando pipeline, comando: %s", args.command)
    
    if args.command == "doctor":
        log.info("Ambiente validado com sucesso. Token e config presentes.")
        return 0

    if args.limit:
        log.info("Limite ativado: processando no máximo %d repositório(s).", args.limit)

    # TODO: Implementar a chamada aos módulos correspondentes de cada estágio
    print(f"[pipeline] estágio '{args.command}' configurado e pronto (implementação pendente T02-T09).")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
