import numpy as np
from faster_whisper import WhisperModel

from ..interfaces import WhisperTranscribeProcessor


class FasterWhisperProcessor(WhisperTranscribeProcessor):
    def __init__(self, model_size: str = 'base'):
        """
        Initialize Faster Whisper model.

        :param model_size: Whisper model size (e.g., 'base', 'small', 'medium', 'large') (default 'base').
        """

        self.model_size = model_size
        self.model = WhisperModel(model_size)

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
        segments, info = self.model.transcribe(audio, **options)

        transcription = " ".join(segment.text for segment in segments).strip()
        detected_language = info.language if language is None else language

        return transcription, detected_language
