from kubeq.operators.value_ops.op_glob import op_Glob
from kubeq.operators.value_ops.op_value import op_ValueOp


import re


class op_Regex(op_ValueOp[str], value_type=str):
    original: op_Glob | None = None

    def __call__(self, what: str) -> bool:
        return bool(re.match(self.value, what))

    def to_normalized(self):
        return self
