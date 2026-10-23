#!/usr/bin/env python3
"""Compila o artigo LaTeX (latex/main.tex) e gera RELATORIO.pdf na raiz do Enunciado 3.

Uso:
    uv run python scripts/build_report.py            # instala TinyTeX se faltar e compila
    uv run python scripts/build_report.py --clean    # apaga latex/build antes

Usa o TinyTeX via ``pytinytex`` (instalado em ``~/.pytinytex``). O
``pytinytex.download_tinytex`` 0.5.x não reconhece os arquivos ``.tar.xz`` das
releases recentes do TinyTeX, então o download é feito aqui, com versão fixa.
O ``tlmgr`` do TinyTeX exige módulos Perl (``File::Find``) que nem toda
distribuição traz, então os pacotes extras são baixados direto do repositório
do TeX Live no CTAN e extraídos numa árvore ``TEXMFHOME`` própria.
O template SBC fica em ``templates/sbc/`` e entra no caminho de busca do TeX
por ``TEXINPUTS``/``BSTINPUTS``; as figuras vêm de ``analysis/output/figures/``.
"""

from __future__ import annotations

import argparse
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

import pytinytex

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LATEX_DIR = PROJECT_ROOT / "latex"
TEMPLATE_DIR = PROJECT_ROOT / "templates" / "sbc"
BUILD_DIR = LATEX_DIR / "build"
OUTPUT_PDF = PROJECT_ROOT / "RELATORIO.pdf"
MAIN = "main"

TINYTEX_VERSION = "2026.09"
TINYTEX_TARGET = Path(pytinytex.DEFAULT_TARGET_FOLDER)

TEXMF_EXTRA = TINYTEX_TARGET / "texmf-extra"
CTAN_ARCHIVE = "https://mirror.ctan.org/systems/texlive/tlnet/archive"

# Pacotes que não vêm na variação 1 do TinyTeX (nome do pacote → arquivo que o prova).
EXTRA_PACKAGES = {
    "babel-portuges": "tex/generic/babel-portuges/portuges.ldf",
    "titlesec": "tex/latex/titlesec/titlesec.sty",
    "caption": "tex/latex/caption/caption.sty",
    "multirow": "tex/latex/multirow/multirow.sty",
    "enumitem": "tex/latex/enumitem/enumitem.sty",
    "microtype": "tex/latex/microtype/microtype.sty",
    "hyphen-portuguese": "tex/generic/hyph-utf8/loadhyph/loadhyph-pt.tex",
}

# Formato pdflatex reconstruído com hifenização em português (o da TinyTeX só tem inglês).
FORMAT_DIR = TEXMF_EXTRA / "web2c" / "pdftex"
FORMAT_STAMP = FORMAT_DIR / "pdflatex.portuguese"
PORTUGUESE_LANGUAGE_DAT = "portuguese loadhyph-pt.tex\n=portuges\n=brazil\n=brazilian\n"


def _asset_name() -> str:
    system, machine = platform.system(), platform.machine().lower()
    if system == "Linux":
        arch = "arm64" if machine in ("aarch64", "arm64") else "x86_64"
        return f"TinyTeX-1-linux-{arch}-v{TINYTEX_VERSION}.tar.xz"
    if system == "Darwin":
        return f"TinyTeX-1-darwin-v{TINYTEX_VERSION}.tar.xz"
    raise SystemExit(
        "Instalação automática do TinyTeX só em Linux/macOS. No Windows, rode "
        "`uv run python -c \"import pytinytex; pytinytex.download_tinytex()\"`."
    )


def install_tinytex() -> None:
    """Baixa e extrai o TinyTeX em ~/.pytinytex, se ainda não estiver lá."""
    try:
        pytinytex.ensure_tinytex_installed(TINYTEX_TARGET)
        return
    except RuntimeError:
        pass
    name = _asset_name()
    url = f"https://github.com/rstudio/tinytex-releases/releases/download/v{TINYTEX_VERSION}/{name}"
    print(f"Baixando TinyTeX {TINYTEX_VERSION} ({name})...")
    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp) / name
        urllib.request.urlretrieve(url, archive)
        with tarfile.open(archive, "r:xz") as tar:
            tar.extractall(tmp, filter="data")
        extracted = next(p for p in Path(tmp).iterdir() if p.is_dir() and "TinyTeX" in p.name)
        TINYTEX_TARGET.mkdir(parents=True, exist_ok=True)
        shutil.copytree(extracted, TINYTEX_TARGET, dirs_exist_ok=True, symlinks=True)
    pytinytex.clear_path_cache()
    pytinytex.ensure_tinytex_installed(TINYTEX_TARGET)


def bin_dir() -> Path:
    return Path(pytinytex.get_tinytex_path(TINYTEX_TARGET))


