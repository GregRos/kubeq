from kubeq.operators.value_ops.op_value import ValueOp


import fnmatch


class NotGlobOp(ValueOp, value_type=str):
    def __call__(self, what: str) -> bool:
        return not fnmatch.fnmatch(what, self.value)
