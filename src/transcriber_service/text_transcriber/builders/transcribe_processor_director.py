from ..interfaces import WhisperTranscribeProcessor


class TranscribeProcessorDirector(object):
    def __init__(self, processor: WhisperTranscribeProcessor):
        self._processor = processor

    def set_processor(self, processor: WhisperTranscribeProcessor):
        self._processor = processor

    def transcribe_audio(self,
                         content: bytes,
                         language: str = None,
                         main_theme: str = None) -> tuple[str, str]:
        audio, sr = self._processor.get_audio_stream(content)
        audio = self._processor.get_mono_audio(audio)
        audio = self._processor.resample_audio(audio, sr)
        return self._processor.transcribe_audio(audio, language, main_theme)
