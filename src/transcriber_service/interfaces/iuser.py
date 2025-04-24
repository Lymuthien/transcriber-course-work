from abc import abstractmethod
from datetime import datetime

from .irestorable import IRestorable


class IUser(IRestorable):
    @property
    @abstractmethod
    def is_blocked(self) -> bool:
        """Returns True if the user is blocked else False."""
        pass

    @is_blocked.setter
    @abstractmethod
    def is_blocked(self, is_blocked: bool):
        """Sets the blocked state of the user."""
        pass

    @property
    @abstractmethod
    def password_hash(self) -> str:
        pass

    @property
    @abstractmethod
    def temp_password_hash(self) -> str | None:
        pass

    @property
    @abstractmethod
    def id(self) -> str:
        """Returns user ID."""
        pass

    @property
    @abstractmethod
    def email(self) -> str:
        """Returns user email."""
        pass

    @property
    @abstractmethod
    def registration_date(self) -> datetime:
        """Returns user registration date."""
        pass

    @property
    @abstractmethod
    def last_updated(self) -> datetime:
        """Returns user last updated date."""
        pass

    @abstractmethod
    def verify_password(self, password: str) -> bool:
        """
        Verify if provided password matches stored hash.

        :param password: Plain-text password to be verified.
        :return: True if password matches stored hash, False otherwise.
        """
        pass

    @abstractmethod
    def change_password(self, current_password: str, new_password: str) -> None:
        pass

    @abstractmethod
    def generate_temp_password(self) -> str:
        pass
