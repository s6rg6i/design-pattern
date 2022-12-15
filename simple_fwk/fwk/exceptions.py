class FwkException(Exception):
    code: str = None
    text: str = None
    headers = ('Content-Type', 'text/html; charset=utf-8')


class NotAllowed(FwkException):
    code = '405	Method Not Allowed'
    text = 'Неподдерживаемый HTTP метод'


class NotFound(FwkException):
    code = '404 Not Found'
    text = 'Страница не найдена'
