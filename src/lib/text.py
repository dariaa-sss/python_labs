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
