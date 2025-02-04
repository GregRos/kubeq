from kubeq.operators.value_ops.op_value import op_ValueOp


class kube_op_Eq(op_ValueOp[str], value_type=str):

    def __call__(self, what: str) -> bool:
        return what == self.value
