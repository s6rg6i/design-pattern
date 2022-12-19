from fwk.request import RequestData
from fwk.response import ResponseData


class BaseView:
    def get(self, request: RequestData, *args, **kwargs) -> ResponseData:
        pass

    def post(self, request: RequestData, *args, **kwargs) -> ResponseData:
        pass
