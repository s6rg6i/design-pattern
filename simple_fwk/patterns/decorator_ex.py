from dataclasses import dataclass


class BaseViewTest:
    def get(self):
        ...


@dataclass
class UrlTest:
    url: str
    view: BaseViewTest


class AppRouteTest:
    """ Структурный паттерн - Декоратор - добавляет url-ы, как во Flask """
    routes = []

    def __init__(self, url):
        print(f"__init__: {url=}")
        self.url = url

    def __call__(self, cls):
        print(f"__call__: {cls=}")
        self.routes.append(UrlTest(self.url, cls))


@AppRouteTest(url="/v1")
class View1(BaseViewTest):
    def get(self):
        print("View1.get()")


@AppRouteTest(url="/v2")
class View2(BaseViewTest):
    def get(self):
        print("View2.get()")


@AppRouteTest(url="/v3")
class View3(BaseViewTest):
    def get(self):
        print("View3.get()")


if __name__ == "__main__":
    print("start:")
    print(AppRouteTest.routes)
    zzz = AppRouteTest.routes[0]
    zzz.view().get()
    AppRouteTest.routes[1].view().get()
    AppRouteTest.routes[2].view().get()
