from pathlib import Path
import json, csv


def json_to_csv(json_path: str, csv_path: str) -> None:
    if not json_path.lower().endswith(".json"):
        raise ValueError("ValueError")
    if not csv_path.lower().endswith(".csv"):
        raise ValueError("ValueError")
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError("FileNotFoundError")
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list) or not all(isinstance(i, dict) for i in data):
        raise ValueError("ValueError")
    output = Path(csv_path)
    with output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=data[0].keys()
        )  # возвращает порядок ключей из первого словаря.
        writer.writeheader()
        writer.writerows(data)


json_to_csv(
    "/Users/dariella/Desktop/python_labs/data/lab05/samples/test.json",
    "/Users/dariella/Desktop/python_labs/data/lab05/out/rr.csv",
)


def csv_to_json(csv_path: str, json_path: str) -> None:
    if not json_path.lower().endswith(".json"):
        raise ValueError("ValueError")
    if not csv_path.lower().endswith(".csv"):
        raise ValueError("ValueError")
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError("FileNotFoundError")
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    output = Path(json_path)

    with output.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


csv_to_json(
    "/Users/dariella/Desktop/python_labs/data/lab05/samples/test.csv",
    "/Users/dariella/Desktop/python_labs/data/lab05/out/test_from_csv.json",
)
