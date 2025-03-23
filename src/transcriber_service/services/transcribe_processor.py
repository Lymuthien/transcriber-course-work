from ..interfaces.itranscribe_processor import ITranscribeProcessor


# Work 3.

class WhisperProcessor(ITranscribeProcessor):
    def __init__(self,
                 model_size: str = 'base'):
        """Initialize Whisper model.

        :param model_size: Whisper model size (default 'base').
        """

        pass

    def transcribe_audio(self,
                         content: bytes,
                         language: str = None,
                         main_theme: str = None) -> str:
        """
        Transcribe given audio bytes into text.
        Uses whisper model to transcribe audio file.
        It is the main function of the class.

        :param content: Audio bytes to transcribe (mp3 format).
        :param language: Language of the audio.
        :param main_theme: Main theme of the audio.
        :return: Transcribed text.
        """

        return 'Пустой вокзал нам шепчет что я стану...'
