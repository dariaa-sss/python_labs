# Лабораторная работа 5 
## Цель работы
Разобраться с форматом JSON, сериализацией/десериализацией и табличными конвертациями.

## Задание A

``` 
from pathlib import Path
import json, csv

def json_to_csv(json_path: str, csv_path: str) -> None:
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError("FileNotFoundError")
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list) or not all(isinstance(i, dict) for i in data):
        raise ValueError("ValueError")
    output = Path(csv_path)
    with output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys()) #возвращает порядок ключей из первого словаря.
        writer.writeheader()
        writer.writerows(data)


json_to_csv("/Users/dariella/Desktop/python_labs/data/lab05/samples/test.json","/Users/dariella/Desktop/python_labs/data/lab05/out/people_from_json.csv")

def csv_to_json(csv_path: str, json_path: str) -> None:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError("FileNotFoundError")
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    output = Path(json_path)

    with output.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

csv_to_json('/Users/dariella/Desktop/python_labs/data/lab05/samples/test.csv', "/Users/dariella/Desktop/python_labs/data/lab05/out/test_from_csv.json")


```
![img01!](./images/lab05/img01.png)
![img01!](./images/lab05/img02.png)
## Задание B

```
from openpyxl import Workbook
import csv
from pathlib import Path

def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    if not csv_path.lower().endswith(".csv"):
        raise ValueError("ValueError")
    if not xlsx_path.lower().endswith(".xlsx"):
        raise ValueError("ValueError")
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError("FileNotFoundError")
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    rows_added = 0
    try:
        with path.open(encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                ws.append(row)
                rows_added += 1
    except UnicodeDecodeError:
        raise ValueError("ValueError")

    if rows_added == 0:
        raise ValueError("ValueError")


    output = Path(xlsx_path)


    wb.save(output)


csv_to_xlsx("/Users/dariella/Desktop/python_labs/data/lab05/samples/cities.csv","/Users/dariella/Desktop/python_labs/data/lab05/out/test_from_csv.xlsx")

```
![img01!](.python_labs/images/lab05/img03.png)



