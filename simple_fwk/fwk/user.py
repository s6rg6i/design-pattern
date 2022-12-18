
class User:
    def __init__(self, username: str, password: str = '', session_id: str = None):
        self.name = username
        self.password = password
        self.session_id = session_id

    @staticmethod
    def get_user_by_session(session_id: str, all_users: list['User']) -> str:  # Forward references
        for user in all_users:
            if user.session_id == session_id:
                return user.name
        return ''

    @staticmethod
    def get_session_by_user(user_name: str, all_users: list['User']) -> str:  # Forward references
        for user in all_users:
            if user.name == user_name:
                return user.session_id
        return ''

    @staticmethod
    def set_session_for_user(user_name: str, session_id: str, all_users: list['User']):
        for user in all_users:
            if user.name == user_name:
                user.session_id = session_id
                return

    @staticmethod
    def user_exists(user_name: str, all_users: list['User']) -> bool:
        for user in all_users:
            if user.name == user_name:
                return True
        return False


users: list[User] = [User('admin1', '1'), User('admin2', '2'), User('admin3', '3'), ]
