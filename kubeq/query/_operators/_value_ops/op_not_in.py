from typing import overload, override
from kubeq.query._operators._op_base import Op
from kubeq.query._operators._value_ops.negated_op import NegatedOp
from kubeq.query._operators._value_ops.op_in import In
from kubeq.query._operators._value_ops.op_multi_value import MultiValueOp
from kubeq.query._operators._value_ops.op_value import ValueOp


class NotIn(MultiValueOp, NegatedOp, value_type=set[str]):

    @property
    @override
    def positive(self) -> MultiValueOp:
        return In(self.value)

    def __call__(self, what: str) -> bool:
        return what not in self.value
