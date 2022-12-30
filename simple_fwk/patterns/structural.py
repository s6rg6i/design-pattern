from fwk.url import Url


class AppRoute:
    """ Структурный паттерн - Декоратор """

    def __init__(self, routes, url):
        self.routes = routes  # Сохраняем значение переданного параметра
        self.url = url

    def __call__(self, cls):
        self.routes.append(Url(self.url, cls))
