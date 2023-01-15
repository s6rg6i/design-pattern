from sqlite3 import connect

from base_mapper import BaseMapper


class User:
    table_name = 'users'

    def __init__(self, user_id: int = None, last_name: str = '', first_name: str = ''):
        self.id = user_id
        self.last_name = last_name
        self.first_name = first_name

    def __repr__(self):
        return f"User({self.id}, {self.last_name}, {self.first_name})"


class Category:
    table_name = 'categories'

    def __init__(self, category_id: int = None, name: str = ''):
        self.id = category_id
        self.name = name

    def __repr__(self):
        return f"Cat({self.id}, {self.name})"


class Course:
    table_name = 'courses'

    def __init__(self, course_id: int = None, name='', description=''):
        self.id = course_id
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Course({self.id}, {self.name})"


class CourseUser:
    table_name = 'course_user'

    def __init__(self, course_id: int, user_id: int):
        self.course_id = course_id
        self.user_id = user_id

    def __repr__(self):
        return f"CourseUser({self.course_id}, {self.user_id})"


class CourseCategory:
    table_name = 'course_category'

    def __init__(self, course_id: int, category_id: int):
        self.course_id = course_id
        self.category_id = category_id

    def __repr__(self):
        return f"CourseCtg({self.course_id}, {self.category_id})"


class Engine:
    """ Основной интерфейс проекта """
    def __init__(self):
        self.base_mapper = BaseMapper(connect('school.sqlite'))
        self.users, self.categories, self.courses, self.course_user, self.course_category = [
            data for data in map(base_mapper.all, (User, Category, Course, CourseUser, CourseCategory))]

    @staticmethod
    def get_obj_by_name(name, lst):
        return next((val for val in lst if val.name == name), None)

    def create_category(self, ctg_path: str, ctg_name: str) -> bool:
        return True

    def create_course(self, ctg_path: str, course_name: str, form: str) -> bool:
        return True

    def create_student(self, name: str, course_name: str):
        return True


if __name__ == "__main__":
    base_mapper = BaseMapper(connect('school.sqlite'))
    users, categories, courses, course_user, course_category = [
        data for data in map(base_mapper.all, (User, Category, Course, CourseUser, CourseCategory))]
    [print(data) for data in (users, categories, courses, course_user, course_category)]

    for new_obj in [User(last_name='Ионов', first_name='Иоан'), Category(name='FrontEnd'), Course(name='Основы JS'),
                    CourseUser(course_id=8, user_id=8), CourseCategory(course_id=5, category_id=5)]:
        base_mapper.insert(new_obj)

    base_mapper.update(users[2], dict(last_name='Сидоров', first_name='Петр'))

    base_mapper.delete(users[1])

    print('\n Обновленные данные')
    [print(data) for data in map(base_mapper.all, (User, Category, Course, CourseUser, CourseCategory))]
