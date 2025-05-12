from password_strength import PasswordPolicy

from transcriber_service.application.services.user_service import UserService
from transcriber_service.domain import AuthException
from transcriber_service.domain.interfaces import IUser, IEmailService


class AuthService(object):
    """
    Represents an authentication services.
    Supports login, register, changing and recovering password, blocking and unblocking of users.
    """

    def __init__(
        self,
        user_service: UserService,
        email_service: IEmailService,
    ):
        self._user_service = user_service
        self._password_hasher = user_service.password_hasher
        self.__policy = PasswordPolicy.from_names(
            length=8, uppercase=1, numbers=1, special=1
        )

        self.__email_service = email_service

    def register_user(self, email: str, password: str) -> IUser:
        """
        Register a new user.

        :param email: Email with existing domain and valid format.
        :param password: Password longer than 8 characters. Contains one uppercase, number, and special character.
        :return: AuthUser object.
        :raise Exception:
            If user already exists.
            If password isn't correct.
        """
        return self._user_service.create_user(email, password)

    def create_admin(self, email: str, password: str) -> IUser:
        """
        Create new admin user.

        :param email: Email with existing domain and valid format.
        :param password: Password longer than 8 characters. Contains one uppercase, number, and special character.
        :return: Admin object.
        :raise Exception:
            If user already exists.
            If password isn't correct.
        """

        return self._user_service.create_admin(email, password)

    def login(self, email: str, password: str) -> IUser:
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
        if not user or not self._password_hasher.verify_password(
            user.password_hash, password
        ):
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

        user = self._user_service.get_user_by_email(email)
        if not user:
            raise AuthException("User not found")

        errors = self.__policy.test(new_password)
        if errors:
            raise AuthException(f"Password is weak: {errors}")
        if not self._password_hasher.verify_password(
            user.password_hash, current_password
        ):
            raise AuthException("Incorrect password")

        user.password_hash = new_password
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

        temp_password = self._password_hasher.create_password()
        temp_password_hash = self._password_hasher.hash_password(temp_password)
        user.temp_password_hash = temp_password_hash

        self.__email_service.send_recovery_email(user.email, temp_password)
        self._user_service.update_user(user)
