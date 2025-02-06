from kubeq.query.operators._value_ops.op_not_in import NotIn
from kubeq.query.operators._value_ops.op_value import ValueOp


class NotEq(ValueOp[str], value_type=str):

    def __call__(self, what: str) -> bool:
        return what != self.value

    def normalize(self) -> "NotIn":
        return NotIn({self.value}, original=self)
