import whisper
import numpy as np

from ..interfaces import WhisperTranscribeProcessor


class WhisperProcessor(WhisperTranscribeProcessor):
    def __init__(self, model_size: str = 'base'):
        """
        Initialize Whisper model.

        :param model_size: Whisper model size (e.g., 'base', 'small', 'medium', 'large') (default 'base').
        """

        self.model_size = model_size
        self.model = whisper.load_model(model_size)

    def transcribe_audio(self,
                         audio: np.ndarray,
                         language: str = None,
                         main_theme: str = None) -> tuple[str, str]:
        """
        Transcribe given audio bytes into text without saving content to a file.

        :param audio: Audio bytes to transcribe (e.g., mp3 format).
        :param language: Language of the audio (optional).
        :param main_theme: Main theme of the audio (optional).
        :return: Transcribed text and detected language.
        """

        audio = audio.astype(np.float32)

        options = {
            "language": language,
            "initial_prompt": main_theme
        }
        result = whisper.transcribe(self.model, audio, **options)

        transcription = result.get('text', '').strip()
        detected_language = result.get('language', language or 'unknown')

        return transcription, detected_language
