from abc import ABC, abstractmethod
from .domain_interfaces import IStorage


class IStorageService(ABC):
    @abstractmethod
    def create_storage(self, user_id: str) -> IStorage: ...

    @abstractmethod
    def get_user_storage(self, user_id: str) -> IStorage | None: ...
