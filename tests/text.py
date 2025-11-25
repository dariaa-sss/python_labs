import pytest
from src.lib.text import normalize, tokenize, count_freq, top_n


@pytest.mark.parametrize(
    "source, expected",
    [
        ("ПрИвЕт\\nМИр\\t", "привет мир"),
        ("ёжик, Ёлка", "ежик, елка"),
        ("Hello\\r\\nWorld", "hello world"),
        ("  двойные   пробелы  ", "двойные пробелы"),
    ],
)
def test_normalize_basic(source, expected):
    assert normalize(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    [
        ("привет мир", ["привет", "мир"]),
        ("по-настоящему круто", ["по-настоящему", "круто"]),
        ("hello world", ["hello", "world"]),
        ("2025 год", ["2025", "год"]),
        ("emoji 😀 не слово", ["emoji", "не", "слово"]),
    ],
)
def test_tokenize_basic(source, expected):
    assert tokenize(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    [
        (["a", "b", "a", "c", "b", "a"], [("a", 3), ("b", 2), ("c", 1)]),
        (["bb", "aa", "bb", "aa", "cc"], [("aa", 2), ("bb", 2), ("cc", 1)]),
    ],
)
def test_count_freq_and_top_n(source, expected):
    assert top_n(count_freq(source)) == expected


@pytest.mark.parametrize(
    "source, count, expected",
    [
        ({"a": 3, "b": 2, "c": 1}, 2, [("a", 3), ("b", 2)]),
        ({"aa": 2, "bb": 2, "cc": 1}, 1, [("aa", 2)]),
    ],
)
def test_top_n_tie_breaker(source, count, expected):
    assert top_n(source, count) == expected
