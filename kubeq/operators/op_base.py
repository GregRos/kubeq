from abc import ABC, abstractmethod
from typing import Callable, ClassVar, TypeGuard, TypeIs


class op_Any(ABC):
    @abstractmethod
    def __call__(self, what: str) -> bool: ...

    @abstractmethod
    def __eq__(self, other: object) -> bool: ...

    @abstractmethod
    def __hash__(self) -> int: ...

    @abstractmethod
    def normalize(self) -> "op_Any": ...
