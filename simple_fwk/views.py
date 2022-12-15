from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from fwk.request import RequestData
from fwk.response import ResponseData
from fwk.jinja import render
from fwk.view import BaseView


class Index(BaseView):
    def get(self, request: RequestData, *args, **kwargs):
        user_name = request.extra.get('user_name', 'Незнакомец')
        body = render('index.html', date=str(datetime.now().date()), user_name=user_name)
        return ResponseData(request, body=body)

    def post(self, request: RequestData, *args, **kwargs):
        user_name = request.POST.get('name', ['Незнакомец'])[0]
        if user_name != 'Незнакомец':
            request.extra['login'] = user_name  # новый пользователь
        body = render(
            'index.html',
            date=str(datetime.now().date()),
            post=f'Получен запрос POST: {request.POST}',
            user_name=user_name
        )
        return ResponseData(request, body=body)


class About(BaseView):
    def get(self, request: RequestData, *args, **kwargs):
        body = render('about.html')
        return ResponseData(request, body=body)

    def post(self, request: RequestData, *args, **kwargs):
        body = render('about.html', post=f'Получен запрос POST: {request.POST}')
        return ResponseData(request, body=body)
