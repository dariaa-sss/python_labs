import pytest
import json
import csv
from pathlib import Path
from src.lab05.json_csv import json_to_csv, csv_to_json


#  json_to_csv


@pytest.mark.parametrize(
    "filename, content",
    [
        ("empty.json", ""),
        ("whitespace.json", "   "),
        ("null.json", "null"),
    ],
)
def test_json_to_csv_invalid_json_types(tmp_path, filename, content):
    src = tmp_path / filename
    dst = tmp_path / "output.csv"
    src.write_text(content, encoding="utf-8")
    with pytest.raises(ValueError):
        json_to_csv(str(src), str(dst))


@pytest.mark.parametrize(
    "filename",
    [
        "nonexistent.json",
        "missing.json",
        "not_here.json",
        "subdir/nested_missing.json",  # относительный путь с поддиректорией
    ],
)
def test_json_to_csv_file_not_found(tmp_path, filename):
    dst = tmp_path / "output.csv"

    with pytest.raises(FileNotFoundError):
        json_to_csv(str(tmp_path / filename), str(dst))


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
    """Битый JSON - должен вызывать json.JSONDecodeError"""
    src = tmp_path / filename
    dst = tmp_path / "output.csv"

    src.write_text(content, encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        json_to_csv(str(src), str(dst))


# csv_to_json


@pytest.mark.parametrize(
    "filename, content",
    [
        ("empty.csv", ""),  # полностью пустой файл
        ("whitespace.csv", "   "),  # только пробелы
        ("only_newlines.csv", "\n\n\n"),  # только переносы строк
    ],
)
def test_csv_to_json_empty_or_invalid_csv(tmp_path, filename, content):
    src = tmp_path / filename
    dst = tmp_path / "output.json"

    src.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError):
        csv_to_json(str(src), str(dst))


@pytest.mark.parametrize(
    "filename",
    [
        "nonexistent.csv",
        "missing.csv",
        "not_found.csv",
        "data/subdir/missing.csv",  # относительный путь с поддиректорией
    ],
)
def test_csv_to_json_file_not_found(tmp_path, filename):
    dst = tmp_path / "output.json"

    with pytest.raises(FileNotFoundError):
        csv_to_json(str(tmp_path / filename), str(dst))


@pytest.mark.parametrize(
    "filename, content",
    [
        ("unclosed_quotes.csv", '"name","age"\n"Alice,22'),
        ("malformed_quotes.csv", 'name,age\n"Alice","22"\n"Bob,25'),
        ("inconsistent_columns.csv", "name,age\nAlice,22\nBob"),
        ("only_header.csv", "name,age"),
    ],
)
def test_csv_to_json_malformed_csv(tmp_path, filename, content):
    src = tmp_path / filename
    dst = tmp_path / "output.json"

    src.write_text(content, encoding="utf-8")

    with pytest.raises(csv.Error):
        csv_to_json(str(src), str(dst))


# общие


@pytest.mark.parametrize(
    "func, input_ext",
    [
        (json_to_csv, "json"),
        (csv_to_json, "csv"),
    ],
)
def test_both_functions_none_paths(func, input_ext):
    with pytest.raises(TypeError):
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

    with pytest.raises(ValueError):
        func(str(src), "")


@pytest.mark.parametrize(
    "func, input_ext, output_ext",
    [
        (json_to_csv, "json", "csv"),
        (csv_to_json, "csv", "json"),
    ],
)
def test_both_functions_relative_paths(tmp_path, func, input_ext, output_ext):
    """Проверка работы с относительными путями"""
    # Создаем поддиректорию
    subdir = tmp_path / "data"
    subdir.mkdir()

    src = subdir / f"test.{input_ext}"
    dst = subdir / f"output.{output_ext}"

    # Создаем валидные данные
    if input_ext == "json":
        src.write_text('[{"name": "Test"}]', encoding="utf-8")
    else:
        src.write_text("name\nTest", encoding="utf-8")

    # Используем относительные пути
    relative_src = Path("data") / f"test.{input_ext}"
    relative_dst = Path("data") / f"output.{output_ext}"

    # Должны работать с относительными путями
    func(str(relative_src), str(relative_dst))

    # Проверяем что файл создался
    assert dst.exists()


@pytest.mark.parametrize(
    "func, input_ext",
    [
        (json_to_csv, "json"),
        (csv_to_json, "csv"),
    ],
)
def test_both_functions_utf8_encoding(tmp_path, func, input_ext):
    """Проверка строгой кодировки UTF-8"""
    src = tmp_path / f"utf8_test.{input_ext}"
    dst = tmp_path / f"output.{'csv' if input_ext == 'json' else 'json'}"

    # Данные с UTF-8 символами
    if input_ext == "json":
        content = '[{"name": "Алиса 😀", "city": "Москва"}]'
    else:
        content = "name,city\nАлиса 😀,Москва"

    src.write_text(content, encoding="utf-8")

    # Должен работать без ошибок кодировки
    func(str(src), str(dst))

    # Проверяем что выходной файл создан
    assert dst.exists()

    # Проверяем что данные сохранились корректно
    output_content = dst.read_text(encoding="utf-8")
    assert "Алиса" in output_content
