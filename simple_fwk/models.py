from sqlite3 import connect

from base_mapper import BaseMapper


class Course:
    table_name = 'courses'

    def __init__(self, course_id: int = None, name='', form='', description=''):
        self.id = course_id
        self.name = name
        self.form = form
        self.description = description

    def __repr__(self):
        return f"Course({self.id}, {self.name}, {self.form})"


class Category:
    table_name = 'categories'

    def __init__(self, category_id: int = None, name: str = ''):
        self.id = category_id
        self.name = name

    def __repr__(self):
        return f"Cat({self.id}, {self.name})"


class User:
    table_name = 'users'

    def __init__(self, user_id: int = None, last_name: str = '', first_name: str = ''):
        self.id = user_id
        self.last_name = last_name
        self.first_name = first_name

    def __repr__(self):
        return f"User({self.id}, {self.last_name}, {self.first_name})"


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
            data for data in map(self.base_mapper.all, (User, Category, Course, CourseUser, CourseCategory))]
        self.user_idx, self.category_idx, self.course_idx = 1, 1, 1

    @staticmethod
    def get_obj_by_name(name, lst):
        return next((val for val in lst if val.name == name), None)

    # *****************************
    # ** Courses
    # *****************************

    def create_course(self, name: str, form: str, descr: str) -> str:
        msg = self.base_mapper.insert(Course(name=name, form=form, description=descr))
        self.courses = self.base_mapper.all(Course)
        return msg

    def update_course(self, name: str, form: str, descr: str) -> str:
        msg = self.base_mapper.update(self.courses[self.course_idx - 1], dict(name=name, form=form, description=descr))
        self.courses = self.base_mapper.all(Course)
        return msg

    def delete_course(self) -> str:
        msg = self.base_mapper.delete(self.courses[self.course_idx - 1])
        self.courses = self.base_mapper.all(Course)
        if self.course_idx > len(self.courses):
            self.course_idx = len(self.courses)
        return msg

    # *****************************
    # ** Categories
    # *****************************

    def create_category(self, ctg_name: str) -> str:
        msg = self.base_mapper.insert(Category(name=ctg_name))
        self.categories = self.base_mapper.all(Category)
        return msg

    def update_category(self, ctg_name: str) -> str:
        msg = self.base_mapper.update(self.categories[self.category_idx - 1], dict(name=ctg_name))
        self.categories = self.base_mapper.all(Category)
        return msg

    def delete_category(self) -> str:
        msg = self.base_mapper.delete(self.categories[self.category_idx - 1])
        self.categories = self.base_mapper.all(Category)
        if self.category_idx > len(self.categories):
            self.category_idx = len(self.categories)
        return msg

    # *****************************
    # ** Student
    # *****************************
    def create_student(self, last_name: str, first_name: str):
        msg = self.base_mapper.insert(User(last_name=last_name, first_name=first_name))
        self.users = self.base_mapper.all(User)
        return msg

    def update_student(self, last_name: str, first_name: str) -> str:
        msg = self.base_mapper.update(self.users[self.user_idx - 1], dict(last_name=last_name, first_name=first_name))
        self.users = self.base_mapper.all(User)
        return msg

    def delete_student(self) -> str:
        msg = self.base_mapper.delete(self.users[self.user_idx - 1])
        self.users = self.base_mapper.all(User)
        if self.user_idx > len(self.users):
            self.user_idx = len(self.users)
        return msg


if __name__ == "__main__":
    temp_base_mapper = BaseMapper(connect('school.sqlite'))
    users, categories, courses, course_user, course_category = [
        data for data in map(temp_base_mapper.all, (User, Category, Course, CourseUser, CourseCategory))]
    [print(data) for data in (users, categories, courses, course_user, course_category)]

    for new_obj in [User(last_name='Ионов', first_name='Иоан'), Category(name='FrontEnd'),
                    Course(name='Основы JS', form='Интерактив', description='Описание курса'),
                    CourseUser(course_id=8, user_id=8), CourseCategory(course_id=5, category_id=5)]:
        temp_base_mapper.insert(new_obj)

    temp_base_mapper.update(users[2], dict(last_name='Сидоров', first_name='Петр'))

    temp_base_mapper.delete(users[1])

    print('\n Обновленные данные')
    [print(data) for data in map(temp_base_mapper.all, (User, Category, Course, CourseUser, CourseCategory))]
