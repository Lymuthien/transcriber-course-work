from abc import ABC, abstractmethod

from ..interfaces import IUser
from ..user import AuthUser, Admin


class IUserFactory(ABC):
    """Abstract base class for user factories."""

    @abstractmethod
    def create_user(self, email: str, password_hash: str) -> IUser:
        """Create a user with the given email and password hash."""
        pass

    @abstractmethod
    def create_object(self) -> IUser:
        pass


class AuthUserFactory(IUserFactory):
    """Factory for creating AuthUser instances."""

    def create_user(self, email: str, password_hash: str) -> IUser:
        return AuthUser(email, password_hash)

    def create_object(self) -> IUser:
        return AuthUser.__new__(AuthUser)


class AdminFactory(IUserFactory):
    """Factory for creating Admin instances."""

    def create_user(self, email: str, password_hash: str) -> IUser:
        return Admin(email, password_hash)

    def create_object(self) -> IUser:
        return Admin.__new__(Admin)
