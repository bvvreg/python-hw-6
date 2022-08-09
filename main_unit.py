from datetime import date, datetime, timedelta
from unittest import TestCase, skip, expectedFailure
from university import Course, Mentor, Teacher, Student, University

print("\nUnit test module University")
print("----------------------------------------")


class UniversityTestCase(TestCase):
    def setUp(self):
        self.python_course = Course(
            "Python", datetime.now(), datetime.now() + timedelta(days=30)
        )

        self.js_course = Course(
            "JavaScript",
            datetime.now() - timedelta(days=20),
            datetime.now() - timedelta(days=10),
        )

        self.qa_course = Course(
            "QA engineer",
            datetime.now() - timedelta(days=10),
            datetime.now() + timedelta(days=30),
        )
        self.alex_student = Student("Alex", "Stp", date(1995, 7, 8))

        self.nik_student = Student("Nik", "Fial", date(1998, 10, 22))

        self.bred_teacher = Teacher(
            "Bred", "Cmp", date(1974, 6, 25), 2000, self.python_course
        )

        self.koli_mentor = Mentor(
            "Koli",
            "Key",
            date(1987, 3, 13),
            1200,
            [self.python_course, self.js_course, self.qa_course],
        )

        self.harvard_university = University(
            "Harvard",
            [self.python_course, self.js_course, self.qa_course],
            [self.bred_teacher, self.koli_mentor],
            [self.alex_student, self.nik_student],
        )

        self.nik_student.add_mark(12, datetime(2022, 7, 28))
        self.nik_student.add_mark(1, datetime(2022, 7, 29))
        self.nik_student.add_mark(5, datetime(2022, 7, 26))

        self.alex_student.add_mark(10, datetime(2022, 7, 29))
        self.alex_student.add_mark(2, datetime(2022, 7, 25))

    def tearDown(self):
        del self.python_course
        del self.js_course
        del self.qa_course
        del self.alex_student
        del self.nik_student
        del self.bred_teacher
        del self.koli_mentor
        del self.harvard_university

    def test_01_change_course_teacher(self):
        """Зміна курсів у вчителя"""
        self.assertTrue(self.bred_teacher.change_course(self.qa_course))

    def test_02_change_ended_course_teacher(self):
        """Спроба заміни вчителю курсу, який не активний"""
        self.assertFalse(self.bred_teacher.change_course(self.js_course))

    def test_03_teacher_answer_question(self):
        """Відповідь вчителя на дійсний курс"""
        self.assertTrue(
            self.bred_teacher.answer_question(self.python_course, "Do you love coffee?")
        )

    def test_04_teacher_ended_course_answer_question(self):
        """Відповідь вчителя на не активний курс"""
        self.assertFalse(
            self.bred_teacher.answer_question(self.js_course, "Do you love coffee?")
        )

    def test_05_change_course_mentor(self):
        """Заміна курсів ментору"""
        self.assertTrue(
            self.koli_mentor.change_courses([self.qa_course, self.python_course])
        )

    def test_06_change_ended_course_mentor(self):
        """Спроба заміни не активними курсами ментору"""
        self.assertFalse(
            self.koli_mentor.change_courses([self.js_course, self.python_course])
        )

    def test_07_get_all_marks(self):
        """Список оцінок студента"""
        self.assertDictContainsSubset(
            self.nik_student.get_all_marks(),
            {"2022-07-26": 5, "2022-07-28": 12, "2022-07-29": 1},
        )

    def test_08_get_average_mark(self):
        """Середня оцінка студента"""
        self.assertEqual(self.nik_student.get_average_mark(), 6.0)

    def test_09_get_average_by_last_n_marks(self):
        """Середня оцінка по n останніх оцінок студента"""
        self.assertEqual(self.nik_student.get_average_by_last_n_marks(2), 3.0)

    def test_10_get_average_from_date(self):
        """Середня оцінка по останнім від date оцінкам студента"""
        self.assertEqual(
            self.nik_student.get_average_from_date(datetime(2022, 7, 28)), 6.5
        )

    def test_11_get_average_salary(self):
        """Середня зарплатня по університету"""
        self.assertEqual(self.harvard_university.get_average_salary(), 1600)

    def test_12_get_average_mark(self):
        """Середня оцінка по університету"""
        self.assertEqual(self.harvard_university.get_average_mark(), 6.0)

    def test_13_get_active_courses(self):
        """Кількість активних курсів по університету"""
        self.assertEqual(len(self.harvard_university.get_active_courses()), 128)

    def test_14_mentor_answer_question(self):
        """Відповіді на питання ментора"""
        self.assertFalse(
            self.koli_mentor.answer_question(self.js_course, "Яка домашка?")
        )

    def test_15_mentor_answer_question(self):
        self.assertTrue(
            self.koli_mentor.answer_question(self.python_course, "Яка домашка?")
        )

    def test_16_mentor_answer_question(self):
        self.koli_mentor.answer_question(self.python_course, "Яка домашка?")
        self.assertFalse(
            self.koli_mentor.answer_question(
                self.python_course, "Чи можу я здати пізніше?"
            )
        )

    def test_17_mentor_answer_question(self):
        self.koli_mentor.answer_question(self.python_course, "Яка домашка?")
        self.koli_mentor.answer_question(self.python_course, "Чи можу я здати пізніше?")
        self.assertTrue(
            self.koli_mentor.answer_question(
                self.python_course, "Чи можу я здати пізніше?"
            )
        )

    def test_18_mentor_answer_question(self):
        self.koli_mentor.answer_question(self.python_course, "Яка домашка?")
        self.koli_mentor.answer_question(self.python_course, "Чи можу я здати пізніше?")
        self.koli_mentor.answer_question(self.python_course, "Чи можу я здати пізніше?")
        self.assertFalse(
            self.koli_mentor.answer_question(self.python_course, "Яка оцінка?")
        )

    def test_19_mentor_answer_question(self):
        self.koli_mentor.answer_question(self.python_course, "Яка домашка?")
        self.koli_mentor.answer_question(self.python_course, "Чи можу я здати пізніше?")
        self.koli_mentor.answer_question(self.python_course, "Чи можу я здати пізніше?")
        self.koli_mentor.answer_question(self.python_course, "Яка оцінка?")
        self.assertFalse(
            self.koli_mentor.answer_question(self.js_course, "Чи можу я здати пізніше?")
        )

    def test_20_mentor_answer_question(self):
        self.koli_mentor.answer_question(self.python_course, "Яка домашка?")
        self.koli_mentor.answer_question(self.python_course, "Чи можу я здати пізніше?")
        self.koli_mentor.answer_question(self.python_course, "Чи можу я здати пізніше?")
        self.koli_mentor.answer_question(self.python_course, "Яка оцінка?")
        self.koli_mentor.answer_question(self.js_course, "Чи можу я здати пізніше?")
        self.assertTrue(
            self.koli_mentor.answer_question(self.qa_course, "Що було на уроці?")
        )

    def test_21_mentor_answer_question(self):
        self.koli_mentor.answer_question(self.python_course, "Яка домашка?")
        self.koli_mentor.answer_question(self.python_course, "Чи можу я здати пізніше?")
        self.koli_mentor.answer_question(self.python_course, "Чи можу я здати пізніше?")
        self.koli_mentor.answer_question(self.python_course, "Яка оцінка?")
        self.koli_mentor.answer_question(self.js_course, "Чи можу я здати пізніше?")
        self.koli_mentor.answer_question(self.python_course, "Що було на уроці?")
        self.assertTrue(
            self.koli_mentor.answer_question(self.python_course, "Що було на уроці?")
        )

    def test_22_mentor_answer_question(self):
        self.koli_mentor.answer_question(self.python_course, "Яка домашка?")
        self.koli_mentor.answer_question(self.python_course, "Чи можу я здати пізніше?")
        self.koli_mentor.answer_question(self.python_course, "Чи можу я здати пізніше?")
        self.koli_mentor.answer_question(self.python_course, "Яка оцінка?")
        self.koli_mentor.answer_question(self.js_course, "Чи можу я здати пізніше?")
        self.koli_mentor.answer_question(self.python_course, "Що було на уроці?")
        self.koli_mentor.answer_question(self.python_course, "Що було на уроці?")
        self.assertTrue(
            self.koli_mentor.answer_question(self.python_course, "Як мені виконати ДЗ?")
        )

    def test_23_mentor_answer_question(self):
        self.koli_mentor.answer_question(self.python_course, "Яка домашка?")
        self.koli_mentor.answer_question(self.python_course, "Чи можу я здати пізніше?")
        self.koli_mentor.answer_question(self.python_course, "Чи можу я здати пізніше?")
        self.koli_mentor.answer_question(self.python_course, "Яка оцінка?")
        self.koli_mentor.answer_question(self.js_course, "Чи можу я здати пізніше?")
        self.koli_mentor.answer_question(self.python_course, "Що було на уроці?")
        self.koli_mentor.answer_question(self.python_course, "Що було на уроці?")
        self.koli_mentor.answer_question(self.python_course, "Як мені виконати ДЗ?")
        self.assertTrue(
            self.koli_mentor.answer_question(self.qa_course, "Як мені виконати ДЗ?")
        )

    def test_24_mentor_answer_question(self):
        self.koli_mentor.answer_question(self.python_course, "Яка домашка?")
        self.koli_mentor.answer_question(self.python_course, "Чи можу я здати пізніше?")
        self.koli_mentor.answer_question(self.python_course, "Чи можу я здати пізніше?")
        self.koli_mentor.answer_question(self.python_course, "Яка оцінка?")
        self.koli_mentor.answer_question(self.js_course, "Чи можу я здати пізніше?")
        self.koli_mentor.answer_question(self.python_course, "Що було на уроці?")
        self.koli_mentor.answer_question(self.python_course, "Що було на уроці?")
        self.koli_mentor.answer_question(self.python_course, "Як мені виконати ДЗ?")
        self.koli_mentor.answer_question(self.qa_course, "Як мені виконати ДЗ?")
        self.assertTrue(
            self.koli_mentor.answer_question(self.python_course, "Як мені виконати ДЗ?")
        )
