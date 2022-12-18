from __future__ import annotations
from dataclasses import dataclass
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from fwk.view import BaseView


@dataclass
class Url:
    url: str
    view: Type[BaseView]
