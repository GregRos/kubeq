from itertools import product
from typing import Callable
from kubeq.operators.boolean.boolean_ops import Bool
from kubeq.operators.boolean.op_and import And
from kubeq.operators.boolean.op_or import Or
from kubeq.operators.op_base import Op
from kubeq.operators.primitives.op_always import Always
from kubeq.operators.primitives.op_exists import Exists
from kubeq.operators.primitives.op_missing import Missing
from kubeq.operators.reducers.base_reducer import BaseReducer
from kubeq.operators.value_ops.kube_op_eq import Eq
from kubeq.operators.value_ops.kube_op_not_eq import NotEq
from kubeq.operators.value_ops.op_glob import Glob
from kubeq.operators.value_ops.op_in import In
from kubeq.operators.value_ops.op_not_glob import NotGlob
from kubeq.operators.value_ops.op_not_in import NotIn
from kubeq.operators.value_ops.op_not_regexp import NotRegex
from kubeq.operators.value_ops.op_regexp import Regex
from kubeq.operators.primitives.op_never import Never
from kubeq.operators.value_ops.op_value import ValueOp


class LeafReducer(BaseReducer):

    def _reduce_pair_and(self, a: Op, b: Op) -> tuple[Op, Op]:
        self.increment()
        a = a.normalize()
        b = b.normalize()
        match a, b:
            # MISSING & NOTIN -> MISSING
            # MISSING & NOTREGEX -> MISSING
            # Reason: MISSING is like a NOTREGEX(/.*/) or NOTIN(all) so it's a subset of both
            case (Missing(), (NotIn() | NotRegex())) | (
                ((NotIn() | NotRegex()), Missing()),
            ):
                return Missing(), Always()
            # EXISTS & IN -> IN
            # EXISTS & REGEX -> REGEX
            # Reason: EXISTS is like a REGEX(/.*/) or IN(all) so it's a superset of both
            case (Exists(), (In() | Regex()) as r) | (
                (In() | Regex()) as r,
                Exists(),
            ):
                return r, Always()
            # This squashes two neighboring And clauses
            # Most of the squashing happens in a different reduction but we do it here for this case
            case And(kids1), And(kids2):
                return And(set(kids1) | set(kids2)), Always()

            # IN(u) & IN(v) -> IN(u & v)
            # Reason: Value must be in both
            case In(v), In(u):
                return In(v & u), Always()
            # NOTIN(u) & NOTIN(v) -> NOTIN(u | v)
            # Reason: Value must not be in either
            case NotIn(u), NotIn(v):
                return NotIn(u | v), Always()
            # IN(us) & NOTIN(vs) -> IN(us - vs)
            # Reason: Value must be in us and not in vs
            case (In(u), NotIn(v)) | (NotIn(v), In(u)):
                return In(u - v), Always()
            # IN(us) & REGEX(/r/) -> IN(us filtered by /r/)
            # Reason: Value must be in us and match /r/
            case (In(v), Regex() as r) | (
                Regex() as r,
                In(v),
            ):
                return In({u for u in v if r(u)}), Always()

            case a, b:
                self.decrement()
                return a, b

    def _reduce_pair_or(self, a: Op, b: Op) -> tuple[Op, Op]:
        self.increment()
        a = a.normalize()
        b = b.normalize()
        match a, b:
            # MISSING | NOTIN -> NOTIN
            # MISSING | NOTREGEX -> NOTREGEX
            # Reason: MISSING is like NOTREGEX(/.*/) or NOTIN(all) so it's a subset of both
            case Missing(), (NotIn() | NotRegex() as r) | (
                (NotIn() | NotRegex()) as r,
                Missing(),
            ):
                return r, Always()
            # EXISTS | IN -> EXISTS
            # EXISTS | REGEX -> EXISTS
            # Reason: EXISTS is like a REGEX(/.*/) or IN(all) so it's a superset of both
            case (Exists(), (In() | Regex())) | (
                (In() | Regex()),
                Exists(),
            ):
                return Exists(), Always()
            # Squash OR nodes
            case Or(kids1), Or(kids2):
                return Or(set(kids1) | set(kids2)), Never()
            # IN(u) | IN(v) -> IN(u | v)
            # Reason: Value must be in either
            case In(v), In(u):
                return In(v | u), Never()
            # NOTIN(u) | NOTIN(v) -> NOTIN(u & v)
            # Reason: Value must not be in both
            case NotIn(u), NotIn(v):
                return NotIn(u & v), Never()
            #
            # IN(us) | NOTIN(vs) -> NOTIN(vs - us)
            # Reason: Value should either not be in vs or be in us
            # It allows some values in vs as an alternative
            case (NotIn(u), In(v)) | (In(v), NotIn(u)):
                return NotIn(u - v), Never()

            case (NotIn(u), NotRegex() as r) | (
                NotRegex() as r,
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

    def reduce(self, op: Op) -> Op:
        match op:
            case And(kids):
                kids = [self.reduce(kid) for kid in kids]
                self._apply_pair_reduction(kids, self._reduce_pair_and)
                return And(kids)
            case Or(kids):
                self._apply_pair_reduction(kids, self._reduce_pair_or)
                return And(kids)
            case _:
                return op
