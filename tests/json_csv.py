import pytest
import json
import csv
from pathlib import Path
from src.lab05.json_csv import json_to_csv, csv_to_json


# json_csv


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

    with pytest.raises((ValueError, json.JSONDecodeError)):
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
        ([{"name": "Alice"}, {"name": "Bob"}], 2),  # одинаковые ключи
        ([{"id": 1}, {"id": 2}, {"id": 3}], 3),
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


# csv_json


@pytest.mark.parametrize(
    "filename, content, expected_count",
    [
        ("empty.csv", "", 0),  # создает пустой массив
        ("whitespace.csv", "   ", 0),
        ("only_newlines.csv", "\n\n\n", 0),
        ("only_header.csv", "name,age", 0),
    ],
)
def test_csv_to_json_empty_csv(tmp_path, filename, content, expected_count):
    src = tmp_path / filename
    dst = tmp_path / "output.json"

    src.write_text(content, encoding="utf-8")

    csv_to_json(str(src), str(dst))

    with dst.open(encoding="utf-8") as f:
        result = json.load(f)

    assert len(result) == expected_count


@pytest.mark.parametrize(
    "filename, content, expected_count",
    [
        ("normal.csv", "name,age\nAlice,22\nBob,25", 2),
        (
            "inconsistent.csv",
            "name,age\nAlice,22\nBob",
            2,
        ),  # обрабатывает неконсистентные данные
        ("quotes.csv", 'name,desc\n"John, Doe",test', 1),
    ],
)
def test_csv_to_json_various_formats(tmp_path, filename, content, expected_count):
    src = tmp_path / filename
    dst = tmp_path / "output.json"

    src.write_text(content, encoding="utf-8")

    csv_to_json(str(src), str(dst))

    with dst.open(encoding="utf-8") as f:
        result = json.load(f)

    assert len(result) == expected_count


@pytest.mark.parametrize(
    "filename",
    [
        "nonexistent.csv",
        "missing.csv",
        "not_found.csv",
    ],
)
def test_csv_to_json_file_not_found(tmp_path, filename):
    dst = tmp_path / "output.json"

    with pytest.raises(FileNotFoundError):
        csv_to_json(str(tmp_path / filename), str(dst))


# same


@pytest.mark.parametrize(
    "func, input_ext",
    [
        (json_to_csv, "json"),
        (csv_to_json, "csv"),
    ],
)
def test_both_functions_none_paths(func, input_ext):
    with pytest.raises(AttributeError):  # AttributeError
        func(None, "output")


@pytest.mark.parametrize(
    "func, input_ext",
    [
        (json_to_csv, "json"),
        (csv_to_json, "csv"),
    ],
)
def test_both_functions_empty_paths(func, input_ext, tmp_path):
    src = tmp_path / f"test.{input_ext}"

    if input_ext == "json":
        src.write_text('[{"test": "data"}]', encoding="utf-8")
    else:
        src.write_text("test\ndata", encoding="utf-8")

    with pytest.raises(ValueError):
        func("", str(tmp_path / "output"))


@pytest.mark.parametrize(
    "func, input_ext, output_ext",
    [
        (json_to_csv, "json", "csv"),
        (csv_to_json, "csv", "json"),
    ],
)
def test_both_functions_simple_paths(tmp_path, func, input_ext, output_ext):
    src = tmp_path / f"test.{input_ext}"
    dst = tmp_path / f"output.{output_ext}"

    if input_ext == "json":
        src.write_text('[{"name": "Test"}]', encoding="utf-8")
    else:
        src.write_text("name\nTest", encoding="utf-8")

    # простые пути в текущей

    func(str(src.name), str(dst.name))

    assert dst.exists()


@pytest.mark.parametrize(
    "func, input_ext, test_data",
    [
        (json_to_csv, "json", '[{"name": "Алиса", "city": "Москва"}]'),
        (csv_to_json, "csv", "name,city\nАлиса,Москва"),
    ],
)
def test_both_functions_utf8_support(tmp_path, func, input_ext, test_data):
    src = tmp_path / f"test.{input_ext}"
    dst = tmp_path / f"output.{'csv' if input_ext == 'json' else 'json'}"

    src.write_text(test_data, encoding="utf-8")

    func(str(src), str(dst))

    assert dst.exists()
