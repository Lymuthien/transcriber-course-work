from abc import ABC, abstractmethod

from ..interfaces import IStorage
from transcriber_service.domain.entities.storage import Storage


class IStorageFactory(ABC):

    @abstractmethod
    def create_storage(self, user_id: str) -> IStorage:
        pass


class StorageFactory(IStorageFactory):

    def create_storage(self, user_id: str) -> IStorage:
        return Storage(user_id)
