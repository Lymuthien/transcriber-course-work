from ..domain import AuthUser, AuthException, Admin, User
from ..repositories import IUserRepository
from .storage_service import StorageService


class AuthService:
    def __init__(self, repo: IUserRepository, storage_service: StorageService):
        self.__users = {}
        self.__user_repo = repo
        self.__storage_service = storage_service

    def register_user(self, email: str, password: str) -> AuthUser:
        if self.__user_repo.get_by_email(email):
            raise AuthException("User already exists")

        user = AuthUser(email, password)
        self.__user_repo.add(user)

        self.__storage_service.create_storage(user.id)

        return user

    def create_admin(self, email: str, password: str) -> Admin:
        if self.__user_repo.get_by_email(email):
            raise AuthException("User already exists")
        user = Admin(email, password)
        self.__user_repo.add(user)
        return user

    def login(self, email: str, password: str) -> User | None:
        user = self.__user_repo.get_by_email(email)
        if not user or not user.verify_password(password):
            raise AuthException("Invalid credentials")
        return user