from password_strength import PasswordPolicy

from .email_service import EmailService
from ..interfaces.istorage_service import IStorageService
from ..utils import Config
from ..domain import AuthUser, AuthException, Admin, User
from ..interfaces.iuser_repository import IUserRepository


class AuthService(object):
    """
    Represents an authentication service.
    Supports login, register, changing and recovering password, blocking and unblocking of users.
    """

    def __init__(self, repo: IUserRepository, storage_service: IStorageService):
        self.__users = {}
        self.__user_repo: IUserRepository = repo
        self.__storage_service = storage_service
        self.__policy = PasswordPolicy.from_names(
            length=8, uppercase=1, numbers=1, special=1
        )

        self.__email_service = EmailService(
            smtp_server=Config.SMTP_SERVER,
            smtp_port=Config.SMTP_PORT,
            sender_email=Config.SENDER_EMAIL,
            sender_password=Config.SENDER_PASSWORD,
        )

    def register_user(self, email: str, password: str) -> AuthUser:
        """
        Register a new user.

        :param email: Email with existing domain and valid format.
        :param password: Password longer than 8 characters. Contains one uppercase, number, and special character.
        :return: AuthUser object.
        :raise AuthException:
            If user already exists.
            If password isn't correct.
        """

        if self.__user_repo.get_by_email(email):
            raise AuthException("User already exists")

        if self.__policy.test(password):
            raise AuthException("Password is weak")

        user = AuthUser(email, password)
        self.__user_repo.add(user)

        self.__storage_service.create_storage(user.id)

        return user

    def block_user(self, initiator: User, target_email: str) -> None:
        """
        Block user. Can be unblocked. Use unblock_user().

        :param initiator: Initiator of blocking. Only admin can block.
        :param target_email: Email of target user.
        :raise PermissionError: If initiator doesn't have permission to block.
        :raise AuthException: If user not found.
        """

        if not isinstance(initiator, Admin):
            raise PermissionError("Only admins can block users")

        user = self.__user_repo.get_by_email(target_email)
        if user is None:
            raise AuthException("User not found")

        user.is_blocked = True

    def unblock_user(self, initiator: User, target_email: str):
        """
        Unblock user. Can be blocked again. Use block_user().

        :param initiator: Initiator of unblocking. Only admin can unblock.
        :param target_email: Email of target user.
        :raise PermissionError: If initiator doesn't have permission to unblock.
        :raise AuthException: If user not found.
        """

        if not isinstance(initiator, Admin):
            raise PermissionError("Only admins can unblock users")

        user = self.__user_repo.get_by_email(target_email)
        if user is None:
            raise AuthException("User not found")
        user.is_blocked = False

    def delete_user(self, initiator: User, target_email: str):
        """
        Delete user. Can not be restored. Use careful.

        :param initiator: Initiator of deleting. Only admin can delete.
        :param target_email: Email of target user.
        :raise PermissionError: If initiator doesn't have permission to delete.
        :raise AuthException: If user not found.
        """

        if not isinstance(initiator, Admin):
            raise PermissionError("Only admins can delete users")

        user = self.__user_repo.get_by_email(target_email)
        if user is None:
            raise AuthException("User not found")
        self.__user_repo.delete(user)

    def create_admin(self, email: str, password: str) -> Admin:
        """
        Create new admin user.

        :param email: Email with existing domain and valid format.
        :param password: Password longer than 8 characters. Contains one uppercase, number, and special character.
        :return: Admin object.
        :raise AuthException:
            If user already exists.
            If password isn't correct.
        """

        if self.__user_repo.get_by_email(email):
            raise AuthException("User already exists")

        if self.__policy.test(password):
            raise AuthException("Password is weak")

        user = Admin(email, password)
        self.__user_repo.add(user)
        self.__storage_service.create_storage(user.id)

        return user

    def login(self, email: str, password: str) -> User:
        """
        Login with email and password.

        :param email: Email of any format.
        :param password: Password of any format.
        :return: User object if login was successful.
        :raise AuthException:
            If user not found.
            If password isn't correct.
            If user is blocked.
        """

        user = self.__user_repo.get_by_email(email)
        if not user or not user.verify_password(password):
            raise AuthException("Invalid credentials")

        if user.is_blocked:
            raise AuthException("User is blocked")
        return user

    def change_password(
        self, email: str, current_password: str, new_password: str
    ) -> None:
        """
        Change password of user.

        :param email: Email of any format.
        :param current_password: Password of current user.
        :param new_password: New password of current user.
        :raise AuthException:
            If user not found.
            If password is weak (less than 8 characters, doesn't contain uppercase, number, special character).
        """

        user = self.__user_repo.get_by_email(email)
        if not user:
            raise AuthException("User not found")

        errors = self.__policy.test(new_password)
        if errors:
            raise AuthException(f"Password is weak: {errors}")

        user.change_password(current_password, new_password)
        self.__user_repo.update(user)

    def recover_password(self, email: str) -> None:
        """
        Recover password for user within email.

        Send message to given email with temporary password.
        :param email: Email of any format.
        :raise AuthException:
            If user not found.
        """
        user = self.__user_repo.get_by_email(email)
        if not user:
            raise AuthException("User not found")

        self.__email_service.send_recovery_email(
            user.email, user.generate_temp_password()
        )
        self.__user_repo.update(user)
