from password_strength import PasswordPolicy

from ..domain import AuthUser, AuthException, Admin, User
from ..repositories import IUserRepository
from .storage_service import StorageService
from .email_service import EmailService


class AuthService:
    def __init__(self, repo: IUserRepository, storage_service: StorageService):
        self.__users = {}
        self.__user_repo: IUserRepository = repo
        self.__storage_service = storage_service
        self.__policy = PasswordPolicy.from_names(length=8, uppercase=1, numbers=1, special=1)

    def register_user(self, email: str, password: str) -> AuthUser:
        if self.__user_repo.get_by_email(email):
            raise AuthException('User already exists')

        if self.__policy.test(password):
            raise AuthException('Password is weak')

        user = AuthUser(email, password)
        self.__user_repo.add(user)

        self.__storage_service.create_storage(user.id)

        return user

    def block_user(self, initiator: User, target_email: str):
        if not isinstance(initiator, Admin):
            raise PermissionError('Only admins can block users')

        user = self.__user_repo.get_by_email(target_email)
        if user is None:
            raise AuthException('User not found')

        user.is_blocked = True

    def unblock_user(self, initiator: User, target_email: str):
        if not isinstance(initiator, Admin):
            raise PermissionError('Only admins can unblock users')

        user = self.__user_repo.get_by_email(target_email)
        if user is None:
            raise AuthException('User not found')
        user.is_blocked = False

    def delete_user(self, initiator: User, target_email: str):
        if not isinstance(initiator, Admin):
            raise PermissionError('Only admins can delete users')

        user = self.__user_repo.get_by_email(target_email)
        if user is None:
            raise AuthException('User not found')
        self.__user_repo.delete(user)

    def create_admin(self, email: str, password: str) -> Admin:
        if self.__user_repo.get_by_email(email):
            raise AuthException('User already exists')

        user = Admin(email, password)
        self.__user_repo.add(user)
        return user

    def login(self, email: str, password: str) -> User | None:
        user = self.__user_repo.get_by_email(email)
        if not user or not user.verify_password(password):
            raise AuthException('Invalid credentials')

        if user.is_blocked:
            raise AuthException('User is blocked')
        return user

    def change_password(self, email: str, current_password: str, new_password: str) -> None:
        user = self.__user_repo.get_by_email(email)
        if not user:
            raise AuthException('User not found')

        errors = self.__policy.test(new_password)
        if errors:
            raise AuthException(f'Password is weak: {errors}')

        user.change_password(current_password, new_password)
        self.__user_repo.update(user)

    def recover_password(self, email: str) -> None:
        user = self.__user_repo.get_by_email(email)
        if not user:
            raise AuthException('User not found')

        EmailService().send_recovery_email(user.email, user.generate_temp_password())
