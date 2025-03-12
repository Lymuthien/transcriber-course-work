from abc import ABC, abstractmethod
from typing import Optional

from ...domain.audio import AudioRecord


class IAudioRepository(ABC):
    @abstractmethod
    def get_by_storage(self, storage_id: str) -> tuple[AudioRecord, ...]: ...

    @abstractmethod
    def get_by_id(self, record_id: str) -> Optional[AudioRecord]: ...

    @abstractmethod
    def search_by_tags(self, storage_id: str, tags: list[str], match_all: bool = False) -> tuple[AudioRecord, ...]: ...

    @abstractmethod
    def add(self, record: AudioRecord) -> None: ...

    @abstractmethod
    def update(self, record: AudioRecord) -> None: ...

    @abstractmethod
    def delete(self, record_id: str) -> None: ...
