import json
from pathlib import Path
from typing import List
from src.lab08.models import Student

def students_to_json(students: List[Student], path: str) -> None:
    path_obj = Path(path)
    if not path_obj.lower().endswith(".json"):
        raise ValueError("ValueError")
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    data = [student.to_dict() for student in students]
    with open(path_obj, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def students_from_json(path: str) -> List[Student]:
    path_obj = Path(path)
    if not path_obj.lower().endswith(".json"):
        raise ValueError("ValueError")
    if not path_obj.exists():
        raise FileNotFoundError(f"Файл не найден")
    with open(path_obj, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("ValueError")
    
    students = []
    for i, item in enumerate(data):
        try:
            student = Student.from_dict(item)
            students.append(student)
        except (ValueError, KeyError) as e:
            print(f"{e}")
            raise
    return students

if __name__ == "__main__":
    input_path = '/Users/dariella/Desktop/python_labs/data/lab08/students_input.json'
    output_path = '/Users/dariella/Desktop/python_labs/data/lab08/students_output.json' 
    try:
        students = students_from_json(input_path)
        students_to_json(students, output_path)
    except Exception as e:
        print(f"{e}")
