from fwk.request import RequestData


class ResponseData:
    def __init__(self, request: RequestData, status_code=200, body='', extra: dict = None):
        self.request = request
        self.status_code = status_code
        self.body = body
        self.headers = [('Content-Type', 'text/html; charset=utf-8'), ]

    def update_headers(self, head: tuple):
        self.headers.append(head)
