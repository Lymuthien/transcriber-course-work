from abc import ABC, abstractmethod
from typing import Any


class IRestorable(ABC):
    @abstractmethod
    @abstractmethod
    def restore_state(self, data: dict[str, Any]):
        pass
