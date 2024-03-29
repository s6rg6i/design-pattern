import sqlite3
import threading
from pathlib import Path


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class DomainObject:

    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)


class Person(DomainObject):
    def __init__(self, id_person, first_name, last_name):
        self.id_person = id_person
        self.last_name = last_name
        self.first_name = first_name


class PersonMapper:
    """ Паттерн DATA MAPPER. Слой преобразования данных """

    def __init__(self, conn):
        self.connection = conn
        self.cursor = connection.cursor()

    def find_by_id(self, id_person):
        statement = f"SELECT ID_PERSON, FIRST_NAME, LAST_NAME FROM PERSON WHERE ID_PERSON=?"

        self.cursor.execute(statement, (id_person,))
        result = self.cursor.fetchone()
        if result:
            return Person(*result)
        else:
            raise RecordNotFoundException(f'record with id={id_person} not found')

    def insert(self, person):
        statement = f"INSERT INTO PERSON (FIRST_NAME, LAST_NAME) VALUES (?, ?)"
        self.cursor.execute(statement, (person.first_name, person.last_name))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, person):
        statement = f"UPDATE PERSON SET FIRST_NAME=?, LAST_NAME=? WHERE ID_PERSON=?"
        self.cursor.execute(statement, (person.first_name, person.last_name, person.id_person))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, person):
        statement = f"DELETE FROM PERSON WHERE ID_PERSON=?"
        self.cursor.execute(statement, (person.id_person,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class MapperRegistry:
    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Person):
            return PersonMapper(connection)
        elif isinstance(obj, Category):
            return CategoryMapper


class UnitOfWork:
    """
    Паттерн UNIT OF WORK
    """
    # Работает с конкретным потоком
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

    def insert_new(self):
        for obj in self.new_objects:
            MapperRegistry.get_mapper(obj).insert(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            MapperRegistry.get_mapper(obj).update(obj)

    def delete_removed(self):
        for obj in self.removed_objects:
            MapperRegistry.get_mapper(obj).delete(obj)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class Category(DomainObject):
    def __init__(self, name):
        self.name = name


class CategoryMapper:
    pass


if __name__ == "__main__":
    create_db_sql = '''
    DROP TABLE IF EXISTS person;
    CREATE TABLE person (
        id_person INTEGER PRIMARY KEY AUTOINCREMENT,
        last_name VARCHAR(50),
        first_name VARCHAR(50)
    );
    INSERT INTO person VALUES (1,'Колчина','Анна'),(2,'Романов','Максим'),(3,'Поликарпов','Константин'),
    (4,'Будницкий','Казимир'), (5,'Трус','Иван'),(6,'Агеев','Пётр'),(7,'Иванов','Иван'),(8,'Федоров','Михаил');
    '''
    if not Path('temp.sqlite').exists():
        print("Создаем БД temp.sqlite")
        connection = sqlite3.connect('temp.sqlite')
        cur = connection.cursor()
        cur.executescript(create_db_sql)
        cur.close()
        connection.close()

    connection = sqlite3.connect('temp.sqlite')
    try:
        UnitOfWork.new_current()
        new_person_1 = Person(None, 'Igor', 'Igorev')
        new_person_1.mark_new()

        new_person_2 = Person(None, 'Fedor', 'Fedorov')
        new_person_2.mark_new()

        person_mapper = PersonMapper(connection)
        exists_person_1 = person_mapper.find_by_id(1)
        exists_person_1.mark_dirty()
        print(exists_person_1.first_name)
        exists_person_1.first_name += ' Senior'
        print(exists_person_1.first_name)

        exists_person_2 = person_mapper.find_by_id(2)
        exists_person_2.mark_removed()

        print(UnitOfWork.get_current().__dict__)

        UnitOfWork.get_current().commit()
    except Exception as e:
        print(e.args)
    finally:
        UnitOfWork.set_current(None)

    print(UnitOfWork.get_current())
