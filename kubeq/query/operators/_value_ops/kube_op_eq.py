from kubeq.query.operators._boolean.op_and import And
from kubeq.query.operators._op_base import Op
from kubeq.query.operators._value_ops.op_in import In
from kubeq.query.operators._value_ops.op_value import ValueOp


class Eq(ValueOp[str], value_type=str):

    def __call__(self, what: str) -> bool:
        return what == self.value

    def normalize(self) -> "In":
        return In({self.value}, original=self)
