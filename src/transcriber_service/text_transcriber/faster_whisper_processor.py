from faster_whisper import WhisperModel
import numpy as np
import soundfile as sf
from io import BytesIO
import scipy.signal

from .interfaces import ITranscribeProcessor


class FasterWhisperProcessor(ITranscribeProcessor):
    def __init__(self, model_size: str = 'base'):
        """
        Initialize Faster Whisper model.

        :param model_size: Whisper model size (e.g., 'base', 'small', 'medium', 'large') (default 'base').
        """

        self.model_size = model_size
        self.model = WhisperModel(model_size)

    def transcribe_audio(self,
                         content: bytes,
                         language: str = None,
                         main_theme: str = None) -> tuple[str, str]:
        """
        Transcribe given audio bytes into text without saving content to a file.

        :param content: Audio bytes to transcribe (e.g., mp3 format).
        :param language: Language of the audio (optional).
        :param main_theme: Main theme of the audio (optional).
        :return: Transcribed text and detected language.
        """

        audio_stream = BytesIO(content)
        audio, sr = sf.read(audio_stream)

        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        if sr != 16000:
            number_of_samples = round(len(audio) * float(16000) / sr)
            audio = scipy.signal.resample(audio, number_of_samples)

        audio = audio.astype(np.float32)

        options = {"language": language, }
        segments, info = self.model.transcribe(audio, **options)

        transcription = " ".join(segment.text for segment in segments).strip()

        detected_language = info.language if language is None else language

        return transcription, detected_language
