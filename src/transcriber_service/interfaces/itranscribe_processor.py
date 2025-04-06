from abc import ABC, abstractmethod


class ITranscribeProcessor(ABC):
    @abstractmethod
    def transcribe_audio(self,
                         content: bytes,
                         language: str = None,
                         main_theme: str = None) -> tuple[str, str]: ...

class IVoiceSeparator(ABC):
    @abstractmethod
    def separate_speakers(self,
                          content: bytes,
                          num_speakers: int) -> list[dict]: ...