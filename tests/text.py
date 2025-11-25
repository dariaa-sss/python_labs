
import re

pattern = r"\w+(?:-\w+)*"


def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if casefold:
        text = text.lower()
    if yo2e:
        text = text.replace("ё", "е")
    text = re.sub(r"\\[nrt]", " ", text)
    result = re.sub(r"\s+", " ", text).strip()
    return result


def tokenize(text: str) -> list[str]:
    text = normalize(text)
    return re.findall(pattern, text)


def count_freq(tokens: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    return counts


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    return sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:n]

import pytest
import json
import csv
from pathlib import Path
from src.lab05.json_csv import json_to_csv, csv_to_json


# 


@pytest.mark.parametrize(
    "filename, content",
    [
        ("empty.json", ""),
        ("null.json", "null"),
        ("string.json", '"text"'),
        ("number.json", "42"),
    ],
)
def test_json_to_csv_invalid_types(tmp_path, filename, content):
    src = tmp_path / filename
    dst = tmp_path / "output.csv"

    src.write_text(content, encoding="utf-8")

    with pytest.raises((ValueError, json.JSONDecodeError, TypeError)):
        json_to_csv(str(src), str(dst))


@pytest.mark.parametrize(
    "filename, content",
    [
        ("malformed.json", '{"name": "Alice",}'),
        ("unclosed.json", '{"name": "Alice"'),
        ("unquoted.json", '{name: "Alice"}'),
        ("broken.json", '[{"name": "Alice]'),
    ],
)
def test_json_to_csv_malformed_json(tmp_path, filename, content):
    src = tmp_path / filename
    dst = tmp_path / "output.csv"

    src.write_text(content, encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        json_to_csv(str(src), str(dst))


@pytest.mark.parametrize(
    "filename",
    [
        "nonexistent.json",
        "missing.json",
        "not_found.json",
        "wrong_path/data.json",
    ],
)
def test_json_to_csv_file_not_found(tmp_path, filename):
    dst = tmp_path / "output.csv"

    with pytest.raises(FileNotFoundError):
        json_to_csv(str(tmp_path / filename), str(dst))


@pytest.mark.parametrize(
    "json_data, expected_rows",
    [
        ([{"name": "Alice", "age": 25}], 1),
        ([{"a": 1}, {"b": 2}], 2),
        ([{"id": 1}, {"id": 2}, {"id": 3}], 3),
        ([], 0),
    ],
)
def test_json_to_csv_valid_data(tmp_path, json_data, expected_rows):
    src = tmp_path / "test.json"
    dst = tmp_path / "test.csv"

    src.write_text(json.dumps(json_data), encoding="utf-8")

    json_to_csv(str(src), str(dst))

    with dst.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == expected_rows


#


@pytest.mark.parametrize(
    "filename, content",
    [
        ("empty.csv", ""),
        ("whitespace.csv", "   "),
        ("only_bom.csv", "\ufeff"),
        ("only_newlines.csv", "\n\n\n"),
    ],
)
def test_csv_to_json_empty_csv(tmp_path, filename, content):
    src = tmp_path / filename
    dst = tmp_path / "output.json"

    src.write_text(content, encoding="utf-8")

    with pytest.raises((ValueError, csv.Error, StopIteration)):
        csv_to_json(str(src), str(dst))


@pytest.mark.parametrize(
    "filename, content",
    [
        ("unclosed_quotes.csv", '"name","age"\n"Alice,22'),
        ("malformed_quotes.csv", 'name,age\n"Alice","22"\n"Bob,25'),
        ("broken_quotes.csv", '"name\nAlice"'),
        ("mixed_quotes.csv", 'name,desc\n"John "The Boss"",test'),
    ],
)
def test_csv_to_json_malformed_csv(tmp_path, filename, content):
    src = tmp_path / filename
    dst = tmp_path / "output.json"

    src.write_text(content, encoding="utf-8")

    with pytest.raises(csv.Error):
        csv_to_json(str(src), str(dst))


@pytest.mark.parametrize(
    "filename",
    [
        "nonexistent.csv",
        "missing.csv",
        "not_found.csv",
        "subdir/data.csv",
    ],
)
def test_csv_to_json_file_not_found(tmp_path, filename):
    dst = tmp_path / "output.json"

    with pytest.raises(FileNotFoundError):
        csv_to_json(str(tmp_path / filename), str(dst))


@pytest.mark.parametrize(
    "csv_data, expected_count",
    [
        ([["name", "age"], ["Alice", "25"]], 1),
        ([["id", "value"], ["1", "a"], ["2", "b"]], 2),
        ([["x"], ["1"], ["2"], ["3"]], 3),
        ([["header"]], 0),
    ],
)
def test_csv_to_json_valid_data(tmp_path, csv_data, expected_count):
    src = tmp_path / "test.csv"
    dst = tmp_path / "test.json"

    with src.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)

    csv_to_json(str(src), str(dst))

    with dst.open(encoding="utf-8") as f:
        result = json.load(f)

    assert len(result) == expected_count

