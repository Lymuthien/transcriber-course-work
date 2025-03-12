from copy import copy
from typing import Dict, Optional, List
from ..interfaces.istorage_repository import IStorageRepository
from ...domain import Storage


class InMemoryStorageRepository(IStorageRepository):
    def __init__(self):
        self.__storages: Dict[str, Storage] = {}
        self.__user_storage_map: Dict[str, str] = {}  # user_id -> storage_id

    def get_by_id(self, storage_id: str) -> Optional[Storage]:
        return copy(self.__storages.get(storage_id))

    def get_by_user(self, user_id: str) -> Optional[Storage]:
        storage_id = self.__user_storage_map.get(user_id)
        return self.__storages.get(storage_id) if storage_id else None

    def add(self, storage: Storage) -> None:
        if storage.id in self.__storages:
            raise ValueError('Storage already exists')

        self.__storages[storage.id] = storage
        self.__user_storage_map[storage.user_id] = storage.id

    def update(self, storage: Storage) -> None:
        if storage.id not in self.__storages:
            raise ValueError('Storage not found')
        self.__storages[storage.id] = storage

    def get_all_records(self, storage_id: str) -> List[str]:
        storage = self.get_by_id(storage_id)
        return storage.audio_record_ids if storage else []