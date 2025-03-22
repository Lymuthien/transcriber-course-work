from abc import ABC, abstractmethod
from ...domain.audio import AudioRecord


class IAudioRepository(ABC):
    @abstractmethod
    def get_by_storage(self, storage_id: str) -> tuple[AudioRecord, ...]: ...

    @abstractmethod
    def get_by_id(self, record_id: str) -> AudioRecord | None: ...

    @abstractmethod
    def search_by_tags(self, storage_id: str, tags: list[str], match_all: bool = False) -> tuple[AudioRecord, ...]: ...

    @abstractmethod
    def search_by_name(self, storage_id: str, name: str) -> tuple[AudioRecord, ...]: ...

    @abstractmethod
    def add(self, record: AudioRecord) -> None: ...

    @abstractmethod
    def update(self, record: AudioRecord) -> None: ...

    @abstractmethod
    def delete(self, record_id: str) -> None: ...
