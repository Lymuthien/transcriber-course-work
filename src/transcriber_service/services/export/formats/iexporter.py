from abc import ABC, abstractmethod

class IExporter(ABC):
    @abstractmethod
    def export(self, content: str, output_path: str) -> None:
        pass

    @property
    @abstractmethod
    def file_extension(self) -> str:
        pass