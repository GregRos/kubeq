from abc import ABC
from typing import Iterable, Self
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.op_base import Op


class op_Bool(Op, ABC):
    __match_args__ = ("operands",)

    operands: list[Op]

    @classmethod
    def of(cls, *operators: Op) -> "Self":
        return cls(set(operators))

    def __init__(self, operators: Iterable[Op]) -> None:
        self.operands = list(operators)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.operands == other.operands

    def __hash__(self) -> int:
        return hash(self.operands)

    def simplify(self):
        