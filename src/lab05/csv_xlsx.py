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


csv_to_xlsx(
    "/Users/dariella/Desktop/python_labs/data/lab05/samples/cities.csv",
    "/Users/dariella/Desktop/python_labs/data/lab05/out/test_from_csv.xlsx",
)
