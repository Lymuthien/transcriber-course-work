from transcriber_service.domain.factories import IStorageFactory, StorageFactory
from transcriber_service.domain.interfaces import IStorage, IStorageRepository
from transcriber_service.interfaces import IStorageService


class StorageService(IStorageService):
    """Manages storage creation and retrieval."""

    def __init__(self, storage_repo: IStorageRepository):
        self.__storage_repository = storage_repo
        self.__storage_factory: IStorageFactory = StorageFactory()

    def create_storage(self, user_id: str) -> IStorage:
        """Creates a new storage container for a user."""

        storage = self.__storage_factory.create_storage(user_id)
        self.__storage_repository.add(storage)
        return storage

    def get_user_storage(self, user_id: str) -> IStorage | None:
        """Returns storage by user id if it exists else None."""

        return self.__storage_repository.get_by_user(user_id)
