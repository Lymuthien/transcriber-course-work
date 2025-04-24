from abc import abstractmethod
from datetime import datetime
from .irestorable import IRestorable


class IAudioRecord(IRestorable):
    @property
    @abstractmethod
    def id(self) -> str: ...

    @property
    @abstractmethod
    def text(self) -> str: ...

    @text.setter
    @abstractmethod
    def text(self, value: str) -> None: ...

    @property
    @abstractmethod
    def language(self) -> str: ...

    @property
    @abstractmethod
    def tags(self) -> list: ...

    @abstractmethod
    def add_tag(self, tag_name: str) -> None: ...

    @abstractmethod
    def remove_tag(self, tag_name: str) -> None: ...

    @property
    @abstractmethod
    def record_name(self) -> str: ...

    @record_name.setter
    @abstractmethod
    def record_name(self, note_name: str): ...

    @property
    @abstractmethod
    def storage_id(self) -> str: ...

    @property
    @abstractmethod
    def file_path(self) -> str: ...

    @property
    @abstractmethod
    def last_updated(self) -> datetime: ...
