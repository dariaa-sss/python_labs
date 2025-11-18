import argparse
from pathlib import Path
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))

from text import tokenize, count_freq, top_n

def command_cat(path: Path, number_lines: bool):
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if number_lines:
                print(f"{i:4d} | {line}")
            else:
                print(line)


def command_stats(path: Path, top_n_value: int):
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    text = path.read_text(encoding="utf-8")

    tokens = tokenize(text)
    freq = count_freq(tokens)
    top = top_n(freq, top_n_value)

    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(freq)}")
    print(f"Топ-{top_n_value}:")
    for word, count in top:
        print(f"{word}: {count}")


def main():
    parser = argparse.ArgumentParser(description="CLI-утилиты лабораторной №6")
    subparsers = parser.add_subparsers(dest="command")

    # cat
    cat_parser = subparsers.add_parser("cat", help="Вывести содержимое файла")
    cat_parser.add_argument("--input", required=True)
    cat_parser.add_argument("-n", action="store_true", help="Нумеровать строки")

    # stats 
    stats_parser = subparsers.add_parser("stats", help="Частоты слов")
    stats_parser.add_argument("--input", required=True)
    stats_parser.add_argument("--top", type=int, default=5)

    args = parser.parse_args()

    if args.command == "cat":
        command_cat(Path(args.input), args.n)

    elif args.command == "stats":
        command_stats(Path(args.input), args.top)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
