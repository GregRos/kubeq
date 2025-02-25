from typing import override
from kubeq.query._operators._op_base import Op
from kubeq.query._operators._value_ops.negated_op import NegatedOp
from kubeq.query._operators._value_ops.op_glob import Glob
from kubeq.query._operators._value_ops.op_not_regexp import NotRegex
from kubeq.query._operators._value_ops.op_value import ValueOp


import fnmatch


class NotGlob(ValueOp[str], NegatedOp, value_type=str):

    @property
    @override
    def positive(self) -> ValueOp[str]:
        return Glob(self.value)

    def normalize(self) -> Op:
        return NotRegex(fnmatch.translate(self.value), original=self)
