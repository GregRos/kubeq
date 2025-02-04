from kubeq.operators.value_ops.op_glob import GlobOp
from kubeq.operators.value_ops.op_value import ValueOp


import re


class RegexOp(ValueOp, value_type=str):
    original: GlobOp | None = None

    def __call__(self, what: str) -> bool:
        return bool(re.match(self.value, what))

    def to_normalized(self):
        return self
