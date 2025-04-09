from abc import ABC, abstractmethod

import numpy as np

from ..helpers import AudioProcessingMixin


class IVoiceSeparator(ABC):
    @abstractmethod
    def separate_speakers(self,
                          content: np.ndarray,
                          num_speakers: int) -> list[dict]: ...


class ResamplingVoiceSeparator(IVoiceSeparator, AudioProcessingMixin):
    @abstractmethod
    def separate_speakers(self,
                          content: np.ndarray,
                          num_speakers: int) -> list[dict]: ...