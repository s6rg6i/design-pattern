from copy import deepcopy
import tempfile
from pathlib import Path


class User:
    """ Абстрактный пользователь """

    def __init__(self, name):
        self.name = name


class Teacher(User):
    """ Преподаватель """
    pass


class Student(User):
    """ Студент """

    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class UserFactory:
    """ Порождающий паттерн "ФАБРИЧНЫЙ МЕТОД" - создание пользователя"""
    types = dict(student=Student, teacher=Teacher)

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class CoursePrototype:
    """ Порождающий паттерн "ПРОТОТИП" - курсы обучения"""

    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype):
    """ Базовый класс"""

    def __init__(self, name: str, learning_form: str):
        self.name = name
        self.learning_form = learning_form
        self.users: list[User] = []

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

    def __init__(self, name: str):
        self.name = name
        self.categories: list[Category] = []  # подкатегории
        self.courses: list[Course] = []  # курсы

    def __repr__(self):
        # return f'{self.name} -> {self.categories}'
        return f'K[{self.name}]'


class Engine:
    """ Основной интерфейс проекта """

    def __init__(self):
        self.category_tree: Category = Category('ROOT')
        self.students: list[User] = []
        self.courses: list[Course] = []

    @staticmethod
    def get_obj_by_name(name, lst):
        return next((val for val in lst if val.name == name), None)

    @staticmethod
    def get_learning_formats():
        return tuple(CourseFactory.learning_formats.keys())

    def get_category_node(self, ctg_path: str) -> Category or None:
        ctg = self.category_tree  # корневой узел
        ctg_path = ctg_path[4:] if ctg_path.startswith('ROOT') else ctg_path
        for sub_ctg in map(str.strip, ctg_path.split('->')):  # пропускаем ROOT
            if not sub_ctg:
                continue
            if not (ctg := self.get_obj_by_name(sub_ctg, ctg.categories)):
                return None
        return ctg

    def create_category(self, ctg_path: str, ctg_name: str) -> bool:
        if not (ctg_node := self.get_category_node(ctg_path)):
            return False
        if all([ctg_name, not self.get_obj_by_name(ctg_name, ctg_node.categories)]):
            ctg_node.categories.append(Category(ctg_name))
            return True
        return False

    def create_course(self, ctg_path: str, course_name: str, form: str) -> bool:
        if not (ctg_node := self.get_category_node(ctg_path)):
            return False
        if all([course_name, form in CourseFactory.learning_formats]):
            if not self.get_obj_by_name(course_name, ctg_node.courses):
                course = CourseFactory.create(course_name, form)
                ctg_node.courses.append(course)
                if not self.get_obj_by_name(course_name, self.courses):
                    self.courses.append(course)
                return True
        return False

    def create_student(self, name: str, course_name: str):
        if not name:
            return False
        if not (student := self.get_obj_by_name(name, self.students)):
            student = UserFactory.create('student', name)
            self.students.append(student)
        if course_name:
            if course := self.get_obj_by_name(course_name, self.courses):
                if not self.get_obj_by_name(name, course.users):
                    course.users.append(student)
            return True
        return False

    def get_nodes(self, tree: Category):
        yield f'<li>{tree.name}'
        # yield f'<div class="course">[{", ".join([course.name for course in tree.courses])}]</div>'
        yield f'<div>[{", ".join([course.name for course in tree.courses])}]</div>'
        for child in tree.categories:
            yield '<ul>'
            yield from self.get_nodes(child)
            yield '</ul>'
        yield '</li>'

    def get_html_tree(self, tree: Category):
        html_tree = "\n".join([name for name in self.get_nodes(tree)])
        return f'<div class ="container" ><ul class ="tree" id="tree" >{html_tree}</ul></div>'

    def load_test_data(self):
        test_categories = [
            ['ROOT->', 'Программирование'],
            ['->Программирование', 'Программирование на Python'],
            ['->Программирование->Программирование на Python', 'Frameworks'],
            ['->Программирование', 'Программирование на Java'],
            ['->Программирование', 'JavaScript'],
            ['->', 'Общий блок'],
            ['->Общий блок', 'Введение'],
            ['->Общий блок', 'WEB'],
            ['->Общий блок', 'Компьютерные сети'],
        ]
        test_courses = [
            ('->Программирование->Программирование на Python', ['Основы языка Python', 'Python ООП']),
            ('->Программирование->Программирование на Python->Frameworks', ['Django', 'DRF', 'Flask', 'FastAPI']),
            ('->Программирование->Программирование на Java', ['Введение в JAVA', 'ООП на JAVA']),
            ('->Общий блок->Введение', ['Основы программирования', 'Введение в алгоритмы', 'Git']),
            ('->Общий блок->WEB', ['HTML / CSS', 'Веб разработка']),
            ('->Общий блок->Компьютерные сети', ['TCP/IP', 'Методы сбора и обработки данных в сети Интернет']),
        ]

        formats = self.get_learning_formats()
        for path, ctg_name in test_categories:
            self.create_category(path, ctg_name)
        for path, course_names in test_courses:
            for course in course_names:
                self.create_course(path, course, formats[len(course) % len(formats)])


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
    print(engine.get_html_tree(engine.category_tree))

    # print(engine.category_tree)
    # logger1, logger2 = Logger('log1'), Logger('log2')
    # print(logger1.filename, logger2.filename)
    # print(Logger('log1').filename, Logger('log2').filename)  # убеждаемся, что экземпляр класса один для имени
    # Logger('log1').log(engine.category_tree)
    # Logger('log2').log(engine.category_tree)
