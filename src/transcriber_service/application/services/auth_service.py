from email_validator import validate_email
from password_strength import PasswordPolicy

from transcriber_service.application.serialization.dto import UserDTO
from transcriber_service.application.services.user_service import UserService
from transcriber_service.domain import AuthException
from transcriber_service.domain.factories import (
    AuthUserFactory,
    IUserFactory,
    AdminFactory,
)
from transcriber_service.domain.interfaces import IEmailService, IPasswordManager
import logging


logger = logging.getLogger(__name__)


class AuthService(object):
    """
    Represents an authentication services.
    Supports login, register, changing and recovering password, blocking and unblocking of users.
    """

    def __init__(
        self,
        user_service: UserService,
        email_service: IEmailService,
        password_hasher: IPasswordManager,
    ):
        self._user_service = user_service
        self._password_manager = password_hasher
        self._policy = PasswordPolicy.from_names(
            length=8, uppercase=1, numbers=1, special=1
        )

        self.__email_service = email_service

    def _register(self, email: str, password: str, factory: IUserFactory) -> UserDTO:
        if self._user_service.get_user_by_email(email):
            logger.error(f"User with email {email} already exists")
            raise ValueError("User already exists")

        errors = self._policy.test(password)
        if errors:
            logger.error(f"Error validating password: {errors}, {password}")
            raise AuthException(
                f"Password is weak: 8 symbols, 1 uppercase, number, special"
            )

        email = validate_email(email).normalized
        password_hash = self._password_manager.hash_password(password)
        user = self._user_service.create_user(email, password_hash, factory)

        return user

    def register_user(self, email: str, password: str) -> UserDTO:
        """
        Register a new user.

        :param email: Email with existing domain and valid format.
        :param password: Password longer than 8 characters. Contains one uppercase, number, and special character.
        :return: AuthUser object.
        :raise Exception:
            If user already exists.
            If password isn't correct.
        """

        return self._register(email, password, AuthUserFactory())

    def create_admin(self, email: str, password: str) -> UserDTO:
        """
        Create new admin user.

        :param email: Email with existing domain and valid format.
        :param password: Password longer than 8 characters. Contains one uppercase, number, and special character.
        :return: Admin object.
        :raise Exception:
            If user already exists.
            If password isn't correct.
        """

        return self._register(email, password, AdminFactory())

    def login(self, email: str, password: str) -> UserDTO:
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

        user = self._user_service.get_user_by_email(email)
        if not user or not password:
            logger.warning(f"User {email} not found or no password.")
            raise AuthException("Invalid credentials")
        if user.temp_password_hash and self._password_manager.verify_password(
            user.temp_password_hash, password
        ):
            logger.info(f"User {email} use temp password.")
            user.password_hash = user.temp_password_hash
            user.temp_password_hash = None
            self._user_service.update_user(user)
        if not self._password_manager.verify_password(user.password_hash, password):
            logger.warning(f"User {email} login unsuccessful.")
            raise AuthException("Invalid credentials")

        if user.is_blocked:
            raise AuthException("User is blocked")

        return self._user_service.mapper.to_dto(user)

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

        user = self._user_service.get_user_by_email(email)
        if not user:
            raise AuthException("User not found")

        errors = self._policy.test(new_password)
        if errors:
            raise AuthException(f"Password is weak: {errors}")
        if not self._password_manager.verify_password(
            user.password_hash, current_password
        ):
            raise AuthException("Incorrect password")

        user.password_hash = self._password_manager.hash_password(new_password)
        self._user_service.update_user(user)

    def recover_password(self, email: str) -> None:
        """
        Recover password for user within email.

        Send message to given email with temporary password.
        :param email: Email of any format.
        :raise AuthException:
            If user not found.
        """
        user = self._user_service.get_user_by_email(email)
        if not user:
            raise AuthException("User not found")

        temp_password = self._password_manager.create_password()
        temp_password_hash = self._password_manager.hash_password(temp_password)
        user.temp_password_hash = temp_password_hash

        self.__email_service.send_recovery_email(user.email, temp_password)
        self._user_service.update_user(user)
