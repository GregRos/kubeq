from abc import ABC, abstractmethod
from typing import Callable, ClassVar, TypeGuard, TypeIs


class Op(ABC):
    @abstractmethod
    def __call__(self, what: str) -> bool: ...

    @abstractmethod
    def __eq__(self, other: object) -> bool: ...

    @abstractmethod
    def __hash__(self) -> int: ...
