from flask_login    import UserMixin, login_user, logout_user, current_user


class UserAuth(UserMixin):
    lm = None
    bc = None

    def __init__(self, user_id):
        self.id = user_id

    def Login(self) ->None:
        login_user(self)

    @staticmethod
    def Logout() -> None:
        logout_user()

    @staticmethod
    def GetCurUserId():
        return current_user.id

    @staticmethod
    def CheckPassword(password: str, hash: str) -> bool:
        return UserAuth.bc.check_password_hash(hash, password)

    @staticmethod
    def HashPassword(password: str) -> str:
        return UserAuth.bc.generate_password_hash(password)

    @staticmethod
    def ChangePassword(email: str) -> str:
        pass

