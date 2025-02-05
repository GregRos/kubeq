from kubeq.operators.value_ops.op_regexp import op_Regex
from kubeq.operators.value_ops.op_value import op_ValueOp


import fnmatch


class op_Glob(op_ValueOp[str], value_type=str):

    def __call__(self, what: str) -> bool:
        return fnmatch.fnmatch(what, self.value)

    def normalize(self) -> op_Regex:
        return op_Regex(fnmatch.translate(self.value), original=self)
