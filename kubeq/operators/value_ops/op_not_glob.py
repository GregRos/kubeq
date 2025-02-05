from kubeq.operators.op_base import Op
from kubeq.operators.value_ops.op_not_regexp import NotRegex
from kubeq.operators.value_ops.op_value import ValueOp


import fnmatch


class NotGlob(ValueOp[str], value_type=str):
    def __call__(self, what: str) -> bool:
        return not fnmatch.fnmatch(what, self.value)

    def normalize(self) -> Op:
        return NotRegex(fnmatch.translate(self.value), original=self)
