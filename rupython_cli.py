from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from Interpritator import Interpreter
from Parser import Parser
from Tokenizer import Tokenizer


VERSION = "0.1.0"
PROJECT_ROOT = Path(__file__).resolve().parent


def run_source(source_code: str) -> None:
    tokenizer = Tokenizer(source_code)
    tokens = tokenizer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(ast)


def run_file(filename: str) -> int:
    if filename == "-":
        try:
            run_source(sys.stdin.read())
        except Exception as error:
            print(f"Ошибка RuPython: {error}", file=sys.stderr)
            return 1

        return 0

    file_path = Path(filename).expanduser()

    if not file_path.exists():
        print(f"Ошибка: файл не найден: {file_path}", file=sys.stderr)
        return 1

    if not file_path.is_file():
        print(f"Ошибка: это не файл: {file_path}", file=sys.stderr)
        return 1

    try:
        source_code = file_path.read_text(encoding="utf-8")
        run_source(source_code)
    except Exception as error:
        print(f"Ошибка RuPython: {error}", file=sys.stderr)
        return 1

    return 0


def update_language() -> int:
    if not (PROJECT_ROOT / ".git").exists():
        print(
            "Ошибка: --update работает только для установки из git-репозитория.",
            file=sys.stderr,
        )
        return 1

    if shutil.which("git") is None:
        print("Ошибка: для обновления нужен установленный git.", file=sys.stderr)
        return 1

    print("Обновляю RuPython из GitHub...")

    try:
        result = subprocess.run(
            ["git", "pull", "--ff-only"],
            cwd=PROJECT_ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except OSError as error:
        print(f"Ошибка запуска git: {error}", file=sys.stderr)
        return 1

    if result.stdout:
        print(result.stdout.strip())

    if result.returncode != 0:
        print(
            "Обновление не выполнено. Проверьте подключение к интернету и локальные изменения.",
            file=sys.stderr,
        )
        return result.returncode

    print("RuPython обновлен.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rupython",
        description="Интерпретатор учебного языка RuPython.",
    )
    parser.add_argument(
        "filename",
        nargs="?",
        help="путь к .rupy файлу или - для чтения из stdin",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="обновить RuPython из GitHub",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"RuPython {VERSION}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.update:
        return update_language()

    if not args.filename:
        parser.print_help()
        return 0

    return run_file(args.filename)


if __name__ == "__main__":
    raise SystemExit(main())
