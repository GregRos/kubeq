from kubeq.operators.value_ops.op_value import op_ValueOp


import fnmatch


class op_NotGlob(op_ValueOp, value_type=str):
    def __call__(self, what: str) -> bool:
        return not fnmatch.fnmatch(what, self.value)
