import argparse
from pathlib import Path

from src.lab05.json_csv import json_to_csv, csv_to_json
from src.lab05.csv_xlsx import csv_to_xlsx


def validate_input_file(path: str, parser, expected_ext: str):
    p = Path(path)
    if not p.exists():
        parser.error(f"Файл не найден: {path}")

    if not p.suffix.lower() == expected_ext:
        parser.error(f"Ожидался файл формата {expected_ext}, получено: {p.suffix}")

    return p


def main():
    parser = argparse.ArgumentParser(description="Конвертеры данных")
    sub = parser.add_subparsers(dest="cmd")

    # json → csv
    p1 = sub.add_parser("json2csv", help="Конвертация JSON → CSV")
    p1.add_argument("--in", dest="input", required=True)
    p1.add_argument("--out", dest="output", required=True)

    # csv → json
    p2 = sub.add_parser("csv2json", help="Конвертация CSV → JSON")
    p2.add_argument("--in", dest="input", required=True)
    p2.add_argument("--out", dest="output", required=True)

    # csv → xlsx
    p3 = sub.add_parser("csv2xlsx", help="Конвертация CSV → XLSX")
    p3.add_argument("--in", dest="input", required=True)
    p3.add_argument("--out", dest="output", required=True)

    args = parser.parse_args()

    if args.cmd is None:
        parser.error("Не указана команда. Используйте: json2csv, csv2json, csv2xlsx")

    if args.cmd == "json2csv":
        validate_input_file(args.input, parser, ".json")
        json_to_csv(args.input, args.output)
        print(f"Готово: {args.output}")

    elif args.cmd == "csv2json":
        validate_input_file(args.input, parser, ".csv")
        csv_to_json(args.input, args.output)
        print(f"Готово: {args.output}")

    elif args.cmd == "csv2xlsx":
        validate_input_file(args.input, parser, ".csv")
        csv_to_xlsx(args.input, args.output)
        print(f"Готово: {args.output}")

    else:
        parser.error(f"Неизвестная команда: {args.cmd}")


if __name__ == "__main__":
    main()
