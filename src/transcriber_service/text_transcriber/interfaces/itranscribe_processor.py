import numpy as np
from abc import ABC, abstractmethod

from ..helpers import AudioProcessingMixin


class ITranscribeProcessor(ABC):
    @abstractmethod
    def transcribe_audio(self,
                         content: bytes,
                         language: str = None,
                         main_theme: str = None) -> tuple[str, str]: ...


class WhisperTranscribeProcessor(ITranscribeProcessor, AudioProcessingMixin):
    @abstractmethod
    def transcribe_audio(self,
                         audio: np.ndarray,
                         language: str = None,
                         main_theme: str = None) -> tuple[str, str]: ...
