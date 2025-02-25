from typing import overload
from kubeq.query._operators._op_base import Op
from kubeq.query._operators._value_ops.op_multi_value import MultiValueOp
from kubeq.query._operators._value_ops.op_value import ValueOp
from kubeq.query._operators._value_ops.repr_collection import repr_collection


class In(MultiValueOp, value_type=set[str]):

    def __call__(self, what: str) -> bool:
        return what in self.value

    def __repr__(self) -> str:
        return f"in({", ".join(self.value)})"
