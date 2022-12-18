from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fwk.request import RequestData
    from fwk.response import ResponseData


class BaseView:
    def get(self, request: RequestData, *args, **kwargs) -> ResponseData:
        pass

    def post(self, request: RequestData, *args, **kwargs) -> ResponseData:
        pass


class StaticFile(BaseView):
    def get(self, request: RequestData, *args, **kwargs):
        body = f'Загрузка файла {request.path_info}'
        return ResponseData(request, body=body)
