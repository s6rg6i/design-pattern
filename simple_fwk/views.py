from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

from fwk.url import AppRoute
from patterns.behavioral import TemplateView

if TYPE_CHECKING:
    from fwk.request import RequestData
from models import Engine
from fwk.response import ResponseData
from fwk.jinja import render
from fwk.view import BaseView

engine = Engine()
urlpatterns = AppRoute.routes
admin_panel = [("Курсы", ("/add-course", "/upd-course", "/lst-course")),
               ("Категории", ("/add-ctg", "/upd-ctg", "/lst-ctg")),
               ("Студенты", ("/add-stud", "/upd-stud", "/lst-stud")),
               ("Курсы-Категории", ("/add-c-ctg", "/upd-c-ctg", "/lst-c-ctg")),
               ("Курсы-Студенты", ("/add-c-stud", "/upd-c-stud", "/lst-c-stud")), ]


@AppRoute(url='/')
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


@AppRoute(url='/about/')
class About(TemplateView):
    get_template_name = post_template_name = 'about.html'

    def post(self, request: RequestData, **kwargs):
        self.get_context_data = dict(post=f'Получен запрос POST: {request.POST}')
        return super().post(request, **kwargs)


@AppRoute(url='/adm/')
class Adm(TemplateView):
    get_template_name = 'adm.html'
    get_context_data = dict(items=admin_panel)


# *****************************
# ** Courses
# *****************************
@AppRoute(url='/add-course/')
class CourseAdd(BaseView):
    def get(self, request: RequestData, *args, **kwargs):
        return ResponseData(request, body=render('adm_course_add.html', items=admin_panel))

    def post(self, request: RequestData, **kwargs):
        name = request.POST.get('name', [''])[0]
        form = request.POST.get('form', [''])[0]
        descr = request.POST.get('message', [''])[0]
        msg = engine.create_course(name, form, descr)
        return ResponseData(request, body=render('adm_course_add.html', items=admin_panel, msg=msg))


@AppRoute(url='/upd-course/')
class CourseUpd(BaseView):
    def get(self, request: RequestData, **kwargs):
        context = dict(items=admin_panel, courses=engine.courses, course_idx=engine.course_idx)
        engine.course_idx = 1
        return ResponseData(request, body=render('adm_course_upd.html', **context))

    def post(self, request: RequestData, **kwargs):
        if (btn := request.POST.get('btn', [''])[0]) == "sel":
            engine.course_idx = int(request.POST.get('course', [''])[0])
            msg = ''
        elif btn == 'upd':
            name = request.POST.get('name', [''])[0]
            form = request.POST.get('form', [''])[0]
            descr = request.POST.get('message', [''])[0]
            msg = engine.update_course(name, form, descr)
        elif btn == 'del':
            engine.course_idx = int(request.POST.get('course', [''])[0])
            msg = engine.delete_course()
        else:
            msg = 'Неизвестная операция'
        context = dict(items=admin_panel, courses=engine.courses, course_idx=engine.course_idx, msg=msg)
        return ResponseData(request, body=render('adm_course_upd.html', **context))


@AppRoute(url='/lst-course/')
class CoursesLst(BaseView):
    def get(self, request: RequestData, **kwargs):
        return ResponseData(request, body=render('adm_course_lst.html', items=admin_panel, courses=engine.courses))


# *****************************
# ** Categories
# *****************************
@AppRoute(url='/add-ctg/')
class CategoryAdd(BaseView):
    def get(self, request: RequestData, **kwargs):
        return ResponseData(request, body=render('adm_ctg_add.html', items=admin_panel))

    def post(self, request: RequestData, **kwargs):
        name = request.POST.get('name', [''])[0]
        msg = engine.create_category(name)
        return ResponseData(request, body=render('adm_ctg_add.html', items=admin_panel, msg=msg))


@AppRoute(url='/upd-ctg/')
class CategoryUpd(BaseView):
    def get(self, request: RequestData, **kwargs):
        context = dict(items=admin_panel, categories=engine.categories, category_idx=engine.category_idx)
        engine.category_idx = 1
        return ResponseData(request, body=render('adm_ctg_upd.html', **context))

    def post(self, request: RequestData, **kwargs):
        if (btn := request.POST.get('btn', [''])[0]) == "sel":
            engine.category_idx = int(request.POST.get('category', [''])[0])
            msg = ''
        elif btn == 'upd':
            name = request.POST.get('name', [''])[0]
            msg = engine.update_category(name)
        elif btn == 'del':
            engine.category_idx = int(request.POST.get('category', [''])[0])
            msg = engine.delete_category()
        else:
            msg = 'Неизвестная операция'
        context = dict(items=admin_panel, categories=engine.categories, category_idx=engine.category_idx, msg=msg)
        return ResponseData(request, body=render('adm_ctg_upd.html', **context))


@AppRoute(url='/lst-ctg/')
class CategoryLst(BaseView):
    def get(self, request: RequestData, **kwargs):
        return ResponseData(request, body=render('adm_ctg_lst.html', items=admin_panel, categories=engine.categories))

# *****************************
# ** Student
# *****************************


@AppRoute(url='/add-stud/')
class StudentAdd(BaseView):
    def get(self, request: RequestData, *args, **kwargs):
        return ResponseData(request, body=render('adm_student_add.html', items=admin_panel))

    def post(self, request: RequestData, **kwargs):
        lastname = request.POST.get('lastname', [''])[0]
        firstname = request.POST.get('firstname', [''])[0]
        msg = engine.create_student(lastname, firstname)
        return ResponseData(request, body=render('adm_student_add.html', items=admin_panel, msg=msg))


@AppRoute(url='/upd-stud/')
class StudentUpd(BaseView):
    def get(self, request: RequestData, **kwargs):
        context = dict(items=admin_panel, users=engine.users, user_idx=engine.user_idx)
        engine.user_idx = 1
        return ResponseData(request, body=render('adm_student_upd.html', **context))

    def post(self, request: RequestData, **kwargs):
        if (btn := request.POST.get('btn', [''])[0]) == "sel":
            engine.user_idx = int(request.POST.get('user', [''])[0])
            msg = ''
        elif btn == 'upd':
            last_name = request.POST.get('lastname', [''])[0]
            first_name = request.POST.get('firstname', [''])[0]
            msg = engine.update_student(last_name, first_name)
        elif btn == 'del':
            engine.user_idx = int(request.POST.get('user', [''])[0])
            msg = engine.delete_student()
        else:
            msg = 'Неизвестная операция'
        context = dict(items=admin_panel, users=engine.users, user_idx=engine.user_idx, msg=msg)
        return ResponseData(request, body=render('adm_student_upd.html', **context))


@AppRoute(url='/lst-stud/')
class StudentsLst(BaseView):
    def get(self, request: RequestData, **kwargs):
        return ResponseData(request, body=render('adm_student_lst.html', items=admin_panel, users=engine.users))

