from kubeq.query.operators._op_base import Op
from kubeq.query.operators._value_ops.op_not_regexp import NotRegex
from kubeq.query.operators._value_ops.op_value import ValueOp


import fnmatch


class NotGlob(ValueOp[str], value_type=str):
    def __call__(self, what: str) -> bool:
        return not fnmatch.fnmatch(what, self.value)

    def normalize(self) -> Op:
        return NotRegex(fnmatch.translate(self.value), original=self)
