from audio_transcribing import Transcriber as BaseTranscriber
from ..domain.interfaces import ITranscriber


class Transcriber(ITranscriber):
    def __init__(self, token: str):
        self._transcriber = BaseTranscriber(token)

    def transcribe(
        self,
        content: bytes,
        language: str | None,
        max_speakers: int | None,
        main_theme: str | None,
    ) -> tuple[str, str]:
        return self._transcriber.transcribe(content, language, max_speakers, main_theme)
