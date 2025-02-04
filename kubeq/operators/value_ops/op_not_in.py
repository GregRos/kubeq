from kubeq.operators.value_ops.op_value import ValueOp


class NotInOp(ValueOp, value_type=set[str]):

    def __call__(self, what: str) -> bool:
        return what not in self.value
