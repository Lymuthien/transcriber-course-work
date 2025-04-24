from abc import abstractmethod
from .irestorable import IRestorable


class IStorage(IRestorable):
    @property
    @abstractmethod
    def id(self) -> str: ...

    @property
    @abstractmethod
    def user_id(self) -> str: ...

    @property
    @abstractmethod
    def audio_record_ids(self) -> list[str]: ...

    @abstractmethod
    def add_audio_record(self, record_id: str) -> None: ...

    @abstractmethod
    def remove_audio_record(self, record_id: str) -> None: ...
