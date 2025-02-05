from kubeq.operators.op_base import op_Any
from kubeq.operators.value_ops.op_not_glob import op_NotGlob
from kubeq.operators.value_ops.op_value import op_ValueOp


import re


class op_NotRegex(op_ValueOp[str], value_type=str):
    original: op_NotGlob | None = None

    def __call__(self, what: str) -> bool:
        return not bool(re.match(self.value, what))

    def normalize(self) -> "op_Any":
        return self
