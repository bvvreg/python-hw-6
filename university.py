"""Модуль який обʼєднує в собі класи
які допомогають управляти університетом: курсами, студентами і вчителями.

Деякі з цих класів частково реалізовані, але більшість класі потребує допрацювання.
Також потрібно реалізувати до кожного класу метод  def __str__(self):
"""

from datetime import date, datetime
from abc import ABC, abstractmethod
from random import random
from typing import List


class Person:
    """Клас Person який обʼєднує в собі базові атрибути кожній людині."""

    def __init__(self, first_name: str, last_name: str, birth_date: date):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date

    def get_age(self):
        """Метод який розрахову і повертає поточний вік людини в залежності від дати народження."""

        today = date.today()
        age = (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )
        return age

    age = property(get_age)

    def __str__(self):
        return f"Person {self.first_name} {self.last_name}, {self.age} years old."


class Course:
    """Клас курсу в університеті. Обʼєднує логіку яка стосується по курсу."""

    def __init__(self, name: str, start_date: datetime, end_date: datetime):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

    def is_active(self) -> bool:
        """Повертає True або False в залежності від того чи курс активний чи ні."""
        if self.start_date <= datetime.now() and datetime.now() <= self.end_date:
            return True

        return False

    def __str__(self):
        return f"Course - {self.name} course. Start: {str(self.start_date)[0:10]}. Finish: {str(self.end_date)[0:10]}"


class UniversityEmployee(Person, ABC):
    """Клас UniversityEmployee який відповідає за працівника університету."""

    def __init__(self, first_name: str, last_name: str, birth_date: date, salary: int):
        super().__init__(first_name, last_name, birth_date)
        self.monthly_salary = salary

    def get_yearly_salary(self):
        """Метод який повертає річну зарплату працівника."""
        return self.monthly_salary * 12

    @abstractmethod
    def answer_question(self, course: Course, question: str) -> bool:
        """Метод який викликається коли студент задає питання по навчанню."""

    def __str__(self):
        return (
            f"Person {self.first_name} {self.last_name}, salary - {self.monthly_salary}"
        )


class Teacher(UniversityEmployee):
    """Клас Teacher який відповідає за вчителя університету."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birth_date: date,
        salary: int,
        course: Course,
    ):
        super().__init__(first_name, last_name, birth_date, salary)
        self.course = course

    def answer_question(self, course: Course, question: str) -> bool:
        """Метод який викликається коли студент задає питання по навчанню."""
        if course.is_active() and self.course == course:
            return True
        return False

    def change_course(self, course: Course) -> bool:
        """Метод який призначений для того щоб призначати викладачу новий курс."""
        if course.is_active() and self.course != course:
            self.course = course
            return True
        return False

    def __str__(self):
        return f"Teacher {self.first_name} {self.last_name}, {self.age} years old, salary - {self.monthly_salary}, {self.course}"


class Mentor(UniversityEmployee):
    """Клас Mentor який відповідає за ментора університету."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birth_date: date,
        salary: int,
        courses: List[Course],
    ):
        super().__init__(first_name, last_name, birth_date, salary)
        self.courses = courses
        self.count_question = 0
        self.list_question = []

    def answer_question(self, course: Course, question: str) -> bool:
        """Метод який викликається коли студент задає питання по навчанню.
        Якщо працівник може відповісти на питання метод повертає True,
        якщо ж працівник не може відповісти метод повертає False.

        Ментор є також дуже розумним і може відповідати на всі запитання.
        Але ментор дуже зайнятий, він може менторити на декількох курсах,
        тому відповідає не на кожне запитання.

        Ментор може відповідати на всі питання якщо він менторить тільки на одному активному курсі (Course.is_active()),
        але якщо курсів більше то ментор відповідає на кожне N заняття, де N кількість активних курсів у ментора.

        Тобто, якщо ментор має 2 активних курси, то ментор буде відповідати на кожне друге запитання.
        Тобто, якщо ментор має 3 активних курси, то ментор буде відповідати на кожне третє запитання.

        Ментор як і вчитель ніколи не відповідає на питання по курсах на яких він не менторить (атрибут courses) і на курсах
        які вже не є активними.

        У ментора гарна памʼять, він запамʼятовує відповіді на запитання, і може відповідати на запитання, на які вже відповідав без черги.
        Питання не унікальні для курсу, тобто для порівняння запитань достатньо використовувати аргумент question.

        Наприклад:
        len(mentor.courses) -> 2 # менторить на 2ух курсах
        mentor.answer_question(some_course, 'Яка домашка?') -> True # на перше питання відповіли
        mentor.answer_question(some_course, 'Чи можу я здати пізніше?') -> False # на друге питання НЕ відповіли
        mentor.answer_question(some_course, 'Чи можу я здати пізніше?') -> True # теж саме питання, але вже знайшли час відповісти
        mentor.answer_question(some_course, 'Яка оцінка?') -> False # не вистачило часу відповісти на це питання

        mentor.answer_question(expired_course, 'Чи можу я здати пізніше?') -> False
        # питання на яке відповідали, і є час відповісти, але питання стосується курсу який вже закінчився

        mentor.answer_question(some_course, 'Що було на уроці?') -> True
        # так як на минуле питання ми не відповідали, на наступне питання є можливість відповісти


        mentor.answer_question(some_course, 'Що було на уроці?') -> True
        # не дивлячись на те що ми дуже зайняті, але маємо змогу відповісти на питання, на яке вже відповідали.

        mentor.answer_question(some_course, 'Як мені виконати ДЗ?') -> False
        # знову зайняті, False


        mentor.answer_question(some_other_course, 'Як мені виконати ДЗ?') -> True
        # те саме питання по іншому курсу, знайшли час відповісти в цей раз

        mentor.answer_question(some_course, 'Як мені виконати ДЗ?') -> True
        # те саме питання по першому курсу, можемо відповідати на це питання поза чергою
        """

        if course.is_active() == False or course not in self.courses:
            return False

        self.count_question += 1
        count_courses = 0

        for element in self.courses:
            if element.is_active() == True:
                count_courses += 1

        if count_courses == 0:
            return False

        if question not in self.list_question:
            self.list_question.append(question)
        else:
            return True

        print(f"Question: {self.list_question}")

        if count_courses > 1:
            if self.count_question % count_courses == 0:
                return False

        return True

    def list_courses(self):
        return f"Mentor courses: {' '.join(str(l) for l in self.courses)}"

    def __str__(self):
        return f"Mentor {self.first_name} {self.last_name}, {self.age} years old, salary - {self.monthly_salary}, {'; '.join(str(l) for l in self.courses)}"

    def change_courses(self, courses: List[Course]) -> bool:
        """Метод який призначений для того щоб призначати ментори нові курси."""
        for checkCourse in courses:
            if Course.is_active(checkCourse) == False:
                return False

        self.courses = courses
        return True


