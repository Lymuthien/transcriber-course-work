from io import BytesIO
import numpy as np
import soundfile as sf
import scipy.signal


class AudioProcessingMixin(object):
    @staticmethod
    def get_audio_stream(content: bytes) -> tuple:
        audio_stream = BytesIO(content)
        audio, sr = sf.read(audio_stream)

        return audio, sr

    @staticmethod
    def get_mono_audio(audio: np.ndarray) -> np.ndarray:
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)

        return audio

    @staticmethod
    def resample_audio(audio: np.ndarray, sr: int) -> np.ndarray:
        if sr != 16000:
            number_of_samples = round(len(audio) * float(16000) / sr)
            audio = scipy.signal.resample(audio, number_of_samples)

        return audio
