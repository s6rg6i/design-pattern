from __future__ import annotations
from dataclasses import dataclass
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from fwk.view import BaseView


@dataclass
class Url:
    url: str
    view: Type[BaseView]


class AppRoute:
    """ Структурный паттерн - Декоратор - добавляет url-ы в routes, как во Flask """

    routes = []

    def __init__(self, url):
        self.url = url

    def __call__(self, cls):
        self.routes.append(Url(self.url, cls))
