from abc import ABC, abstractmethod


class IDictable(ABC):
    @abstractmethod
    def to_dict(self, data) -> dict: ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict): ...
