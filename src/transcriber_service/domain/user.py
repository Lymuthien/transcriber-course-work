from datetime import datetime
from uuid import uuid4

from email_validator import validate_email

from .exceptions import AuthException
from .password_manager import PasswordManager


class User(object):
    """
    Represents a base user in the system.

    Handles core user properties validation and initialization.
    Should not be instantiated directly - use AuthUser or Admin subclasses.
    """

    def __init__(self, email: str, password: str):
        """
        Create User instance with validated credentials.

        :param email: User's email address.
        :param password: Plain-text password to be hashed.
        :raises: If email is not valid.
        """

        self.__email: str = validate_email(email).normalized
        self.__id: str = uuid4().hex
        self.__password_hash: str = PasswordManager.hash_password(password)
        self.__temp_password_hash: str | None = None
        self.__registration_date: datetime = datetime.now()
        self.__last_updated: datetime = self.__registration_date
        self.__is_blocked: bool = False
        self._role = "guest"

    @property
    def is_blocked(self) -> bool:
        """Returns True if the user is blocked else False."""

        return self.__is_blocked

    @is_blocked.setter
    def is_blocked(self, is_blocked: bool):
        """Sets the blocked state of the user."""

        self.__is_blocked = is_blocked
        self.__last_updated = datetime.now()

    @property
    def id(self) -> str:
        """Returns user ID."""

        return self.__id

    @property
    def email(self) -> str:
        """Returns user email."""

        return self.__email

    @property
    def role(self) -> str:
        """Returns user role."""

        return self._role

    @property
    def registration_date(self) -> datetime:
        """Returns user registration date."""

        return self.__registration_date

    @property
    def last_updated(self) -> datetime:
        """Returns user last updated date."""

        return self.__last_updated

    def verify_password(self, password: str) -> bool:
        """
        Verify if provided password matches stored hash.

        :param password: Plain-text password to be verified.
        :return: True if password matches stored hash, False otherwise.
        """
        if PasswordManager.verify_password(self.__temp_password_hash, password):
            self.__password_hash = self.__temp_password_hash
            self.__temp_password_hash = None

        return PasswordManager.verify_password(self.__password_hash, password)

    def change_password(self, current_password: str, new_password: str) -> None:
        """
        Change user password.

        :param current_password: Current user password.
        :param new_password: New password.
        :return: None
        :raise AuthException: if current password does not match.
        """
        if not self.verify_password(current_password):
            raise AuthException("Invalid current password")

        self.__password_hash = PasswordManager.hash_password(new_password)
        self.__last_updated = datetime.now()

    def generate_temp_password(self) -> str:
        """
        Generate temporary password.

        When creating a new once the old one will be invalid.
        :return: Not hashed temporary password.
        """
        temp_password = PasswordManager.create_password()
        self.__temp_password_hash = PasswordManager.hash_password(temp_password)

        return temp_password


class AuthUser(User):
    """
    Represents an authenticated user with basic privileges.

    Inherits from User class and sets default role to 'user'.
    Should be used for all registered non-admin users.
    """

    def __init__(self, email: str, password: str):
        super().__init__(email, password)
        self._role = "user"


class Admin(AuthUser):
    """
    Represents an administrator user with elevated privileges.

    Inherits from AuthUser and sets default role to 'admin'.
    Should be instantiated only through proper admin creation process.
    """

    def __init__(self, email: str, password: str):
        super().__init__(email, password)
        self._role = "admin"
