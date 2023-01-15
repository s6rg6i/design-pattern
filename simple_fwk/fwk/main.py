import mimetypes
from http import HTTPStatus
from pathlib import Path
from typing import List, Type
from wsgiref import util, simple_server

from fwk.url import Url
from fwk.request import RequestData
from fwk.response import ResponseData
from fwk.exceptions import NotAllowed, FwkException, NotFound
from fwk.user import users, User
from fwk.view import BaseView
from fwk.middleware import BaseMiddleware


class Framework:
    def __init__(self, urls: List[Url], settings: dict, middlewares: List[Type[BaseMiddleware]]):
        self.urls = urls
        self.settings = settings
        self.middlewares = middlewares

    def __call__(self, environ: dict, start_response):
        """ Обработка HTTP запросов пользователя"""
        try:
            request = RequestData(environ)  # GET, POST, COOKIE, обработанные environ

            if static_file := self._get_static_file(request.path_info):
                if mime := mimetypes.guess_type(Path(static_file)):
                    start_response("200 OK", [("Content-Type", mime[0])])
                    return util.FileWrapper(open(static_file, "rb"))

            view = self._find_view(request.path_info)()

            # 'Front Controller' до 'Page Controller'
            self._apply_middleware_to_request(request, users)

            # 'Page Controller'
            response = self._get_response(view, request)  # 'View'

            # 'Front Controller' после 'Page Controller'
            self._apply_middleware_to_response(response, users)

            # Отправляем клиенту
            start_response(self._get_status(response.status_code), response.headers)
            if response.body:
                return iter([response.body.encode('utf-8')])

        except FwkException as e:
            start_response(e.code, [e.headers])
            return iter([e.text.encode('utf-8')])

    def _find_view(self, requested_url: str) -> Type[BaseView]:
        """ Возвращаем view по заданному url """
        for url in self.urls:  # Ищем в url списке доступных
            if requested_url == url.url:
                return url.view
        raise NotFound  # Страница не найдена

    def _get_static_file(self, requested_url: str) -> str:
        if requested_url.startswith(self.settings.get('STATIC')):  # Запрошен статический файл ?
            fn = Path(self.settings.get('BASE_DIR', '')) / requested_url[1:-1]  # убираем крайние слэши
            if fn.is_file():
                return str(fn)
        return ''

    @staticmethod
    def _get_status(code: int) -> str:
        """ Получить строку HTTP Status Code (Value, Description) по номеру """
        """ See http://www.iana.org/assignments/http-status-codes """
        try:
            return f'{code} {HTTPStatus(code).phrase}'
        except ValueError:  # код отсутствует в таблице
            return f'{code} Unassigned'

    def _apply_middleware_to_request(self, request: RequestData, users_: List[User]):
        for front in self.middlewares:
            front().to_request(request, users_)

    @staticmethod
    def _get_response(view: BaseView, request: RequestData) -> ResponseData:
        if not hasattr(view, request.method):
            raise NotAllowed
        return getattr(view, request.method)(request)

    def _apply_middleware_to_response(self, response: ResponseData, users_: List[User]):
        for front in self.middlewares:
            front().to_response(response, users_)


class DebugApplication(Framework):
    """ WSGI-application (логирующий). Как основной, только выводит информацию о запросе в консоль """

    def __init__(self, urls: List[Url], settings: dict, middlewares: List[Type[BaseMiddleware]]):
        self.application = Framework(urls, settings, middlewares)

    def __call__(self, env, start_response):
        print('DEBUG MODE:')
        print(env)
        return self.application(env, start_response)


class FakeApplication:
    """ WSGI-application (фейковый). На все запросы пользователя отвечает: 200 OK, Hello from Fake """

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']


if __name__ == "__main__":
    if input('Введите 0 - для запуска FakeApplication, иначе запуск DebugApplication\n') == '0':
        print('--- FakeApplication:')
        app = FakeApplication()
    else:
        print('--- DebugApplication:')
        app = DebugApplication()
    httpd = simple_server.make_server("", 8000, app)
    print(f"FakeServer 127.0.0.1 on port 8000, control-C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down.")
        httpd.server_close()
