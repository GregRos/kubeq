from abc import abstractmethod
from typing import Any


class BaseAttr:
    @abstractmethod
    def get(self, object: Any) -> Any:
        pass