class Student(Person):
    """Клас Student який відповідає за студента університету."""

    def __init__(self, first_name: str, last_name: str, birth_date: date):
        super().__init__(first_name, last_name, birth_date)
        self.list_mark = {}

    def add_mark(self, mark: int, data):
        """Метод який використовується вчителем коли той ставить оцінку студенту."""
        data = str(data)[0:10]
        if 1 <= mark and mark <= 12:
            self.list_mark[data] = mark
            return True

        return False

    def get_all_marks(self) -> List[int]:
        """Метод виводу всіх оцінок стундента."""
        return self.list_mark

    def get_average_mark(self) -> float:
        """Метод який повертає середню оцінку студенту по всіх наданих студенту оцінках."""
        val_dict = list(self.list_mark.values())
        if len(val_dict) > 0:
            return sum(val_dict) / len(val_dict)
        else:
            return 0

    def get_average_by_last_n_marks(self, n: int) -> float:
        """Метод який повертає середню оцінку за певною кількістю останніх оцінок."""
        if n <= 0:
            return 0

        val_dict = list(self.list_mark.values())
        len_dict = len(val_dict) - n
        sum_element = 0
        i = n
        while i > 0:
            sum_element += val_dict[len_dict]
            len_dict += 1
            i -= 1

        return sum_element / n

    def get_average_from_date(self, from_date: datetime) -> float:
        """Метод який повертає середню оцінку за певний період (від певної дати)."""
        sum_element = 0
        n_element = 0
        for element, value in self.list_mark.items():
            if element >= str(from_date)[0:10]:
                sum_element += value
                n_element += 1

        if n_element > 0:
            return sum_element / n_element
        else:
            return 0

    def __str__(self):
        return f"Student {self.first_name} {self.last_name}, {self.age} years old"


class University:
    """Клас University який зберігає студентів, працівників, та курси
    та обʼєднує в собі базові методи потрібні для роботи університету.
    """

    def __init__(
        self,
        name: str,
        courses: List[Course],
        employees: List[UniversityEmployee],
        students: List[Student],
    ):
        self.name = name
        self.courses = courses
        self.employees = employees
        self.students = students

    def get_average_salary(self) -> float:
        """Метод який розраховує і повертає середню місячну зарплату працівників університету."""
        sum_element = 0
        n_element = len(self.employees)
        for element in self.employees:
            sum_element += element.monthly_salary

        if n_element > 0:
            return sum_element / n_element
        else:
            return 0

    def get_average_mark(self) -> float:
        """Метод який розраховує і повертає середню оцінку всіх студентів університету.
        Для цього потрібно враховувати середню оцінку кожно студента.
        """
        sum_element = 0
        n_element = len(self.students)
        for element in self.students:
            sum_element += element.get_average_mark()

        if n_element > 0:
            return sum_element / n_element
        else:
            return 0

    def get_active_courses(self) -> List[Course]:
        """Метод повертає всі активні (в данний момент) курси (Course.is_active())."""
        list_course = []
        for element in self.courses:
            if element.is_active() == True:
                list_course.append(element)

        return " ".join(str(l) for l in list_course)

    def __str__(self) -> str:
        return f"Name University: {self.name},\n {'; '.join(str(l) for l in self.courses)},\n employees - {'; '.join(str(l) for l in self.employees)},\n students - {'; '.join(str(l) for l in self.students)}"
