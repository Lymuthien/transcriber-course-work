from copy import copy

from .local_file_manager import LocalFileManager
from ..interfaces.istorage_repository import IStorageRepository
from ...domain import Storage


class InMemoryStorageRepository(IStorageRepository):
    def __init__(self, data_dir: str):
        self.__storages: dict[str, Storage] = {}
        self.__user_storage_map: dict[str, str] = {}  # user_id -> storage_id
        self.__dir = data_dir
        try:
            self.__storages, self.__user_storage_map = LocalFileManager.load(data_dir)
        except:
            pass

    def get_by_id(self, storage_id: str) -> Storage | None:
        return copy(self.__storages.get(storage_id))

    def get_by_user(self, user_id: str) -> Storage | None:
        storage_id = self.__user_storage_map.get(user_id)
        return self.__storages.get(storage_id) if storage_id else None

    def add(self, storage: Storage) -> None:
        if storage.id in self.__storages:
            raise ValueError('Storage already exists')

        self.__storages[storage.id] = storage
        self.__user_storage_map[storage.user_id] = storage.id
        LocalFileManager.save((self.__storages, self.__user_storage_map), self.__dir)

    def update(self, storage: Storage) -> None:
        if storage.id not in self.__storages:
            raise ValueError('Storage not found')
        self.__storages[storage.id] = storage
        LocalFileManager.save((self.__storages, self.__user_storage_map), self.__dir)

    def get_all_records(self, storage_id: str) -> list[str]:
        storage = self.get_by_id(storage_id)
        return storage.audio_record_ids if storage else []
