from time import time

from fwk.url import Url


class AppRoute:
    """ Структурный паттерн - Декоратор - добавляет url-ы, как во Flask """

    def __init__(self, routes, url):
        self.routes = routes  # Сохраняем значение переданного параметра
        self.url = url

    def __call__(self, cls):
        self.routes.append(Url(self.url, cls))


class Debug:
    """ Декоратор @debug - выводит в терминал название функции и время ее выполнения """

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            """ Декоратор класса оборачивает в timeit каждый метод декорируемого класса """

            def timed(*args, **kw):
                time_ = time()
                result = method(*args, **kw)
                time_ = time() - time_
                print(f'Debug --> {self.name} выполнялся {time_:2.2f} ms')
                return result

            return timed

        return timeit(cls)
