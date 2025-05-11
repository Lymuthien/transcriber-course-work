from abc import abstractmethod
from datetime import datetime

from transcriber_service.domain.interfaces.entities.irestorable import IRestorable


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

    @password_hash.setter
    @abstractmethod
    def password_hash(self, password_hash: str):
        pass

    @property
    @abstractmethod
    def temp_password_hash(self) -> str | None:
        pass

    @temp_password_hash.setter
    @abstractmethod
    def temp_password_hash(self, temp_password_hash: str):
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
    def can_block(self) -> bool:
        pass
