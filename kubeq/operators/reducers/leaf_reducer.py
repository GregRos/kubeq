from itertools import product
from typing import Callable
from kubeq.operators.boolean.boolean_ops import op_Bool
from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import op_Any
from kubeq.operators.primitives.op_always import op_Always
from kubeq.operators.primitives.op_exists import op_Exists
from kubeq.operators.primitives.op_missing import op_Missing
from kubeq.operators.reducers.base_reducer import BaseReducer
from kubeq.operators.value_ops.kube_op_eq import op_Eq
from kubeq.operators.value_ops.kube_op_not_eq import op_NotEq
from kubeq.operators.value_ops.op_glob import op_Glob
from kubeq.operators.value_ops.op_in import op_In
from kubeq.operators.value_ops.op_not_glob import op_NotGlob
from kubeq.operators.value_ops.op_not_in import op_NotIn
from kubeq.operators.value_ops.op_not_regexp import op_NotRegex
from kubeq.operators.value_ops.op_regexp import op_Regex
from kubeq.operators.primitives.op_never import op_Never
from kubeq.operators.value_ops.op_value import op_ValueOp


class LeafReducer(BaseReducer):

    def _reduce_pair_and(self, a: op_Any, b: op_Any) -> tuple[op_Any, op_Any]:
        self.increment()
        a = a.normalize()
        b = b.normalize()
        match a, b:
            # MISSING & NOTIN -> MISSING
            # MISSING & NOTREGEX -> MISSING
            # Reason: MISSING is like a NOTREGEX(/.*/) or NOTIN(all) so it's a subset of both
            case (op_Missing(), (op_NotIn() | op_NotRegex())) | (
                ((op_NotIn() | op_NotRegex()), op_Missing()),
            ):
                return op_Missing(), op_Always()
            # EXISTS & IN -> IN
            # EXISTS & REGEX -> REGEX
            # Reason: EXISTS is like a REGEX(/.*/) or IN(all) so it's a superset of both
            case (op_Exists(), (op_In() | op_Regex()) as r) | (
                (op_In() | op_Regex()) as r,
                op_Exists(),
            ):
                return r, op_Always()
            # This squashes two neighboring And clauses
            # Most of the squashing happens in a different reduction but we do it here for this case
            case op_And(kids1), op_And(kids2):
                return op_And(set(kids1) | set(kids2)), op_Always()

            # IN(u) & IN(v) -> IN(u & v)
            # Reason: Value must be in both
            case op_In(v), op_In(u):
                return op_In(v & u), op_Always()
            # NOTIN(u) & NOTIN(v) -> NOTIN(u | v)
            # Reason: Value must not be in either
            case op_NotIn(u), op_NotIn(v):
                return op_NotIn(u | v), op_Always()
            # IN(us) & NOTIN(vs) -> IN(us - vs)
            # Reason: Value must be in us and not in vs
            case (op_In(u), op_NotIn(v)) | (op_NotIn(v), op_In(u)):
                return op_In(u - v), op_Always()
            # IN(us) & REGEX(/r/) -> IN(us filtered by /r/)
            # Reason: Value must be in us and match /r/
            case (op_In(v), op_Regex() as r) | (
                op_Regex() as r,
                op_In(v),
            ):
                return op_In({u for u in v if r(u)}), op_Always()

            case a, b:
                self.decrement()
                return a, b

    def _reduce_pair_or(self, a: op_Any, b: op_Any) -> tuple[op_Any, op_Any]:
        self.increment()
        a = a.normalize()
        b = b.normalize()
        match a, b:
            # MISSING | NOTIN -> NOTIN
            # MISSING | NOTREGEX -> NOTREGEX
            # Reason: MISSING is like NOTREGEX(/.*/) or NOTIN(all) so it's a subset of both
            case op_Missing(), (op_NotIn() | op_NotRegex() as r) | (
                (op_NotIn() | op_NotRegex()) as r,
                op_Missing(),
            ):
                return r, op_Always()
            # EXISTS | IN -> EXISTS
            # EXISTS | REGEX -> EXISTS
            # Reason: EXISTS is like a REGEX(/.*/) or IN(all) so it's a superset of both
            case (op_Exists(), (op_In() | op_Regex())) | (
                (op_In() | op_Regex()),
                op_Exists(),
            ):
                return op_Exists(), op_Always()
            # Squash OR nodes
            case op_Or(kids1), op_Or(kids2):
                return op_Or(set(kids1) | set(kids2)), op_Never()
            # IN(u) | IN(v) -> IN(u | v)
            # Reason: Value must be in either
            case op_In(v), op_In(u):
                return op_In(v | u), op_Never()
            # NOTIN(u) | NOTIN(v) -> NOTIN(u & v)
            # Reason: Value must not be in both
            case op_NotIn(u), op_NotIn(v):
                return op_NotIn(u & v), op_Never()
            #
            # IN(us) | NOTIN(vs) -> NOTIN(vs - us)
            # Reason: Value should either not be in vs or be in us
            # It allows some values in vs as an alternative
            case (op_NotIn(u), op_In(v)) | (op_In(v), op_NotIn(u)):
                return op_NotIn(u - v), op_Never()

            case (op_NotIn(u), op_NotRegex() as r) | (
                op_NotRegex() as r,
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

    def reduce(self, op: op_Any) -> op_Any:
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
