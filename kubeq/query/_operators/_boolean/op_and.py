from kubeq.query._utils.render_parts import collection_repr
from kubeq.query._operators._boolean.boolean_ops import Bool
from kubeq.query._operators._op_base import Op


from typing import Callable, Iterable


class And[T](Bool[T]):

    @classmethod
    def of(cls, *operators: Op[T]) -> "And":
        match operators:
            case (And() as r,):
                return r
            case _:
                return And(operators)

    def __call__(self, what: T) -> bool:
        return all(op(what) for op in self.operands)

    def __repr__(self) -> str:
        return " & ".join(map(repr, self.operands))
