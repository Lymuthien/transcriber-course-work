"""
Module: whisper_processor

This module defines the `WhisperProcessor` class, which uses the Whisper
library to perform speech-to-text transcription.

Classes
-------
WhisperProcessor :
    Provides methods for transcribing audio using Whisper.
"""

import whisper
import numpy as np

from ..interfaces import WhisperTranscribeProcessor


class WhisperProcessor(WhisperTranscribeProcessor):
    """
    A processor for audio-to-text transcription using Whisper.

    Methods
    -------
    transcribe_audio(audio, language, main_theme):
        Transcribes audio content and optionally detects language.
    """

    def __init__(self, model_size: str = 'base'):
        """
        Initializes the WhisperProcessor.

        Parameters
        ----------
        model_size : str, optional
            The size of the Whisper model to load. Defaults to 'base'.
        """

        self.model_size = model_size
        self.model = whisper.load_model(model_size)

    def transcribe_audio(self,
                         audio: np.ndarray,
                         language: str = None,
                         main_theme: str = None) -> tuple[str, str]:
        """
        Transcribe given audio into text and detects the language.

        Parameters
        ----------
        audio: np.ndarray
            Audio to transcribe (e.g., mp3 format).
        language: str, optional
            Language of the audio.
        main_theme: str, optional
            Main theme of the audio.

        Returns
        -------
        tuple[str, str]
            Transcribed text and detected language.
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
