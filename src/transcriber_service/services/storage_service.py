from typing import List

from ..domain import Storage


class StorageService:
    """Manages storage creation and retrieval."""

    def __init__(self):
        self.__storages = []

    def create_storage(self,
                       user_id: str) -> Storage:
        """Creates a new storage container for a user."""

        storage = Storage(user_id)
        self.__storages.append(storage)
        return storage

    @property
    def storages(self) -> List[Storage]:
        return self.__storages.copy()

    def get_storage(self,
                    user_id: str) -> Storage | None:
        for storage in self.__storages:
            if storage.user_id == user_id:
                return storage
