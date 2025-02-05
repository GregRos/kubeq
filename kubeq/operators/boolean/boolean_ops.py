from abc import ABC
from typing import Any, Iterable, Self, overload
from kubeq.operators.boolean.op_or import Or
from kubeq.operators.boolean.op_and import And
from kubeq.operators.op_base import Op


class Bool(Op, ABC):
    __match_args__ = ("operands",)

    operands: list[Op]

    @overload
    def __init__(self, *operators: Op) -> None: ...

    @overload
    def __init__(self, operators: Iterable[Op], /) -> None: ...

    def __init__(self, *args: Any) -> None:
        match list(args):
            case []:
                self.operands = []
            case [Op(), *_] as x:
                self.operands = x
            case [Iterable() as x]:
                self.operands = list(x)
            case _:
                raise ValueError("Invalid arguments")
        super().__init__()

    def __iter__(self):
        return iter(self.operands)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.operands == other.operands

    def __hash__(self) -> int:
        return hash(self.operands)

    def normalize(self) -> Op:
        return self
