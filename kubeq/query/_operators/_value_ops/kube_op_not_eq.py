from typing import override
from kubeq.query._operators._value_ops.kube_op_eq import Eq
from kubeq.query._operators._value_ops.negated_op import NegatedOp
from kubeq.query._operators._value_ops.op_not_in import NotIn
from kubeq.query._operators._value_ops.op_value import ValueOp


class NotEq(ValueOp[str], NegatedOp, value_type=str):

    def normalize(self) -> "NotIn":
        return NotIn({self.value}, original=self)

    @property
    @override
    def positive(self) -> ValueOp[str]:
        return Eq(self.value)

    def __repr__(self) -> str:
        return f"!{self.value!r}"
