from ..domain import AuthUser, Admin
from ..domain import AuthException

class AuthService:
    def __init__(self):
        self.__users = {}

    def register(self, email: str, password: str) -> AuthUser:
        if email in self.__users:
            raise AuthException("User already exists")
        user = AuthUser(email, password)
        self.__users[email] = user
        return user

    def login(self, email: str, password: str) -> AuthUser:
        user = self.__users.get(email)
        if not user or not user.verify_password(password):
            raise AuthException("Invalid credentials")
        return user