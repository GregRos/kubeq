from kubeq.operators.value_ops.op_not_in import op_NotIn
from kubeq.operators.value_ops.op_value import op_ValueOp


class op_NotEq(op_ValueOp[str], value_type=str):

    def __call__(self, what: str) -> bool:
        return what != self.value

    def normalize(self) -> "op_NotIn":
        return op_NotIn({self.value}, original=self)
