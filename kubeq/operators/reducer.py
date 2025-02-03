from kubeq.operators.boolean_ops import BooleanOp
from .core import Op
from .kubeq_ops import InOp, NotInOp, RegexOp, NotRegexOp
from .primitive_ops import Always


def op_intersection(a: Op, b: Op) -> tuple[Op, Op]:
    match a, b:
        case InOp(v), InOp(u):
            return InOp(v & u), Always()
        case InOp(v), RegexOp(x) as r:
            return InOp({u for u in v if r(u)}), Always()
        case InOp(u), NotInOp(v):
            return InOp(u - v), Always()
        case InOp(u), NotRegexOp(x) as r:
            return InOp({v for v in u if not r(v)}), Always()
        case NotInOp(u), NotInOp(v):
            return NotInOp(u | v), Always()
        case a, b:
            return a, b


def intersect_ops_list(ops: list[Op]) -> list[Op]:

    i = 0
    j = 1
    for i in range(len(ops)):
        for j in range(i + 1, len(ops)):
            ops[i], ops[j] = op_intersection(ops[i], ops[j])

    return [*filter(lambda x: not isinstance(x, Always), ops)]
