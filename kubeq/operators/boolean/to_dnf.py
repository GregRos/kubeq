from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.boolean.simplify import simplify_singletons
from kubeq.operators.op_base import Op


from itertools import product


def _merge_and(a: op_Or, b: op_Or) -> op_Or:
    return op_Or(op_And([x, y]) for x, y in product(a.operands, b.operands))


def _to_dnf(op: Op) -> op_Or:
    if not isinstance(op, op_Or) and not isinstance(op, op_And):
        return op_Or.of(op)
    kids = list(op.operands)
    last = _to_dnf(kids[0])
    for kid in kids[1:]:
        normal_kid = _to_dnf(kid)
        last = _merge_and(last, normal_kid)
    return last


def to_simplified_dnf(op: Op) -> op_Or:
    x = simplify_singletons(_to_dnf(op))
    match x:
        case op_Or():
            return x
        case _:
            return op_Or({x})
