from abc import ABC, abstractmethod
from typing import Optional, List
from ...domain import Storage


class IStorageRepository(ABC):
    @abstractmethod
    def get_by_id(self, storage_id: str) -> Optional[Storage]: ...

    @abstractmethod
    def get_by_user(self, user_id: str) -> Optional[Storage]: ...

    @abstractmethod
    def add(self, storage: Storage) -> None: ...

    @abstractmethod
    def update(self, storage: Storage) -> None: ...

    @abstractmethod
    def get_all_records(self, storage_id: str) -> List[str]: ...