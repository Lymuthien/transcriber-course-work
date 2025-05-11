from audio_transcribing import NatashaStopwordsRemover as BaseStopwordsRemover
from ..domain.interfaces import IStopwordsRemover


class StopwordsRemover(IStopwordsRemover):
    def __init__(self):
        self._remover = BaseStopwordsRemover()

    def remove_stopwords(
        self, text: str, remove_swear_words: bool, go_few_times: bool
    ) -> str:
        return self._remover.remove_stopwords(text, remove_swear_words, go_few_times)

    def remove_words(self, text: str, words: list[str] | tuple[str]) -> str:
        return self._remover.remove_words(text, words)
