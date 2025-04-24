from abc import ABC, abstractmethod
from ..domain import AuthUser, Admin
from ..interfaces.iuser import IUser


class UserFactory(ABC):
    """Abstract base class for user factories."""

    @abstractmethod
    def create_user(self, email: str, password: str) -> IUser:
        """Create a user with the given email and password."""
        pass


class AuthUserFactory(UserFactory):
    """Factory for creating AuthUser instances."""

    def create_user(self, email: str, password: str) -> IUser:
        return AuthUser(email, password)


class AdminFactory(UserFactory):
    """Factory for creating Admin instances."""

    def create_user(self, email: str, password: str) -> IUser:
        return Admin(email, password)
