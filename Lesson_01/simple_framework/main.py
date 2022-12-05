import mimetypes
import pathlib
from wsgiref import util


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:
    """Класс Framework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        # Отработка паттерна "front controller" (request получат все контроллеры)
        request = {k: v for d in self.fronts_lst for k, v in d().items()}

        path = environ['PATH_INFO']  # получаем адрес, по которому выполнен переход
        path = path if path.endswith('/') else f"{path}/"  # Добавляем закрывающий слэш

        # Загрузка статических файлов
        static_url = request.get('static_url', '') or '/static/'  # '/static/' по умолчанию
        if path.startswith(static_url):
            fn = pathlib.Path.cwd() / path[1:]
            if fn.exists():
                start_response("200 OK", [("Content-Type", mimetypes.guess_type(fn)[0])])
                return util.FileWrapper(open(fn, "rb"))

        # отработка паттерна "page controller"
        view = self.routes_lst.get(path, PageNotFound404())  # Находим нужный контроллер
        code, body = view(request)  # Запускаем контроллер

        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
