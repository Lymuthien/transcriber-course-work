from abc import ABC, abstractmethod


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
