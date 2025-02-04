from kubeq.operators.boolean.op_and import And
from kubeq.operators.boolean.op_or import Or
from kubeq.operators.boolean.simplify import simplify_deep
from kubeq.operators.op_base import Op


from itertools import product


def _to_dnf(op: Op) -> Or:
    if not isinstance(op, Or) and not isinstance(op, And):
        return Or.of(op)
    kids = list(op.kids)
    last = _to_dnf(kids[0])
    for kid in kids[1:]:
        normal_kid = _to_dnf(kid)
        last = Or(And([x, y]) for x, y in product(last.kids, normal_kid.kids))
    return last


def to_simplified_dnf(op: Op) -> Or:
    x = simplify_deep(_to_dnf(op))
    match x:
        case Or():
            return x
        case _:
            return Or({x})
