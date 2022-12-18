from http import HTTPStatus
from pathlib import Path
from typing import List, Type
# from wsgiref import util

from fwk.url import Url
from fwk.request import RequestData
from fwk.response import ResponseData
from fwk.exceptions import NotAllowed, FwkException, NotFound
from fwk.user import users, User
from fwk.view import BaseView, StaticFile
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
            view = self._find_view(request.path_info)()

            if request.GET:
                print(f'Получен Get запрос с параметрами {request.GET}')
            if request.POST:
                print(f'Получен Post запрос с параметрами {request.POST}')
            if request.COOKIE:
                print(f'Получены COOKIE: {request.COOKIE}')

            # 'Front Controller' до 'Page Controller'
            self._apply_middleware_to_request(request, users)

            # 'Page Controller'
            response = self._get_response(view, request)  # 'View'

            # 'Front Controller' после 'Page Controller'
            self._apply_middleware_to_response(response, users)

            # Отправляем клиенту
            status_code = self._get_status(response.status_code)
            start_response(status_code, response.headers)
            if response.body:
                return iter([response.body.encode('utf-8')])
            # if file := request.file:
            #     return util.FileWrapper(open(file, "rb"))

        except FwkException as e:
            start_response(e.code, [e.headers])
            return iter([e.text.encode('utf-8')])

    def _find_view(self, requested_url: str) -> Type[BaseView]:
        """ Возвращаем view по заданному url """

        for url in self.urls:  # Ищем в url списке доступных
            if requested_url == url.url:
                return url.view
        # Статика
        if requested_url.startswith(self.settings.get('STATIC')):  # Загрузка статических файлов
            fn = Path(self.settings.get('BASE_DIR', '')) / requested_url[1:-1]  # убираем крайние слэши
            if fn.exists():
                return StaticFile
        else:
            raise NotFound  # Страница не найдена

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
