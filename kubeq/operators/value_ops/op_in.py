from kubeq.operators.value_ops.op_value import ValueOp


class InOp(ValueOp, value_type=set[str]):

    def __call__(self, what: str) -> bool:
        return what in self.value
