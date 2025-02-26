from abc import ABC
from typing import TYPE_CHECKING, Any, Iterable, Self, overload

from kubeq.query._operators._op_base import Op


class Bool[T](Op[T], ABC):
    __match_args__ = ("operands",)

    operands: list[Op[T]]

    @overload
    def __init__(self, *operators: Op[T]) -> None: ...

    @overload
    def __init__(self, operators: Iterable[Op[T]], /) -> None: ...

    def __init__(self, *args: Any) -> None:
        match list(args):
            case []:
                operands = []
            case [Op(), *_] as x:
                operands = x
            case [x] if isinstance(x, Iterable):
                operands = list(x)
            case _:
                raise ValueError("Invalid arguments")
        self.operands = operands
        super().__init__()

    def __iter__(self):
        return iter(self.operands)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.operands == other.operands

    def __hash__(self) -> int:
        return hash(frozenset(self.operands))

    def normalize(self) -> Op[T]:
        return self