def install_packages() -> None:
    """Baixa do CTAN os pacotes que faltam e extrai em TEXMF_EXTRA (sem tlmgr)."""
    TEXMF_EXTRA.mkdir(parents=True, exist_ok=True)
    for package, marker in EXTRA_PACKAGES.items():
        if (TEXMF_EXTRA / marker).exists():
            continue
        print(f"Instalando pacote TeX: {package}")
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / f"{package}.tar.xz"
            urllib.request.urlretrieve(f"{CTAN_ARCHIVE}/{package}.tar.xz", archive)
            with tarfile.open(archive, "r:xz") as tar:
                members = [m for m in tar.getmembers() if m.name.startswith("tex/")]
                tar.extractall(TEXMF_EXTRA, members=members, filter="data")
        if not (TEXMF_EXTRA / marker).exists():
            raise SystemExit(f"Pacote {package} baixado, mas {marker} não foi encontrado.")


def build_format() -> None:
    """Gera pdflatex.fmt com português, chamando ``pdftex -ini`` (o fmtutil exige Perl).

    O ``language.dat`` modificado fica na pasta de trabalho, que tem prioridade na
    busca do TeX sobre o ``language.dat`` da distribuição.
    """
    if FORMAT_STAMP.exists():
        return
    print("Gerando formato pdflatex com hifenização em português...")
    FORMAT_DIR.mkdir(parents=True, exist_ok=True)
    kpsewhich = str(bin_dir() / "kpsewhich")
    original = subprocess.run([kpsewhich, "language.dat"], capture_output=True, text=True, check=True)
    language_dat = FORMAT_DIR / "language.dat"
    language_dat.write_text(
        Path(original.stdout.strip()).read_text(encoding="utf-8") + PORTUGUESE_LANGUAGE_DAT,
        encoding="utf-8",
    )
    env = dict(os.environ, TEXMFHOME=str(TEXMF_EXTRA))
    cmd = [
        str(bin_dir() / "pdftex"), "-ini", "-interaction=nonstopmode", "-jobname=pdflatex",
        "-progname=pdflatex", "-translate-file=cp227.tcx", "*pdflatex.ini",
    ]
    result = subprocess.run(cmd, cwd=FORMAT_DIR, env=env, capture_output=True, text=True, errors="replace")
    language_dat.unlink()
    log = (FORMAT_DIR / "pdflatex.log").read_text(errors="replace")
    if result.returncode != 0 or "l@portuguese" not in log:
        print(result.stdout[-3000:])
        raise SystemExit("Falha ao gerar o formato pdflatex com português.")
    FORMAT_STAMP.write_text("ok\n", encoding="utf-8")


def _env() -> dict[str, str]:
    env = dict(os.environ)
    sep = os.pathsep
    # O separador vazio no fim mantém os caminhos padrão da distribuição.
    env["TEXMFHOME"] = str(TEXMF_EXTRA)
    env["TEXFORMATS"] = f"{FORMAT_DIR}{sep}"
    env["TEXINPUTS"] = f"{LATEX_DIR}{sep}{TEMPLATE_DIR}{sep}"
    env["BSTINPUTS"] = f"{TEMPLATE_DIR}{sep}"
    env["BIBINPUTS"] = f"{LATEX_DIR}{sep}"
    env["PATH"] = f"{bin_dir()}{sep}{env.get('PATH', '')}"
    return env


def _run(cmd: list[str], env: dict[str, str], cwd: Path = LATEX_DIR) -> None:
    result = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, errors="replace")
    if result.returncode != 0:
        log = BUILD_DIR / f"{MAIN}.log"
        tail = log.read_text(errors="replace").splitlines()[-40:] if log.exists() else []
        print(result.stdout[-4000:], result.stderr[-2000:], *tail, sep="\n")
        raise SystemExit(f"Falhou: {' '.join(cmd)}")


def compile_report() -> Path:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    env = _env()
    pdflatex = [
        str(bin_dir() / "pdflatex"),
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-output-directory={BUILD_DIR}",
        f"{MAIN}.tex",
    ]
    _run(pdflatex, env)
    # bibtex não aceita caminhos com espaço ("Enunciado 3"): roda dentro de build/.
    _run([str(bin_dir() / "bibtex"), MAIN], env, cwd=BUILD_DIR)
    _run(pdflatex, env)
    _run(pdflatex, env)
    pdf = BUILD_DIR / f"{MAIN}.pdf"
    shutil.copy2(pdf, OUTPUT_PDF)
    return OUTPUT_PDF


def page_count() -> int | None:
    """Número de páginas, lido da linha "Output written on ... (N pages" do log."""
    log = (BUILD_DIR / f"{MAIN}.log").read_text(errors="replace")
    match = re.search(r"Output written on .*?\((\d+) pages?", log, re.DOTALL)
    return int(match.group(1)) if match else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clean", action="store_true", help="apaga latex/build antes")
    args = parser.parse_args(argv)
    if args.clean and BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    install_tinytex()
    install_packages()
    build_format()
    pdf = compile_report()
    pages = page_count()
    print(f"PDF gerado: {pdf.relative_to(PROJECT_ROOT)}" + (f" ({pages} páginas)" if pages else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
