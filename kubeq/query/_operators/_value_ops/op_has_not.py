from typing import override
from kubeq.query._operators._op_base import Op
from kubeq.query._operators._value_ops.negated_op import NegatedOp
from kubeq.query._operators._value_ops.op_has import Has
from kubeq.query._operators._value_ops.op_multi_value import MultiValueOp
from kubeq.query._operators._value_ops.op_value import ValueOp


class HasNot(ValueOp[set[str], set[str]], NegatedOp[set[str]], value_type=set[str]):
    @property
    @override
    def positive(self) -> Op[set[str]]:
        return Has(self.value)
