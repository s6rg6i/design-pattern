import sqlite3

create_db_sql = '''
DROP TABLE IF EXISTS courses;
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50),
    form VARCHAR(50),
    description Text
);
INSERT INTO courses VALUES (1,'Основы языка Python','',''), (2,'Алгоритмы Python','',''), (3,'Django','',''),
(4,'DRF','',''), (5,'Flask','',''), (6,'Архитектура и шаблоны проектирования на Python','',''),
(7,'Асинхронный чат','',''), (8,'HTML CSS','',''), (9,'Linux. Рабочая станция','',''), (10,'Git. Базовый курс','',''),
(11,'MySQL','',''), (12,'Компьютерные сети. Основы.','','');

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name VARCHAR(50),
    first_name VARCHAR(50)
);
INSERT INTO users VALUES (1,'Колчина','Анна'),(2,'Романов','Максим'),(3,'Поликарпов','Константин'),(4,'Буйницкий','Казимир'),
(5,'Трус','Иван'),(6,'Агеев','Пётр'),(7,'Иванов','Иван'),(8,'Федеровский','Михаил'),(9,'Чернявский','Михаил'),(10,'Русов','Пётр');

DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100)
);
INSERT INTO categories VALUES (1,'Программирование на Python'), (2,'Python Frameworks'), (3,'Python разработчик'),(4,'Базы данных'),
(5,'Компьютерные сети'), (6,'Веб разработчик'), (7,'Cистема управления версиями'), (8,'Операционные системы');

DROP TABLE IF EXISTS course_user;
CREATE TABLE course_user (
    course_id BIGINT UNSIGNED NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (course_id, user_id),
    FOREIGN KEY (course_id) REFERENCES courses(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE
);
INSERT INTO course_user VALUES (1,1),(1,3),(2,1),(2,3),(3,1),(3,2),(3,3),(4,1),(4,2),(4,3),(5,1),(5,2),(5,3),(6,1),
(6,3),(7,1),(7,3),(8,6),(9,8),(10,7),(11,4),(12,5),(12,6),(12,7),(12,8),(12,9),(12,10);

DROP TABLE IF EXISTS course_category;
CREATE TABLE course_category (
    course_id BIGINT UNSIGNED NOT NULL,
    category_id BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (course_id, category_id),
    FOREIGN KEY (course_id) REFERENCES courses(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON UPDATE CASCADE ON DELETE CASCADE
);
INSERT INTO course_category VALUES (1,1),(1,3),(2,1),(2,3),(3,1),(3,2),(3,3),(4,1),(4,2),(4,3),(5,1),(5,2),(5,3),(6,1),
(6,3),(7,1),(7,3),(8,6),(9,8),(10,7),(11,4),(12,5);
'''

con = sqlite3.connect('school.sqlite')
cur = con.cursor()
cur.executescript(create_db_sql)
cur.close()
con.close()
