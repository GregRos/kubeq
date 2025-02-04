from kubeq.operators.boolean.boolean_ops import BooleanOp
from kubeq.operators.primitives.op_never import op_Never
from kubeq.operators.value_ops.op_value import op_ValueOp
from .value_ops.op_regexp import op_Regex
from .value_ops.op_not_in import op_NotIn
from .value_ops.op_in import op_In
from .op_base import Op
from .value_ops.op_not_regexp import op_NotRegex
from .primitives.op_always import op_Always
from .op_leaf import op_LeafOp


def _reduce_pair(a: op_LeafOp, b: op_LeafOp) -> tuple[op_LeafOp, op_LeafOp]:
    match a, b:
        case op_In(v), op_In(u):
            return op_In(v & u), op_Always()
        case op_In(v), op_Regex(x) as r:
            return op_In({u for u in v if r(u)}), op_Always()
        case op_In(u), op_NotIn(v):
            return op_In(u - v), op_Always()
        case op_In(u), op_NotRegex(x) as r:
            return op_In({v for v in u if not r(v)}), op_Always()
        case op_NotIn(u), op_NotIn(v):
            return op_NotIn(u | v), op_Always()
        case a, b:
            return a, b


def _convert_form(op: Op):
    match op:
        case op_In({}):
            return op_Never()
        case op_NotIn({}):
            return op_Always()
        case _:
            return op


def _simplify_non_value(ops: list[Op]) -> list[Op]:
    ops = [_convert_form(op) for op in ops]
    if op_Never() in ops:
        return [op_Never()]
    no_always = [op for op in ops if not isinstance(op, op_Always)]
    if len(no_always) == 0:
        return [op_Always()]
    return no_always


def reduce_ops_list(ops: list[Op]) -> list[Op]:

    i = 0
    j = 1
    for i in range(len(ops)):
        for j in range(i + 1, len(ops)):
            ops[i], ops[j] = _reduce_pair(ops[i], ops[j])

    return _simplify_non_value(ops)
