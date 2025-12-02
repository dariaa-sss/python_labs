from dataclasses import dataclass
from datetime import datetime, date



@dataclass
class Student:  
    fio: str
    birthdate: str
    group: str
    gpa: float
    
    def __post_init__(self):
        try:
            datetime.strptime(self.birthdate, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Некорректный формат даты: {self.birthdate}. "
                           f"Используйте формат YYYY-MM-DD")
        
        if not (0 <= self.gpa <= 5):
            raise ValueError(f"Средний балл должен быть в диапазоне 0-5, получено: {self.gpa}")
        birth_date = datetime.strptime(self.birthdate, "%Y-%m-%d").date()
        if birth_date > date.today():
            raise ValueError("Дата рождения не может быть в будущем")
    
    def age(self) -> int:
        birth_date = datetime.strptime(self.birthdate, "%Y-%m-%d").date()
        today = date.today()
        
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
            
        return age
    
    def to_dict(self) -> dict:
        return {
            "fio": self.fio,
            "birthdate": self.birthdate,
            "group": self.group,
            "gpa": round(self.gpa, 2)
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Student':
        required_fields = ['fio', 'birthdate', 'group', 'gpa']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Отсутствует обязательное поле: {field}")
        try:
            gpa = float(data['gpa'])
        except (ValueError, TypeError):
            raise ValueError(f"Некорректное значение GPA: {data['gpa']}")
        
        return cls(
            fio=str(data['fio']),
            birthdate=str(data['birthdate']),
            group=str(data['group']),
            gpa=gpa
        )
    
    def __str__(self) -> str:
        age = self.age()
        return (f"Студент: {self.fio}\n"
                f"Возраст: {age} лет\n"
                f"Группа: {self.group}\n"
                f"Средний балл: {self.gpa:.2f}")        