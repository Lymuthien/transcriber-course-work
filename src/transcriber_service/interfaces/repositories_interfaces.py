from abc import ABC, abstractmethod
from .domain_interfaces import IAudioRecord, IStorage, IUser



class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> IUser | None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> IUser | None: ...

    @abstractmethod
    def add(self, user: IUser) -> None: ...

    @abstractmethod
    def update(self, user: IUser) -> None: ...

    @abstractmethod
    def delete(self, user: IUser): ...


class IStorageRepository(ABC):
    @abstractmethod
    def get_by_id(self, storage_id: str) -> IStorage | None: ...

    @abstractmethod
    def get_by_user(self, user_id: str) -> IStorage | None: ...

    @abstractmethod
    def add(self, storage: IStorage) -> None: ...

    @abstractmethod
    def update(self, storage: IStorage) -> None: ...

    @abstractmethod
    def get_all_records(self, storage_id: str) -> list[str]: ...


class IAudioRepository(ABC):
    @abstractmethod
    def get_by_storage(self, storage_id: str) -> tuple[IAudioRecord, ...]: ...

    @abstractmethod
    def get_by_id(self, record_id: str) -> IAudioRecord | None: ...

    @abstractmethod
    def search_by_tags(
        self, storage_id: str, tags: list[str], match_all: bool = False
    ) -> tuple[IAudioRecord, ...]: ...

    @abstractmethod
    def search_by_name(
        self, storage_id: str, name: str
    ) -> tuple[IAudioRecord, ...]: ...

    @abstractmethod
    def add(self, record: IAudioRecord) -> None: ...

    @abstractmethod
    def update(self, record: IAudioRecord) -> None: ...

    @abstractmethod
    def delete(self, record_id: str) -> None: ...
