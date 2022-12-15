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


class Homepage(BaseView):
    def get(self, request: RequestData, *args, **kwargs):
        body = render(
            'home.html',
            time=str(datetime.now()), lst=[1, 2, 3], session_id=request.extra.get('session_id'))
        return ResponseData(request, body=body)


class Hi(BaseView):
    def get(self, request: RequestData, *args, **kwargs):
        body = render('hello.html', name='незнакомец')
        return ResponseData(request, body=body)

    def post(self, request: RequestData, *args, **kwargs):
        raw_name = request.POST.get('name')
        name = raw_name[0] if raw_name else 'незнакомец'
        body = render('hello.html', name=name)
        return ResponseData(request, body=body)
