from datetime import datetime
from uuid import uuid4
import hashlib
from email_validator import validate_email
from .exceptions import InvalidEmailException


class User(object):
    """
    Represents a base user in the system.

    Handles core user properties validation and initialization.
    Should not be instantiated directly - use AuthUser or Admin subclasses.
    """

    def __init__(self,
                 email: str,
                 password: str):
        """
        Create User instance with validated credentials.

        :param email: User's email address.
        :param password: Plain-text password to be hashed.
        :raises InvalidEmailException: If email is not valid.
        """
        self.__email = self.__validated_normalized_email(email)
        self.__id = uuid4().hex
        self.__password_hash = self.__hash_password(password)
        self.__registration_date = datetime.now()
        self.__last_updated = self.__registration_date
        self._role = "guest"

    @staticmethod
    def __hash_password(password: str) -> str:
        """Generate secure hash from plain text password."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def __validated_normalized_email(email: str) -> str:
        """Validate email format and return normalized version."""
        try:
            return validate_email(email).normalized
        except Exception as e:
            raise InvalidEmailException(str(e))

    @property
    def id(self) -> str:
        return self.__id

    @property
    def email(self) -> str:
        return self.__email

    @property
    def role(self) -> str:
        return self._role

    @property
    def registration_date(self) -> datetime:
        return self.__registration_date

    @property
    def last_updated(self) -> datetime:
        return self.__last_updated

    def verify_password(self,
                        password: str) -> bool:
        """
        Verify if provided password matches stored hash.

        :param password: Plain-text password to be verified.
        :return: True if password matches stored hash, False otherwise.
        """
        return self.__password_hash == self.__hash_password(password)

    def change_password(self,
                        current_password: str,
                        new_password: str) -> bool:
        if self.verify_password(current_password):
            self.__password_hash = self.__hash_password(new_password)
            return True
        else:
            return False


class AuthUser(User):
    """
    Represents an authenticated user with basic privileges.

    Inherits from User class and sets default role to 'user'.
    Should be used for all registered non-admin users.
    """

    def __init__(self,
                 email: str,
                 password: str):
        super().__init__(email, password)
        self._role = "user"


class Admin(AuthUser):
    """
    Represents an administrator user with elevated privileges.

    Inherits from AuthUser and sets default role to 'admin'.
    Should be instantiated only through proper admin creation process.
    """

    def __init__(self,
                 email: str,
                 password: str):
        super().__init__(email, password)
        self._role = "admin"
