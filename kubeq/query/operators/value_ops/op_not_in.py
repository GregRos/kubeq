from typing import overload
from kubeq.query.operators.op_base import Op
from kubeq.query.operators.value_ops.op_multi_value import MultiValueOp
from kubeq.query.operators.value_ops.op_value import ValueOp


class NotIn(MultiValueOp, value_type=set[str]):

    def __call__(self, what: str) -> bool:
        return what not in self.value
