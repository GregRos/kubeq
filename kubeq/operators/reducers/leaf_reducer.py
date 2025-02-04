from itertools import product
from typing import Callable
from kubeq.operators.boolean.boolean_ops import op_Bool
from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import Op
from kubeq.operators.primitives.op_always import op_Always
from kubeq.operators.reducers.base_reducer import BaseReducer
from kubeq.operators.value_ops.op_glob import op_Glob
from kubeq.operators.value_ops.op_in import op_In
from kubeq.operators.value_ops.op_not_glob import op_NotGlob
from kubeq.operators.value_ops.op_not_in import op_NotIn
from kubeq.operators.value_ops.op_not_regexp import op_NotRegex
from kubeq.operators.value_ops.op_regexp import op_Regex
from kubeq.operators.value_ops.simplify_trivial import simplify_trivial
from kubeq.operators.primitives.op_never import op_Never
from kubeq.operators.value_ops.op_value import op_ValueOp
from kubeq.query_plan.kube_ops import op_Eq, op_NotEq


class LeafReducer(BaseReducer):

    def _reduce_pair_and(self, a: Op, b: Op) -> tuple[Op, Op]:
        self.increment()
        match a, b:
            case op_In(v), op_In(u):
                return op_In(v & u), op_Always()
            case op_NotIn(u), op_NotIn(v):
                return op_NotIn(u | v), op_Always()
            case (op_In(v), (op_Regex() | op_Glob()) as r) | (
                (op_Regex() | op_Glob()) as r,
                op_In(v),
            ):
                return op_In({u for u in v if r(u)}), op_Always()
            case (op_In(u), op_NotIn(v)) | (op_NotIn(v), op_In(u)):
                return op_In(u - v), op_Always()
            case a, b:
                self.decrement()
                return a, b

    def _reduce_pair_or(self, a: Op, b: Op) -> tuple[Op, Op]:
        self.increment()
        match a, b:
            case op_Eq(v), op_NotEq(u) if v == u:
                return op_Always(), op_Never()
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
        self, ops: list[Op], pair_reduction: Callable[[Op, Op], tuple[Op, Op]]
    ):

        i = 0
        j = 1
        for i in range(len(ops)):
            for j in range(i + 1, len(ops)):
                ops[i], ops[j] = pair_reduction(ops[i], ops[j])

    def reduce(self, op: Op) -> Op:
        match op:
            case op_And(kids):
                kids = [self.reduce(kid) for kid in kids]
                self._apply_pair_reduction(kids, self._reduce_pair_and)
                return op_And(kids)
            case op_Or(kids):
                self._apply_pair_reduction(kids, self._reduce_pair_or)
                return op_And(kids)
            case _:
                return op
