from abc import ABC
from typing import Iterable, Self
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.op_base import op_Any


class op_Bool(op_Any, ABC):
    __match_args__ = ("operands",)

    operands: list[op_Any]

    def __init__(self, operators: Iterable[op_Any]) -> None:
        self.operands = list(operators)

    def __iter__(self):
        return iter(self.operands)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.operands == other.operands

    def __hash__(self) -> int:
        return hash(self.operands)

    def normalize(self) -> op_Any:
        return self
