from __future__ import annotations
from typing import TYPE_CHECKING, List
from uuid import uuid4

from fwk.user import User

if TYPE_CHECKING:
    from fwk.request import RequestData
    from fwk.response import ResponseData


class BaseMiddleware:

    def to_request(self, request: RequestData, users: List[User]):
        return

    def to_response(self, response: ResponseData, users: List[User]):
        return


class Session(BaseMiddleware):

    def to_request(self, request: RequestData, users: List[User]):
        """ По куки session_id определяем пользователя """
        session_id = request.COOKIE.get('session_id', [''])[0]
        if session_id:
            user_name = User.get_user_by_session(session_id, users)
            if user_name:
                request.extra['user_name'] = user_name

    def to_response(self, response: ResponseData, users: List[User]):
        """ Добавляем заголовок, устанавливающий cookie, если нет session_id """
        user_name = response.request.extra.get('login', '')
        if user_name:
            session_id = str(uuid4())  # создаем новый идентификатор сессии
            response.update_headers(("Set-Cookie", f"session_id={session_id}"))  # обновим заголовок: установим куки
            if User.user_exists(user_name, users):
                User.set_session_for_user(user_name, session_id, users)  # для пользователя устанавливаем session_id
            else:
                users.append(User(user_name, '', session_id))  # создаем пользователя


middlewares = [
    Session
]
