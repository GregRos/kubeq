from kubeq.operators.value_ops.op_not_glob import NotGlobOp
from kubeq.operators.value_ops.op_value import ValueOp


import re


class NotRegexOp(ValueOp, value_type=str):
    original: NotGlobOp | None = None

    def __call__(self, what: str) -> bool:
        return not bool(re.match(self.value, what))

    def to_normalized(self):
        return self
