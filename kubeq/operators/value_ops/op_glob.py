from kubeq.operators.value_ops.op_value import ValueOp


import fnmatch


class GlobOp(ValueOp, value_type=str):

    def __call__(self, what: str) -> bool:
        return fnmatch.fnmatch(what, self.value)
