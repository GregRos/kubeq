from abc import ABC, abstractmethod
from typing import Callable, ClassVar, TypeGuard, TypeIs


class UnboundedToken:
    pass


class Op[T = str](ABC):
    @abstractmethod
    def __call__(self, what: T) -> bool: ...

    @abstractmethod
    def __eq__(self, other: object) -> bool: ...

    @abstractmethod
    def __hash__(self) -> int: ...

    @abstractmethod
    def normalize(self) -> "Op[T]": ...

    def and_(self, *others: "Op[T]"):
        from kubeq.query._operators._boolean.op_and import And

        return And([self, *others])

    def or_(self, *others: "Op[T]"):
        from kubeq.query._operators._boolean.op_or import Or

        return Or([self, *others])
