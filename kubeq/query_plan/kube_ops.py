from kubeq.operators import AnyOp
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.value_ops.op_not_in import op_NotIn
from kubeq.operators.value_ops.op_value import op_ValueOp
from kubeq.selection.selector import Selector


class op_Eq(op_ValueOp, value_type=str):

    def __call__(self, what: str) -> bool:
        return what == self.value


class op_NotEq(op_ValueOp, value_type=str):

    def __call__(self, what: str) -> bool:
        return what != self.value


type KubeOp = op_Eq | op_NotEq
