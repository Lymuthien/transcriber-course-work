from abc import ABC, abstractmethod


class IDictable(ABC):
    @abstractmethod
    def to_dict(self, data) -> dict: ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict): ...


class ISerializer(ABC):
    @abstractmethod
    def serialize(self, data) -> str: ...

    @abstractmethod
    def deserialize(self, data: str): ...

    @property
    @abstractmethod
    def binary(self) -> bool: ...

    @property
    @abstractmethod
    def extension(self) -> str: ...
