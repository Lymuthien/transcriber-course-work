from ..interfaces import ResamplingVoiceSeparator


class VoiceSeparatorDirector(object):
    def __init__(self, separator: ResamplingVoiceSeparator):
        self._separator = separator

    def set_separator(self, separator: ResamplingVoiceSeparator):
        self._separator = separator

    def separate_speakers(self,
                          content: bytes,
                          max_speakers: int | None = None) -> list[dict]:
        audio, sr = self._separator.get_audio_stream(content)
        audio = self._separator.get_mono_audio(audio)
        audio = self._separator.resample_audio(audio, sr)
        return self._separator.separate_speakers(audio, max_speakers)
