from typing import AnyStr
from urllib.parse import parse_qs


class RequestData:
    def __init__(self, environ: dict):
        self.environ = environ
        self.path_info = self._get_path_info()
        self.method = environ['REQUEST_METHOD'].lower()
        self.GET = self._get_get_params()
        self.POST = self._get_post_params()
        self.COOKIE = self._get_cookies()
        self.extra = {}

    def _get_path_info(self) -> str:
        """ Добавляем отсутствующий слэш в конце """
        path = self.environ.get('PATH_INFO', '/')
        return path if path.endswith('/') else f"{path}/"

    def _get_get_params(self) -> dict[AnyStr, list[AnyStr]]:
        """ Получаем словарь GET параметров"""
        return parse_qs(self.environ.get('QUERY_STRING', ''))

    def _get_post_params(self) -> dict[AnyStr, list[AnyStr]]:
        """ Получаем словарь POST параметров"""
        try:
            content_length = int(self.environ.get('CONTENT_LENGTH'))
        except (ValueError, TypeError):
            content_length = 0
        body = self.environ['wsgi.input'].read(content_length) if content_length else b''
        return parse_qs(body.decode(encoding='utf-8'))

    def _get_cookies(self) -> dict[AnyStr, list[AnyStr]]:
        if cookie := self.environ.get('HTTP_COOKIE', None):
            return parse_qs(cookie)
        return {}
