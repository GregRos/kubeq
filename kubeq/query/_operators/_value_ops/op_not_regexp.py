from typing import TYPE_CHECKING, override
from kubeq.query._operators._op_base import Op
from kubeq.query._operators._value_ops.negated_op import NegatedOp
from kubeq.query._operators._value_ops.op_regexp import Regex
from kubeq.query._operators._value_ops.op_value import ValueOp

if TYPE_CHECKING:
    from kubeq.query._operators._value_ops.op_not_glob import NotGlob


import re


class NotRegex(ValueOp[str], NegatedOp, value_type=str):
    original: "NotGlob | None" = None

    @property
    @override
    def positive(self) -> ValueOp[str]:
        return self.original.positive if self.original else Regex(self.value)

    def normalize(self) -> "Op":
        return self
