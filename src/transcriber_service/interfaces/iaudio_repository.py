from abc import ABC, abstractmethod
from ..interfaces.iaudio_record import IAudioRecord


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
