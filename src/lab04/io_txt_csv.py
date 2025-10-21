from pathlib import Path
import csv
from typing import Iterable, Sequence
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from text import normalize, tokenize
def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    path = Path(path)
    try:
         open(path, encoding=encoding)
    except UnicodeDecodeError:
        print("UnicodeDecodeError")
    except FileNotFoundError:
        print("FileNotFoundError")
    return path.read_text(encoding=encoding)


def write_csv(rows: Iterable[Sequence], path: str | Path,
              header: tuple[str, ...] | None = None) -> None:
    p = Path(path)
    rows = list(rows)
    if len(rows) == 0:
        header=("a","b")
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if rows:
            first_len = len(rows[0])
            for i, row in enumerate(rows):
                if len(row) != first_len:
                    raise ValueError
        if header is not None:
            w.writerow(header)
        for r in rows:
            w.writerow(r)

from collections import Counter

def frequencies_from_text(text: str) -> dict[str, int]:
    from lib.text import normalize, tokenize  # из ЛР3
    tokens = tokenize(normalize(text))
    return Counter(tokens)  # dict-like

def sorted_word_counts(freq: dict[str, int]) -> list[tuple[str, int]]:
    return sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))



