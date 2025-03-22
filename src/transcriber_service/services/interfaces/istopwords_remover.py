from abc import ABC, abstractmethod


class IStopwordsRemover(ABC):
    @abstractmethod
    def remove_parasite_words(self, text: str, remove_swear_words: bool = True) -> str: ...

    @abstractmethod
    def remove_words(self, text: str, removing_words: tuple | list) -> str: ...

