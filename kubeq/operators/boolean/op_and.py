from kubeq.operators.boolean.boolean_ops import op_Bool
from kubeq.operators.op_base import Op


from typing import Callable, Iterable


class op_And(op_Bool):

    def __call__(self, what: str) -> bool:
        return all(op(what) for op in self.operands)
