from abc import ABC, abstractmethod


class IVoiceSeparator(ABC):
    @abstractmethod
    def separate_speakers(self,
                          content: bytes,
                          num_speakers: int) -> list[dict]: ...