from kubeq.operators.op_base import Op
from kubeq.operators.primitives.op_always import op_Always
from kubeq.operators.primitives.op_never import op_Never
from kubeq.operators.value_ops.op_in import op_In
from kubeq.operators.value_ops.op_not_in import op_NotIn


def simplify_trivial(op: Op):
    match op:
        case op_In({}):
            return op_Never()
        case op_NotIn({}):
            return op_Always()
        case _:
            return op
