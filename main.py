from __future__ import annotations
import argparse
import csv
from pathlib import Path
from typing import NoReturn, Sequence
from tabulate import tabulate

from brand_rate import reports as _reports
from brand_rate.reader import CSVProductReader
from brand_rate.reporting import UnknownReportError, registry


def translate_error_message(message: str) -> str:
    replacements = {
        "argument": "аргумент",
        "invalid choice": "недопустимое значение",
        "choose from": "возможные варианты",
        "expected one argument": "требуется значение",
        "expected at least one argument": "нужно указать хотя бы одно значение",
        "the following arguments are required:": "не указаны обязательные аргументы:",
        "unrecognized arguments:": "неизвестные аргументы:",
    }
    translated = message
    for src, dst in replacements.items():
        translated = translated.replace(src, dst)
    return translated


class LocalizedArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        translated = translate_error_message(message)
        fail(self, translated)


def build_parser() -> argparse.ArgumentParser:
    parser = LocalizedArgumentParser(
        add_help=False,
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Показать эту справку и выйти.",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        metavar="ПУТЬ",
        help="Один или несколько CSV-файлов с колонками name,brand,price,rating.",
    )
    parser.add_argument(
        "--path",
        metavar="ПАПКА",
        help="Папка, из которой нужно взять все CSV-файлы.",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=registry.available_reports(),
        help="Название отчёта (например, average-rating).",
    )
    parser.add_argument(
        "--save",
        metavar="ФАЙЛ",
        help="Путь для сохранения отчёта в формате CSV.",
    )
    return parser


def render_table(rows: Sequence[dict[str, object]]) -> str:
    if not rows:
        return "Нет данных для отображения."

    showindex = range(1, len(rows) + 1)
    return tabulate(rows, headers="keys", tablefmt="grid", showindex=showindex)


def resolve_input_files(
    file_list: Sequence[str] | None, directory: str | None
) -> list[str]:
    files: list[str] = []

    if directory:
        dir_path = Path(directory)
        if not dir_path.is_dir():
            raise ValueError(f"Каталог не найден: {dir_path}")

        dir_files = sorted(p for p in dir_path.glob("*.csv") if p.is_file())
        if not dir_files:
            raise ValueError(f"В каталоге {dir_path} нет CSV-файлов.")

        files.extend(str(path) for path in dir_files)

    if file_list:
        files.extend(file_list)

    if not files:
        raise ValueError("Укажите --files или --path хотя бы с одним CSV-файлом.")

    unique: list[str] = []
    seen: set[str] = set()
    for path in files:
        if path not in seen:
            unique.append(path)
            seen.add(path)

    return unique


def save_report_csv(path: Path, rows: Sequence[dict[str, object]]) -> None:
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row.keys():
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)

    if not fieldnames:
        fieldnames = ["brand", "rating"]

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def fail(parser: argparse.ArgumentParser, message: str) -> NoReturn:
    parser.print_help()
    parser.exit(2, f"\nОшибка: {message}\n")


def run(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    reader = CSVProductReader()

    try:
        files = resolve_input_files(args.files, args.path)
        records = reader.read_many(files)
    except FileNotFoundError as exc:
        missing = exc.filename or str(exc)
        fail(parser, f"Файл не найден: {missing}")
    except ValueError as exc:
        fail(parser, str(exc))

    try:
        report = registry.create(args.report)
    except UnknownReportError as exc:
        fail(parser, str(exc))

    table_rows = report.generate(records)
    table_output = render_table(table_rows)
    print(table_output)

    if args.save:
        save_report_csv(Path(args.save), table_rows)

    return 0

if __name__ == "__main__":
    raise SystemExit(run())
