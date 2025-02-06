from itertools import product
from typing import Callable
from kubeq.operators.boolean.boolean_ops import Bool
from kubeq.operators.boolean.op_and import And
from kubeq.operators.boolean.op_or import Or
from kubeq.operators.op_base import Op
from kubeq.operators.primitives.op_exists import Exists
from kubeq.operators.value_ops.op_glob import Glob
from kubeq.operators.value_ops.op_in import In
from kubeq.operators.value_ops.op_not_glob import NotGlob
from kubeq.operators.value_ops.op_not_in import NotIn
from kubeq.operators.value_ops.op_not_regexp import NotRegex
from kubeq.operators.value_ops.op_regexp import Regex
from kubeq.operators.primitives.op_never import Never
from kubeq.operators.value_ops.op_value import ValueOp


class LeafReducer:
    reductions = 0

    def increment(self):
        self.reductions += 1

    def decrement(self):
        self.reductions -= 1

    def _reduce_pair_and(self, a: Op, b: Op) -> tuple[Op, Op]:
        self.increment()
        match a, b:
            case In(v), In(u):
                return In(v & u), Exists()
            case NotIn(u), NotIn(v):
                return NotIn(u | v), Exists()
            case (In(v), (Regex() | Glob()) as r) | (
                (Regex() | Glob()) as r,
                In(v),
            ):
                return In({u for u in v if r(u)}), Exists()
            case (In(u), NotIn(v)) | (NotIn(v), In(u)):
                return In(u - v), Exists()
            case a, b:
                self.decrement()
                return a, b

    def _reduce_pair_or(self, a: Op, b: Op) -> tuple[Op, Op]:
        self.increment()
        match a, b:
            case Or(kids1), Or(kids2):
                return Or(set(kids1) | set(kids2)), Never()
            case In(v), In(u):
                return In(v | u), Never()
            case NotIn(u), NotIn(v):
                return NotIn(u & v), Never()
            case (NotIn(u), In(v)) | (In(v), NotIn(u)):
                return NotIn(u - v), Never()
            case (NotIn(u), (NotRegex() | NotGlob()) as r) | (
                (NotRegex() | NotGlob()) as r,
                NotIn(u),
            ):
                return NotIn({v for v in u if not r(v)}), Never()

            case a, b:
                self.decrement()
                return a, b

    def _apply_pair_reduction(
        self,
        ops: list[Op],
        pair_reduction: Callable[[Op, Op], tuple[Op, Op]],
    ):

        i = 0
        j = 1
        for i in range(len(ops)):
            for j in range(i + 1, len(ops)):
                ops[i], ops[j] = pair_reduction(ops[i], ops[j])

    def pair_reduce(self, op: Op) -> Op:
        match op:
            case And(kids):
                kids = [self.pair_reduce(kid) for kid in kids]
                self._apply_pair_reduction(kids, self._reduce_pair_and)
                return And(kids)
            case Or(kids):
                self._apply_pair_reduction(kids, self._reduce_pair_or)
                return Or(kids)
            case _:
                return op
