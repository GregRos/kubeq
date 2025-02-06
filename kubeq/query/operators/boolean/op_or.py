from dataclasses import dataclass
from kubeq.operators._utils._print import collection_repr
from kubeq.operators.boolean.boolean_ops import Bool
from kubeq.operators.boolean.op_and import And
from kubeq.operators.op_base import Op


from typing import Callable, Iterable, Self


class Or(Bool):

    @classmethod
    def of(cls, *operators: Op) -> "Or":
        match operators:
            case (Or() as r,):
                return r
            case _:
                return Or(operators)

    def __call__(self, what: str) -> bool:
        return any(op(what) for op in self.operands)

    def __repr__(self) -> str:
        return collection_repr("", "|", self.operands)
