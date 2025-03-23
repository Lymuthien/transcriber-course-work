from transcriber_service.domain import Storage
from abc import ABC, abstractmethod

class IStorageService(ABC):
    @abstractmethod
    def create_storage(self, user_id: str) -> Storage: ...

    @abstractmethod
    def get_user_storage(self, user_id: str) -> Storage | None: ...
