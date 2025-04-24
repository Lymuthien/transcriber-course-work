from abc import ABC, abstractmethod

from ..domain import Storage
from ..interfaces import IStorage


class IStorageFactory(ABC):

    @abstractmethod
    def create_storage(self, user_id: str) -> IStorage:
        pass

    @abstractmethod
    def create_object(self) -> IStorage:
        pass


class StorageFactory(IStorageFactory):

    def create_storage(self, user_id: str) -> IStorage:
        return Storage(user_id)

    def create_object(self) -> IStorage:
        return Storage.__new__(Storage)
