from kubeq.operators.value_ops.op_value import op_ValueOp


class op_NotIn(op_ValueOp[set[str]], value_type=set[str]):

    def __call__(self, what: str) -> bool:
        return what not in self.value
