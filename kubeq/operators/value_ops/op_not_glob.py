from kubeq.operators.op_base import op_Any
from kubeq.operators.value_ops.op_not_regexp import op_NotRegex
from kubeq.operators.value_ops.op_value import op_ValueOp


import fnmatch


class op_NotGlob(op_ValueOp[str], value_type=str):
    def __call__(self, what: str) -> bool:
        return not fnmatch.fnmatch(what, self.value)

    def normalize(self) -> op_Any:
        return op_NotRegex(fnmatch.translate(self.value), original=self)
