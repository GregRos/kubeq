from typing import TYPE_CHECKING
from kubeq.query.operators.op_base import Op
from kubeq.query.operators.value_ops.op_value import ValueOp

if TYPE_CHECKING:
    from kubeq.query.operators.value_ops.op_not_glob import NotGlob


import re


class NotRegex(ValueOp[str], value_type=str):
    original: "NotGlob | None" = None

    def __call__(self, what: str) -> bool:
        return not bool(re.match(self.value, what))

    def normalize(self) -> "Op":
        return self
