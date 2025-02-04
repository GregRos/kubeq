from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import Op
from kubeq.operators.primitives.op_always import op_Always
from kubeq.operators.primitives.op_never import op_Never
from kubeq.operators.value_ops.op_in import op_In
from kubeq.operators.value_ops.op_not_glob import op_NotGlob
from kubeq.operators.value_ops.op_not_in import op_NotIn
from kubeq.operators.value_ops.op_not_regexp import op_NotRegex
from kubeq.operators.value_ops.op_regexp import op_Regex
from kubeq.operators.op_leaf import op_LeafOp


def reduce_pair_or(a: Op, b: Op) -> tuple[Op, Op]:
    match a, b:
        case op_Or(kids1), op_Or(kids2):
            return op_Or(kids1 | kids2), op_Never()
        case op_In(v), op_In(u):
            return op_In(v | u), op_Never()
        case op_NotIn(u), op_NotIn(v):
            return op_NotIn(u & v), op_Never()
        case (op_NotIn(u), op_In(v)) | (op_In(v), op_NotIn(u)):
            return op_NotIn(u - v), op_Never()
        case (op_NotIn(u), (op_NotRegex() | op_NotGlob()) as r) | (
            (op_NotRegex() | op_NotGlob()) as r,
            op_NotIn(u),
        ):
            return op_NotIn({v for v in u if not r(v)}), op_Never()

        case a, b:
            return a, b
