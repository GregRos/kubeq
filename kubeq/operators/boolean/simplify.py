from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import Op


def simplify_deep(parent: Op) -> Op:

    match parent:
        case op_And(kids) | op_Or(kids):
            cls = op_And if isinstance(parent, op_And) else op_Or
            simplified = _simplify_kids(cls, kids)
            if len(simplified) == 1:
                return simplified[0]
            return cls(_simplify_kids(cls, kids))  # type: ignore
        case _:
            return parent


def _simplify_kids[X: op_And | op_Or](cls: type[X], kids: set[Op]) -> list[Op]:
    result_kids = []
    for kid in kids:
        simplified_kid = simplify_deep(kid)
        if isinstance(simplified_kid, cls):
            result_kids.extend(simplified_kid.operands)
        else:
            result_kids.append(simplified_kid)
    return result_kids
