# Лабораторная работа 4
## Цель работы
Нормализовать текст, аккуратно токенизировать, посчитать частоты слов и вывести топ-N слов.

## Задание A

``` 
import re

pattern = r'\w+(?:-\w+)*'
def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if casefold: text = text.lower()
    if yo2e: text = text.replace("ё","е")
    #text = re.findall(pattern, text)
    result = re.sub(r'\s+', ' ', text).strip()

    return result

print(normalize("ПрИвЕт\nМИр\t"))

def tokenize(text: str) -> list[str]:
    text=normalize(text)
    return re.findall(pattern, text)

print(tokenize("emoji 😀 не слово"))

def count_freq(tokens: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    return counts
print(count_freq(["a","b","b","b","a","c","b","a"]))

def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)[:n]
print(top_n(count_freq(["a","b","a","c","b","a"]),n=5))
```
![img01!](./images/lab03/img01.png)
## Задание B

```
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))

from text import normalize, top_n,tokenize, count_freq

inf=input("")
print(f'Всего слов: {len(tokenize(inf))}')
print(f'Уникальных слов: {len(count_freq((tokenize(inf))))}')
print('Топ-5:')
for world,count in top_n(count_freq((tokenize(inf))))[:5]:
     print(f'{world}: {count}')

```
![img01!](./images/lab03/img02.png)
# Лабораторная работа 4 
## Цель работы
закрепить работу с файлами (чтение/запись, кодировки), автоматизировать сбор статистики по словам и выгружать её в CSV.

## Задание A

``` 
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
    raise UnicodeDecodeError
    raise FileNotFoundError

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

```
![img01!](./images/lab04/img01.png)
![img01!](./images/lab04/img03.png)
## Задание B

```
import sys
import os

from src.lib.text import top_n

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from io_txt_csv import read_text, write_csv, frequencies_from_text
from text import normalize, top_n,tokenize, count_freq

txt = read_text("/Users/dariella/Desktop/python_labs/data/lab04/test.txt")
norm=normalize(txt)
token=tokenize(norm)
counts=count_freq(token)
top=top_n(counts)


write_csv( top, "/Users/dariella/Desktop/python_labs/data/lab04/check2.csv",header=("word", "count"))

print(f"Всего слов: {len(token)}")
print(f'Уникальных слов:{len(counts)}')
print('Топ-5:')
for world,count in top[:5]:
     print(f'{world}: {count}')

```
![img01!](./images/lab04/img03.png)

![img01!](./images/lab04/img02.png)
