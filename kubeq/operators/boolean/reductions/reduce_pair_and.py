from kubeq.operators.boolean.boolean_ops import op_Bool
from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.value_ops.op_glob import op_Glob
from kubeq.operators.value_ops.simplify_trivial import simplify_trivial
from kubeq.operators.primitives.op_never import op_Never
from kubeq.operators.value_ops.op_value import op_ValueOp
from ...value_ops.op_regexp import op_Regex
from ...value_ops.op_not_in import op_NotIn
from ...value_ops.op_in import op_In
from ...op_base import Op
from ...value_ops.op_not_regexp import op_NotRegex
from ...primitives.op_always import op_Always
from ...op_leaf import op_LeafOp


def reduce_pair_and(a: Op, b: Op) -> tuple[Op, Op]:
    match a, b:
        case op_And(kids1), op_And(kids2):
            return op_And(kids1 | kids2), op_Always()
        case op_In(v), op_In(u):
            return op_In(v & u), op_Always()
        case op_NotIn(u), op_NotIn(v):
            return op_NotIn(u | v), op_Always()
        case (op_In(v), (op_Regex() | op_Glob()) as r) | (
            (op_Regex() | op_Glob()) as r,
            op_In(v),
        ):
            return op_In({u for u in v if r(u)}), op_Always()
        case (op_In(u), op_NotIn(v)) | (op_NotIn(v), op_In(u)):
            return op_In(u - v), op_Always()
        case a, b:
            return a, b
