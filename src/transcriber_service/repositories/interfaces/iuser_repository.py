from abc import ABC, abstractmethod
from ...domain.user import User


class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> User | None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def add(self, user: User) -> None: ...

    @abstractmethod
    def update(self, user: User) -> None: ...

    @abstractmethod
    def delete(self, user: User): ...
