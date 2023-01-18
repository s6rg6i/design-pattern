
class BaseMapper:
    def __init__(self, connection) -> None:
        self.connection = connection
        self.cursor = self.connection.cursor()

    def commit(self):
        try:
            self.connection.commit()
            return 'Операция завершилась успешно'
        except Exception as e:
            return f'Ошибка: {str(e)}'

    def all(self, obj):
        statement = f'SELECT * from {getattr(obj, "table_name")}'
        self.cursor.execute(statement)
        result = [obj(*values) for values in self.cursor.fetchall()]
        return result

    def insert(self, obj):
        """ Операция INSERT: 'INSERT INTO books (price, name)  VALUES (?, ?)' """
        _ = [*zip(*[(key, val) for key, val in obj.__dict__.items() if val])]
        fields, values = _
        quan = len(fields)
        tbl = getattr(obj, "table_name")
        statement = f'INSERT INTO {tbl} ({",".join(fields)}) VALUES ({("?," * quan).strip(",")})'
        self.cursor.execute(statement, (*values,))
        return self.commit()

    def update(self, obj, d: dict):
        """ Операция UPDATE: 'UPDATE books SET price = ? WHERE id = ?' """
        _ = [*zip(*[(key, val) for key, val in d.items()])]
        fields, values = _
        fields_str = ",".join([f'{f} = ?' for f in fields])
        tbl = getattr(obj, "table_name")
        statement = f'UPDATE {tbl} SET {fields_str} WHERE id=?'
        self.cursor.execute(statement, (*values, obj.id))
        return self.commit()

    def delete(self, obj):
        """ Операция DELETE: 'DELETE FROM books WHERE id=?' """
        statement = f'DELETE FROM {getattr(obj, "table_name")} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        return self.commit()

