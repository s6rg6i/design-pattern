from json import dumps, loads

from fwk.jinja import render
from fwk.request import RequestData
from fwk.response import ResponseData
from fwk.view import BaseView


class Observer:
    """ Поведенческий паттерн - наблюдатель """

    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SmsNotifier(Observer):

    def update(self, subject):
        print('SMS->', 'к нам присоединился', subject.students[-1].name)


class EmailNotifier(Observer):

    def update(self, subject):
        print(('EMAIL->', 'к нам присоединился', subject.students[-1].name))


class TemplateView(BaseView):
    """ Поведенческий паттерн - Шаблонный метод """
    get_template_name = 'template.html'
    get_context_data = {}
    post_template_name = 'template.html'
    post_context_data = {}
    post_args = []
    ok_msg = ''
    err_msg = ''

    def get(self, request: RequestData, **kwargs):
        template = self.get_template_name
        context = self.get_context_data
        body = render(template, **context)
        return ResponseData(request, body=body)

    def create_obj(self, *args) -> bool:
        return True

    def post(self, request: RequestData, **kwargs):
        self.create_obj(*self.post_args)
        template = self.post_template_name
        context = self.post_context_data
        body = render(template, **context)
        return ResponseData(request, body=body)


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)
