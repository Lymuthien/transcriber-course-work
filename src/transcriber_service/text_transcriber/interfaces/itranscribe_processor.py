from abc import ABC, abstractmethod


class ITranscribeProcessor(ABC):
    @abstractmethod
    def transcribe_audio(self,
                         content: bytes,
                         language: str = None,
                         main_theme: str = None) -> tuple[str, str]: ...
