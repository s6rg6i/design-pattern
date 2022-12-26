from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from fwk.request import RequestData
from patterns.creational import Engine
from fwk.response import ResponseData
from fwk.jinja import render
from fwk.view import BaseView

engine = Engine()
engine.load_test_data()  # загрузка тестовых данных


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


class Adm(BaseView):
    def get(self, request: RequestData, *args, **kwargs):
        body = render('adm.html')
        return ResponseData(request, body=body)


class AddCategory(BaseView):
    def get(self, request: RequestData, *args, **kwargs):
        body = render('adm_add_ctg.html')
        return ResponseData(request, body=body)

    def post(self, request: RequestData, *args, **kwargs):
        ctg = request.POST.get('name', [''])[0]
        if engine.create_category(ctg):
            return ResponseData(request, body=render('adm_add_ctg.html', msg=f'Создана новая категория: {ctg}'))
        return ResponseData(request, body=render('adm_add_ctg.html', msg=f'Ошибка создания категории: {ctg}'))


class AddCourse(BaseView):
    def get(self, request: RequestData, *args, **kwargs):
        fmts = engine.get_learning_formats()
        ctgs = engine.categories
        body = render('adm_add_course.html', formats=fmts, categories=ctgs)
        return ResponseData(request, body=body)

    def post(self, request: RequestData, *args, **kwargs):
        ctg = request.POST.get('categories', [''])[0]
        name = request.POST.get('name', [''])[0]
        fmt = request.POST.get('format', [''])[0]
        fmts = engine.get_learning_formats()
        ctgs = engine.categories
        if engine.create_course(ctg, name, fmt):
            msg = f'Создан новый курс: {name}'
            return ResponseData(request, body=render('adm_add_course.html', formats=fmts, categories=ctgs, msg=msg))
        msg = f'Ошибка создания курса: {name}'
        return ResponseData(request, body=render('adm_add_course.html', formats=fmts, categories=ctgs, msg=msg))


class ShowCourses(BaseView):
    def get(self, request: RequestData, *args, **kwargs):
        body = render('adm_show_courses.html', categories=engine.categories)
        return ResponseData(request, body=body)
