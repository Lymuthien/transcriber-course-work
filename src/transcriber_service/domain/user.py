from datetime import datetime
from typing import Any
from uuid import uuid4

from .exceptions import AuthException
from .password_manager import PasswordManager
from ..interfaces import IUser


class User(IUser):
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

        self._email: str = email
        self._id: str = uuid4().hex
        self._password_hash: str = PasswordManager.hash_password(password)
        self._temp_password_hash: str | None = None
        self._registration_date: datetime = datetime.now()
        self._last_updated: datetime = self._registration_date
        self._is_blocked: bool = False

    @property
    def is_blocked(self) -> bool:
        """Returns True if the user is blocked else False."""

        return self._is_blocked

    @is_blocked.setter
    def is_blocked(self, is_blocked: bool):
        """Sets the blocked state of the user."""

        self._is_blocked = is_blocked
        self._last_updated = datetime.now()

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @property
    def temp_password_hash(self) -> str | None:
        return self._temp_password_hash

    @property
    def id(self) -> str:
        """Returns user ID."""

        return self._id

    @property
    def email(self) -> str:
        """Returns user email."""

        return self._email

    @property
    def registration_date(self) -> datetime:
        """Returns user registration date."""

        return self._registration_date

    @property
    def last_updated(self) -> datetime:
        """Returns user last updated date."""

        return self._last_updated

    def verify_password(self, password: str) -> bool:
        """
        Verify if provided password matches stored hash.

        :param password: Plain-text password to be verified.
        :return: True if password matches stored hash, False otherwise.
        """
        if PasswordManager.verify_password(self._temp_password_hash, password):
            self._password_hash = self._temp_password_hash
            self._temp_password_hash = None

        return PasswordManager.verify_password(self._password_hash, password)

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

        self._password_hash = PasswordManager.hash_password(new_password)
        self._last_updated = datetime.now()

    def generate_temp_password(self) -> str:
        """
        Generate temporary password.

        When creating a new once the old one will be invalid.
        :return: Not hashed temporary password.
        """
        temp_password = PasswordManager.create_password()
        self._temp_password_hash = PasswordManager.hash_password(temp_password)

        return temp_password

    def restore_state(self, data: dict[str, Any]):
        self._id = data["id"]
        self._email = data["email"]
        self._registration_date = datetime.fromisoformat(data["registration_date"])
        self._last_updated = datetime.fromisoformat(data["last_updated"])
        self._is_blocked = data["is_blocked"]
        self._password_hash = data["password_hash"]
        self._temp_password_hash = data["temp_password_hash"]


class AuthUser(User):
    """
    Represents an authenticated user with basic privileges.

    Inherits from User class and sets default role to 'user'.
    Should be used for all registered non-admin users.
    """

    def __init__(self, email: str, password: str):
        super().__init__(email, password)


class Admin(AuthUser):
    """
    Represents an administrator user with elevated privileges.

    Inherits from AuthUser and sets default role to 'admin'.
    Should be instantiated only through proper admin creation process.
    """

    def __init__(self, email: str, password: str):
        super().__init__(email, password)
