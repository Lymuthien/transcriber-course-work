from abc import ABC, abstractmethod
from typing import Optional
from ...domain.user import User


class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]: ...

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    def add(self, user: User) -> None: ...

    @abstractmethod
    def update(self, user: User) -> None: ...
