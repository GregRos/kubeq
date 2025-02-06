from typing import overload
from kubeq.operators.op_base import Op
from kubeq.operators.value_ops.op_multi_value import MultiValueOp
from kubeq.operators.value_ops.op_value import ValueOp
from kubeq.operators.value_ops.repr_collection import repr_collection


class In(MultiValueOp, value_type=set[str]):

    def __call__(self, what: str) -> bool:
        return what in self.value
