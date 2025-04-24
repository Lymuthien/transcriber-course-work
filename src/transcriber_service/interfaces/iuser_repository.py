from abc import ABC, abstractmethod
from ..interfaces.iuser import IUser


class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> IUser | None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> IUser | None: ...

    @abstractmethod
    def add(self, user: IUser) -> None: ...

    @abstractmethod
    def update(self, user: IUser) -> None: ...

    @abstractmethod
    def delete(self, user: IUser): ...
