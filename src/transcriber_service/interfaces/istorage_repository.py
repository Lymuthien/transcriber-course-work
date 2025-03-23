from abc import ABC, abstractmethod
from .istorage import IStorage


class IStorageRepository(ABC):
    @abstractmethod
    def get_by_id(self, storage_id: str) -> IStorage | None: ...

    @abstractmethod
    def get_by_user(self, user_id: str) -> IStorage | None: ...

    @abstractmethod
    def add(self, storage: IStorage) -> None: ...

    @abstractmethod
    def update(self, storage: IStorage) -> None: ...

    @abstractmethod
    def get_all_records(self, storage_id: str) -> list[str]: ...