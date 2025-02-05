from kubeq.operators.boolean.boolean_ops import Bool
from kubeq.operators.op_base import Op


from typing import Callable, Iterable


class And(Bool):

    @classmethod
    def of(cls, *operators: Op) -> "And":
        match operators:
            case (And() as r,):
                return r
            case _:
                return And(operators)

    def __call__(self, what: str) -> bool:
        return all(op(what) for op in self.operands)
