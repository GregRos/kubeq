from abc import ABC, abstractmethod
from typing import Callable, ClassVar, TypeGuard, TypeIs


class UnboundedToken:
    pass


class Op(ABC):
    @abstractmethod
    def __call__(self, what: str) -> bool: ...

    @abstractmethod
    def __eq__(self, other: object) -> bool: ...

    @abstractmethod
    def __hash__(self) -> int: ...

    @abstractmethod
    def normalize(self) -> "Op": ...

    def and_(self, *others: "Op"):
        from kubeq.query._operators._boolean.op_and import And

        return And([self, *others])

    def or_(self, *others: "Op"):
        from kubeq.query._operators._boolean.op_or import Or

        return Or([self, *others])
