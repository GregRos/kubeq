from kubeq.operators import AnyOp
from kubeq.operators.boolean.op_or import Or
from kubeq.operators.boolean.op_and import And
from kubeq.operators.value_ops.op_not_in import NotInOp
from kubeq.operators.value_ops.op_value import ValueOp
from kubeq.selection.selector import Selector


class EqOp(ValueOp, value_type=str):

    def __call__(self, what: str) -> bool:
        return what == self.value


class NotEqOp(ValueOp, value_type=str):

    def __call__(self, what: str) -> bool:
        return what != self.value
