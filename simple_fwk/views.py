from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

from patterns.behavioral import TemplateView
from patterns.structural import AppRoute

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
class About(TemplateView):
    get_template_name = post_template_name = 'about.html'

    def post(self, request: RequestData, **kwargs):
        self.get_context_data = dict(post=f'Получен запрос POST: {request.POST}')
        return super().post(request, **kwargs)


@AppRoute(routes=urlpatterns, url='/adm/')
class Adm(TemplateView):
    get_template_name = 'adm.html'


@AppRoute(routes=urlpatterns, url='/add-ctg/')
class AddCategory(BaseView):
    def get(self, request: RequestData, *args, **kwargs):
        body = render('adm_add_ctg.html', tree=engine.get_html_tree(engine.category_tree))
        return ResponseData(request, body=body)

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
class ShowCourses(TemplateView):
    get_template_name = 'adm_show_courses.html'
    get_context_data = dict(tree=engine.get_html_tree(engine.category_tree))


@AppRoute(routes=urlpatterns, url='/add-students/')
class AddStudents(TemplateView):
    get_template_name = post_template_name = 'adm_add_students.html'
    get_context_data = post_context_data = dict(courses=engine.courses)

    def post(self, request: RequestData, **kwargs):
        self.post_args = [request.POST.get('name', [''])[0], request.POST.get('course', [''])[0]]
        return super().post(request, **kwargs)

    def create_obj(self, name, course_name):
        if engine.create_student(name, course_name):
            msg = f'Студент {name} добавлен на курс {course_name} '
        else:
            msg = f'Ошибка добавления студента: {name}'
        self.post_context_data.update(dict(msg=msg))


@AppRoute(routes=urlpatterns, url='/show-students/')
class ShowCourses(TemplateView):
    get_template_name = 'adm_show_students.html'
    get_context_data = dict(courses_list=engine.courses)
