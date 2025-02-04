from dataclasses import dataclass
from kubeq.operators.op_base import Op


from typing import Callable, Iterable


class Or(Op):
    __match_args__ = ("kids",)

    kids: set[Op]

    @staticmethod
    def of(*operators: Op) -> "Or":
        return Or(set(operators))

    def __init__(self, operators: Iterable[Op]) -> None:
        self.kids = set(operators)

    def __call__(self, what: str) -> bool:
        return any(op(what) for op in self.kids)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.kids == other.kids

    def __hash__(self) -> int:
        return hash(self.kids)

    def __iter__(self):
        return iter(self.kids)
