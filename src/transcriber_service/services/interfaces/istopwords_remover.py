from abc import ABC, abstractmethod


class IStopwordsRemover(ABC):
    @abstractmethod
    def remove_parasite_words(self, text: str, remove_swear_words: bool = True) -> str: ...

