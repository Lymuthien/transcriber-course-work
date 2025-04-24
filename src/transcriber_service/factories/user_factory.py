from abc import ABC, abstractmethod
from ..domain import AuthUser, Admin
from ..interfaces import IUser


class IUserFactory(ABC):
    """Abstract base class for user factories."""

    @abstractmethod
    def create_user(self, email: str, password: str) -> IUser:
        """Create a user with the given email and password."""
        pass

    @abstractmethod
    def create_object(self) -> IUser:
        pass


class AuthUserFactory(IUserFactory):
    """Factory for creating AuthUser instances."""

    def create_user(self, email: str, password: str) -> IUser:
        return AuthUser(email, password)

    def create_object(self) -> IUser:
        return AuthUser.__new__(AuthUser)


class AdminFactory(IUserFactory):
    """Factory for creating Admin instances."""

    def create_user(self, email: str, password: str) -> IUser:
        return Admin(email, password)

    def create_object(self) -> IUser:
        return Admin.__new__(Admin)
