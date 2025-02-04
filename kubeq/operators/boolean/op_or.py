from dataclasses import dataclass
from kubeq.operators.boolean.boolean_ops import op_Bool
from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.op_base import Op


from typing import Callable, Iterable, Self


class op_Or(op_Bool):

    @classmethod
    def of(cls, *operators: Op) -> "op_Or":
        match operators:
            case (op_Or() as r,):
                return r
            case _:
                return op_Or(operators)

    def __call__(self, what: str) -> bool:
        return any(op(what) for op in self.operands)
