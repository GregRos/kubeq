from kubeq.operators.op_base import Op
from kubeq.operators.value_ops.op_not_glob import NotGlob
from kubeq.operators.value_ops.op_value import ValueOp


import re


class NotRegex(ValueOp[str], value_type=str):
    original: NotGlob | None = None

    def __call__(self, what: str) -> bool:
        return not bool(re.match(self.value, what))

    def normalize(self) -> "Op":
        return self
