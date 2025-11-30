class Student:
    def __init__(self, fio: str, age: int, group_number: str, average_score: float):
        self.fio = fio
        self.age = age
        self.group_number = group_number
        self.average_score = average_score

    def print_info(self):
        print(f"ФИО: {self.fio}, Возраст: {self.age}")

    def scholarship(self) -> int:
        if self.average_score == 5.0:
            return 6000
        elif 0 < self.average_score < 5:
            return 4000
        else:
            return 0

    def compare_scholarship(self, other: 'Student') -> str:
        self_sch = self.scholarship()
        other_sch = other.scholarship()
        if self_sch > other_sch:
            return 'больше'
        elif self_sch < other_sch:
            return 'меньше'
        else:
            return 'равно'


class GraduateStudent(Student):
    def __init__(self, fio: str, age: int, group_number: str, average_score: float, thesis_title: str):
        super().__init__(fio, age, group_number, average_score)
        self.thesis_title = thesis_title  

    def scholarship(self) -> int:
        if self.average_score == 5.0:
            return 8000
        elif 0 < self.average_score < 5:
            return 6000
        else:
            return 0


    
if __name__ == "__main__":

    student1 = Student("Иванов Иван Иванович", 20, "ГР-101", 5.0)
    student2 = Student("Петров Петр Петрович", 19, "ГР-102", 4.2)
    grad1 = GraduateStudent("Сидорова Анна Сергеевна", 24, "АСП-201", 5.0, "Машинное обучение в медицине")
    grad2 = GraduateStudent("Кузнецов Дмитрий Алексеевич", 25, "АСП-202", 4.7, "Анализ больших данных")

    student1.print_info()
    grad1.print_info()

    print("Студент 1 стипендия:", student1.scholarship())
    print("Аспирант 1 стипендия:", grad1.scholarship())

    print("Сравнение стипендий (студент1 vs аспирант1):", student1.compare_scholarship(grad1))
    print("Сравнение стипендий (аспирант1 vs аспирант2):", grad1.compare_scholarship(grad2))