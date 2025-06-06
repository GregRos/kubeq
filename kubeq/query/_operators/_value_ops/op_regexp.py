from kubeq.query._operators._op_base import Op
from kubeq.query._operators._value_ops.op_glob import Glob
from kubeq.query._operators._value_ops.op_value import ValueOp


import re


class Regex(ValueOp[str], value_type=str):
    original: Glob | None = None

    def __call__(self, what: str) -> bool:
        return bool(re.match(self.value, what))

    def normalize(self) -> "Op":
        return self

    def __repr__(self) -> str:
        return repr(self.original) if self.original else f"regex({self.value})"
