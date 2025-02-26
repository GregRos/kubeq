from dataclasses import dataclass
from kubeq.query._utils.render_parts import collection_repr
from kubeq.query._operators._boolean.boolean_ops import Bool
from kubeq.query._operators._boolean.op_and import And
from kubeq.query._operators._op_base import Op


from typing import Callable, Iterable, Self


class Or[T](Bool[T]):

    @classmethod
    def of(cls, *operators: Op) -> "Or":
        match operators:
            case (Or() as r,):
                return r
            case _:
                return Or(operators)

    def __call__(self, what: T) -> bool:
        return any(op(what) for op in self.operands)

    def __repr__(self) -> str:
        return " | ".join(map(repr, self.operands))
