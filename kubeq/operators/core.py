from abc import ABC, abstractmethod
from typing import ClassVar


class Op(ABC):
    @abstractmethod
    def __call__(self, what: str) -> bool: ...

    def is_op(self, t: "type[Op]") -> bool:
        return isinstance(self, t)
