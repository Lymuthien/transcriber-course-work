from abc import ABC, abstractmethod


class ITranscribeProcessor(ABC):
    @abstractmethod
    def transcribe_audio(self,
                         content: bytes) -> str:
        """
        Transcribe given audio bytes into text.

        :param content: Audio bytes to transcribe.
        :return: Transcribed text.
        """
        pass


class WhisperProcessor(ITranscribeProcessor):
    def __init__(self,
                 model_size: str = 'base'):
        """Initialize Whisper model.

        :param model_size: Whisper model size (default 'base').
        """
        pass

    def transcribe_audio(self,
                         content: bytes) -> str:
        """
        Transcribe given audio bytes into text.
        Uses whisper model to transcribe audio file.
        It is the main function of the class.

        :param content: Audio bytes to transcribe.
        :return: Transcribed text.
        """
        pass
