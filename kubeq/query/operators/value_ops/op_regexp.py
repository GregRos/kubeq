from kubeq.operators.op_base import Op
from kubeq.operators.value_ops.op_glob import Glob
from kubeq.operators.value_ops.op_value import ValueOp


import re


class Regex(ValueOp[str], value_type=str):
    original: Glob | None = None

    def __call__(self, what: str) -> bool:
        return bool(re.match(self.value, what))

    def normalize(self) -> "Op":
        return self
