from abc import ABC, abstractmethod

class IFileManager(ABC):
    @staticmethod
    @abstractmethod
    def save(data,
             path: str) -> None: ...

    @staticmethod
    @abstractmethod
    def load(path: str): ...


