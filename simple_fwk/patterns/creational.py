from copy import deepcopy
import tempfile
from pathlib import Path


class User:
    """ Абстрактный пользователь """
    pass


class Teacher(User):
    """ Преподаватель """
    pass


class Student(User):
    """ Студент """
    pass


class UserFactory:
    """ Порождающий паттерн "ФАБРИЧНЫЙ МЕТОД" - создание пользователя"""
    types = dict(student=Student, teacher=Teacher)

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


class CoursePrototype:
    """ Порождающий паттерн "ПРОТОТИП" - курсы обучения"""

    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype):
    """ Базовый класс"""

    def __init__(self, name, learning_form):
        self.name = name
        self.learning_form = learning_form

    def __repr__(self):
        return f'{self.name}'


class InteractiveCourse(Course):
    """ Интерактивный курс """
    pass


class RecordCourse(Course):
    """ Курс в записи """
    pass


class OffLine(Course):
    """ Курс в живую """
    pass


class LongRead(Course):
    """ Лонгрид """
    pass


class CourseFactory:
    """ Порождающий паттерн "ФАБРИЧНЫЙ МЕТОД" - создание курса"""
    learning_formats = dict(interactive=InteractiveCourse, record=RecordCourse, offline=OffLine, longread=LongRead)

    @classmethod
    def create(cls, name, form):
        return cls.learning_formats[form](name, form)


class Category:
    """ Категория """

    def __init__(self, name):
        self.name = name
        self.courses = []  # курсы

    def __repr__(self):
        return f'{self.name} : {self.courses}'


class Engine:
    """ Основной интерфейс проекта """

    def __init__(self):
        self.categories = []

    @staticmethod
    def get_obj_by_name(_name, _iter):
        return next((val for val in _iter if val.name == _name), None)

    @staticmethod
    def get_learning_formats():
        return tuple(CourseFactory.learning_formats.keys())

    def create_category(self, ctg_name):
        if all([ctg_name, not self.get_obj_by_name(ctg_name, self.categories)]):
            self.categories.append(Category(ctg_name))
            return True
        return False

    def create_course(self, ctg_name, course_name, form):
        if all([ctg_name, course_name, form in CourseFactory.learning_formats]):
            if ctg_obj := self.get_obj_by_name(ctg_name, self.categories):
                if not self.get_obj_by_name(course_name, ctg_obj.courses):
                    ctg_obj.courses.append(CourseFactory.create(course_name, form))
                    return True
        return False

    def load_test_data(self):
        courses = (("Основы программирования", ("Введение в алгоритмы", "Git", "Английский для IT-специалистов")),
                   ('Программирование на Python', ("Основы Python", "Python ООП", "Django Framework", "Django REST")),
                   ('Программирование на Java', ("Основы языка Java", "Java ООП")),
                   ('JavaScript', ()),
                   ('Networks', ("Компьютерные сети", "Методы сбора и обработки данных из сети Интернет")),)
        formats = self.get_learning_formats()
        for ctg, courses in courses:
            self.create_category(ctg)
            for course in courses:
                self.create_course(ctg, course, formats[len(course) % len(formats)])


class SingletonByName(type):
    """ Порождающий паттерн ОДИНОЧКА(SINGLETON) """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instances = {}

    def __call__(cls, *args, **kwargs):
        name = args[0] if args else kwargs['name'] if kwargs else ''
        if name not in cls.__instances:
            cls.__instances[name] = super().__call__(*args, **kwargs)
        return cls.__instances[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name
        self.filename = Path(tempfile.gettempdir()) / f'{name}.log'

    def log(self, *args):
        Path(self.filename).write_text(f'log--->: {args}')


if __name__ == "__main__":
    engine = Engine()
    engine.load_test_data()
    logger1, logger2 = Logger('log1'), Logger('log2')
    print(logger1.filename, logger2.filename)
    print(Logger('log1').filename, Logger('log2').filename)  # убеждаемся, что экземпляр класса один для имени
    Logger('log1').log(engine.categories)
    Logger('log2').log(engine.categories)
