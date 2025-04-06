import whisper
import numpy as np
import soundfile as sf
from io import BytesIO
import librosa

from ...interfaces.itranscribe_processor import ITranscribeProcessor, IVoiceSeparator


class WhisperProcessor(ITranscribeProcessor):
    def __init__(self, model_size: str = 'base'):
        """
        Initialize Whisper model.

        :param model_size: Whisper model size (e.g., 'base', 'small', 'medium', 'large') (default 'base').
        """

        self.model_size = model_size
        self.model = whisper.load_model(model_size)

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
            audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)

        audio = audio.astype(np.float32)

        options = {"language": language, }
        result = whisper.transcribe(self.model, audio, **options)

        transcription = result.get('text', '').strip()
        detected_language = result.get('language', language or 'unknown')

        return transcription, detected_language
