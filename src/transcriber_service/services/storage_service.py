from ..interfaces.istorage_repository import IStorageRepository
from ..interfaces.istorage_service import IStorageService
from ..domain import Storage


class StorageService(IStorageService):
    """Manages storage creation and retrieval."""

    def __init__(self, storage_repo: IStorageRepository):
        self.__storage_repository = storage_repo

    def create_storage(self, user_id: str) -> Storage:
        """Creates a new storage container for a user."""

        storage = Storage(user_id)
        self.__storage_repository.add(storage)
        return storage

    def get_user_storage(self, user_id: str) -> Storage | None:
        """Returns storage by user id if it exists else None."""

        return self.__storage_repository.get_by_user(user_id)
