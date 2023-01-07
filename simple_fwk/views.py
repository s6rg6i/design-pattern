from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

from patterns.structural import AppRoute, Debug

if TYPE_CHECKING:
    from fwk.request import RequestData
from patterns.creational import Engine
from fwk.response import ResponseData
from fwk.jinja import render
from fwk.view import BaseView

engine = Engine()
engine.load_test_data()  # загрузка тестовых данных
urlpatterns = []


@AppRoute(routes=urlpatterns, url='/')
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


@AppRoute(routes=urlpatterns, url='/about/')
class About(BaseView):
    def get(self, request: RequestData, *args, **kwargs):
        body = render('about.html')
        return ResponseData(request, body=body)

    def post(self, request: RequestData, *args, **kwargs):
        body = render('about.html', post=f'Получен запрос POST: {request.POST}')
        return ResponseData(request, body=body)


@AppRoute(routes=urlpatterns, url='/adm/')
class Adm(BaseView):
    def get(self, request: RequestData, *args, **kwargs):
        body = render('adm.html')
        return ResponseData(request, body=body)


@AppRoute(routes=urlpatterns, url='/add-ctg/')
class AddCategory(BaseView):
    @Debug(name='AddCategory-get')
    def get(self, request: RequestData, *args, **kwargs):
        body = render('adm_add_ctg.html', tree=engine.get_html_tree(engine.category_tree))
        return ResponseData(request, body=body)

    @Debug(name='AddCategory-post')
    def post(self, request: RequestData, *args, **kwargs):
        ctg = request.POST.get('name', [''])[0]
        path = request.POST.get('selected-ctg', [''])[0]
        if engine.create_category(path, ctg):
            return ResponseData(request, body=render('adm_add_ctg.html',
                                                     tree=engine.get_html_tree(engine.category_tree),
                                                     msg=f'Создана новая категория: {ctg}'))
        return ResponseData(request,
                            body=render('adm_add_ctg.html',
                                        tree=engine.create_category(path, ctg),
                                        msg=f'Ошибка создания категории: {ctg}'))


@AppRoute(routes=urlpatterns, url='/add-course/')
class AddCourse(BaseView):
    def get(self, request: RequestData, *args, **kwargs):
        fmts = engine.get_learning_formats()
        body = render('adm_add_course.html', formats=fmts, tree=engine.get_html_tree(engine.category_tree))
        return ResponseData(request, body=body)

    def post(self, request: RequestData, *args, **kwargs):
        path = request.POST.get('selected-ctg', [''])[0]
        name = request.POST.get('name', [''])[0]
        fmt = request.POST.get('format', [''])[0]
        fmts = engine.get_learning_formats()
        if engine.create_course(path, name, fmt):
            return ResponseData(request, body=render('adm_add_course.html',
                                                     formats=fmts,
                                                     tree=engine.get_html_tree(engine.category_tree),
                                                     msg=f'Создан новый курс: {name}'))
        return ResponseData(request, body=render('adm_add_course.html',
                                                 formats=fmts,
                                                 tree=engine.get_html_tree(engine.category_tree),
                                                 msg=f'Ошибка создания курса: {name}'))


@AppRoute(routes=urlpatterns, url='/show-courses/')
class ShowCourses(BaseView):
    def get(self, request: RequestData, *args, **kwargs):
        body = render('adm_show_courses.html', tree=engine.get_html_tree(engine.category_tree))
        return ResponseData(request, body=body)
