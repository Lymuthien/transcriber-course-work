from abc import ABC, abstractmethod


class ITranscribeProcessor(ABC):
    @abstractmethod
    def transcribe_audio(self,
                         content: bytes,
                         language: str = None,
                         main_theme: str = None) -> str:
        """
        Transcribe given audio bytes into text.

        :param content: Audio bytes to transcribe.
        :param language: Language of the audio.
        :param main_theme: Main theme of the audio.
        :return: Transcribed text.
        """

        pass
