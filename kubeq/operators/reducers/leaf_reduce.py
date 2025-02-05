from itertools import product
from typing import Callable
from kubeq.operators.boolean.boolean_ops import op_Bool
from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import op_Any
from kubeq.operators.primitives.op_exists import op_Exists
from kubeq.operators.value_ops.op_glob import op_Glob
from kubeq.operators.value_ops.op_in import op_In
from kubeq.operators.value_ops.op_not_glob import op_NotGlob
from kubeq.operators.value_ops.op_not_in import op_NotIn
from kubeq.operators.value_ops.op_not_regexp import op_NotRegex
from kubeq.operators.value_ops.op_regexp import op_Regex
from kubeq.operators.value_ops.simplify_trivial import simplify_trivial
from kubeq.operators.primitives.op_never import op_Never
from kubeq.operators.value_ops.op_value import op_ValueOp


class LeafReducer:
    reductions = 0

    def increment(self):
        self.reductions += 1

    def decrement(self):
        self.reductions -= 1

    def _reduce_pair_and(self, a: op_Any, b: op_Any) -> tuple[op_Any, op_Any]:
        self.increment()
        match a, b:
            case op_In(v), op_In(u):
                return op_In(v & u), op_Exists()
            case op_NotIn(u), op_NotIn(v):
                return op_NotIn(u | v), op_Exists()
            case (op_In(v), (op_Regex() | op_Glob()) as r) | (
                (op_Regex() | op_Glob()) as r,
                op_In(v),
            ):
                return op_In({u for u in v if r(u)}), op_Exists()
            case (op_In(u), op_NotIn(v)) | (op_NotIn(v), op_In(u)):
                return op_In(u - v), op_Exists()
            case a, b:
                self.decrement()
                return a, b

    def _reduce_pair_or(self, a: op_Any, b: op_Any) -> tuple[op_Any, op_Any]:
        self.increment()
        match a, b:
            case op_Or(kids1), op_Or(kids2):
                return op_Or(set(kids1) | set(kids2)), op_Never()
            case op_In(v), op_In(u):
                return op_In(v | u), op_Never()
            case op_NotIn(u), op_NotIn(v):
                return op_NotIn(u & v), op_Never()
            case (op_NotIn(u), op_In(v)) | (op_In(v), op_NotIn(u)):
                return op_NotIn(u - v), op_Never()
            case (op_NotIn(u), (op_NotRegex() | op_NotGlob()) as r) | (
                (op_NotRegex() | op_NotGlob()) as r,
                op_NotIn(u),
            ):
                return op_NotIn({v for v in u if not r(v)}), op_Never()

            case a, b:
                self.decrement()
                return a, b

    def _apply_pair_reduction(
        self,
        ops: list[op_Any],
        pair_reduction: Callable[[op_Any, op_Any], tuple[op_Any, op_Any]],
    ):

        i = 0
        j = 1
        for i in range(len(ops)):
            for j in range(i + 1, len(ops)):
                ops[i], ops[j] = pair_reduction(ops[i], ops[j])

    def pair_reduce(self, op: op_Any) -> op_Any:
        match op:
            case op_And(kids):
                kids = [self.pair_reduce(kid) for kid in kids]
                self._apply_pair_reduction(kids, self._reduce_pair_and)
                return op_And(kids)
            case op_Or(kids):
                self._apply_pair_reduction(kids, self._reduce_pair_or)
                return op_And(kids)
            case _:
                return op
