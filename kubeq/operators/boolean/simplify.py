from kubeq.operators.boolean.boolean_ops import op_Bool
from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import Op
from kubeq.operators.primitives.op_always import op_Always
from kubeq.operators.primitives.op_never import op_Never
from kubeq.operators.value_ops.op_in import op_In
from kubeq.operators.value_ops.op_not_in import op_NotIn


def simplify_singletons(parent: Op) -> Op:

    match parent:
        case op_Bool([one]):
            return one
        case op_And([]):
            return op_Always()
        case op_Or([]):
            return op_Never()
        case (op_Or(kids) | op_And(kids)) as r:
            return r.__class__(simplify_singletons(kid) for kid in kids)
        case op_In([]):
            return op_Never()
        case op_NotIn([]):
            return op_Always()
        case _:
            return parent
