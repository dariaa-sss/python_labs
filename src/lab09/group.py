import csv
from pathlib import Path
from lab08.models import Student
from datetime import datetime


def validate_date(date_str: str):
    """Проверка даты формата YYYY-MM-DD"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Неверный формат даты: {date_str}. Ожидается YYYY-MM-DD")


def validate_gpa(gpa):
    """Проверка корректности GPA"""
    try:
        gpa = float(gpa)
    except ValueError:
        raise ValueError(f"GPA должно быть числом, получено: {gpa}")

    if not (0 <= gpa <= 5):
        raise ValueError(f"GPA должно быть в диапазоне 0–5, получено: {gpa}")

    return gpa

class Group:
    def __init__(self, storage_path: str):
        self.path = Path(storage_path)
        if not self.path.exists():
            with self.path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["fio", "birthdate", "group", "gpa"]) 

    

    def _read_all(self):
        if not self.path.exists():
            raise FileNotFoundError("FileNotFoundError")
        if not self.path.suffix.lower() == ".csv":
            raise ValueError("ValueError: не то расширение файла")
    
        students =[]
        with self.path.open("r", encoding="utf-8", newline="") as f:
            base = csv.DictReader(f) 
            for row in base:
                # Проверка корректности записи
                if not row.get('fio'):
                    raise ValueError("Поле 'fio' отсутствует в CSV")

                validate_date(row['birthdate'])
                row['gpa'] = validate_gpa(row['gpa'])

                students.append(row)
        return students


    def list(self):
        return self._read_all()
    
    def add(self, student: Student):
        if not isinstance(student, Student):
            raise TypeError("add() принимает только объект класса Student")

        validate_date(student.birthdate)
        gpa = validate_gpa(student.gpa)
        students = self._read_all()
        for s in students:
            if s["fio"] == student.fio:
                raise ValueError(f"Студент '{student.fio}' уже существует в списке")

    
        students.append({
            'fio': student.fio,
            'birthdate': student.birthdate,
            'group': student.group,
            'gpa': float(student.gpa)
        })
        with self.path.open("w", encoding="utf-8", newline="") as f:
            fieldnames = ["fio", "birthdate", "group", "gpa"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(students)
        return students

    def find(self, substr: str):
        if not isinstance(substr, str):
            raise TypeError("Поисковая строка должна быть str")

        rows = self.list()
        return [r for r in rows if substr in r["fio"]]  
 

    def remove(self, fio: str):
        if not isinstance(fio, str):
            raise TypeError("fio должно быть строкой")
        rows = self.list()
        for i, r in enumerate(rows):
            if r["fio"] == fio:
                rows.pop(i)
                with self.path.open("w", encoding="utf-8", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=["fio", "birthdate", "group", "gpa"])
                    writer.writeheader()
                    writer.writerows(rows)
                return True
        return False

    def update(self, fio: str, birthdate: str, group: str, gpa: float):
        students = self._read_all()
        updated = False
        
        for student in students:
            if student.get('fio') == fio:
                student['birthdate'] = birthdate
                student['group'] = group
                student['gpa'] = float(gpa)
                updated = True
                break
        
        if updated:
            with self.path.open("w", encoding="utf-8", newline="") as f:
                fieldnames = ["fio", "birthdate", "group", "gpa"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(students)
        
        return updated
    

if __name__ == "__main__":
    print("КОД ЗАПУСТИЛСЯ")
    group= Group('/Users/dariella/Desktop/python_labs/data/lab09/students.csv')

    
    student1 = Student(
        fio="Иванов Иван Иванович",
        birthdate="2000-01-15",
        group="БИВТ-25-8",
        gpa=4.5
    )

    student2 = Student(
        fio="Петрова Мария Сергеевна",
        birthdate="2001-03-22",
        group="БИВТ-25-7",
        gpa=4.8
    )

    student3 = Student(
        fio="Васильева Екатерина Сергеевна",
        birthdate="2002-07-12",
        group="БИВТ-25-8",
        gpa=4.6
    )

    group.add(student1)
    group.add(student2)
    group.add(student3)

    all_students = group.list()
    print(f"Список студентов: {all_students}")

    found_students = group.find("Иванов")
    print(f"Найденные студенты: {found_students}")

    updated = group.update(
        fio="Иванов Иван Иванович",
        birthdate="2000-01-15",
        group="БИВТ-25-9",
        gpa=4.7
    )
    print(f"Обновление выполнено:")

    removed = group.remove("Петрова Мария Сергеевна")
    print(f"Удаление выполнено: {removed}")

    updated_list = group.list()
    print("Обновленный список:", updated_list)


