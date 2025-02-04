from kubeq.operators.boolean.op_and import And
from kubeq.operators.boolean.op_or import Or
from kubeq.operators.op_base import Op


def simplify_deep(parent: Op) -> Op:

    match parent:
        case And(kids) | Or(kids):
            cls = And if isinstance(parent, And) else Or
            simplified = _simplify_kids(cls, kids)
            if len(simplified) == 1:
                return simplified[0]
            return cls(_simplify_kids(cls, kids))  # type: ignore
        case _:
            return parent


def _simplify_kids[X: And | Or](cls: type[X], kids: set[Op]) -> list[Op]:
    result_kids = []
    for kid in kids:
        simplified_kid = simplify_deep(kid)
        if isinstance(simplified_kid, cls):
            result_kids.extend(simplified_kid.operands)
        else:
            result_kids.append(simplified_kid)
    return result_kids
