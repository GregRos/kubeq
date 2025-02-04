from kubeq.operators.value_ops.op_value import op_ValueOp


class op_In(op_ValueOp, value_type=set[str]):

    def __call__(self, what: str) -> bool:
        return what in self.value
