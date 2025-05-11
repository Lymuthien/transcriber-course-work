from abc import ABC, abstractmethod

from transcriber_service.domain.interfaces.services.iserializer import ISerializer


class IFileManager(ABC):
    @staticmethod
    @abstractmethod
    def save(
        data, path: str, binary: bool = True, serializer: ISerializer = None
    ) -> None: ...

    @staticmethod
    @abstractmethod
    def load(path: str, binary: bool = True, serializer: ISerializer = None): ...
