from kubeq.operators.value_ops.op_in import op_In
from kubeq.operators.value_ops.op_value import op_ValueOp


class op_Eq(op_ValueOp[str], value_type=str):

    def __call__(self, what: str) -> bool:
        return what == self.value

    def normalize(self) -> "op_In":
        return op_In({self.value}, original=self)
