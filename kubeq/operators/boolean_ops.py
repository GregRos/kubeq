from itertools import product
from typing import Callable, Iterable
from kubeq.operators.core import Op


class Or(Op):
    __match_args__ = ("kids",)

    kids: set[Op]

    @staticmethod
    def of(*operators: Op) -> "Or":
        return Or(set(operators))

    def __init__(self, operators: Iterable[Op]) -> None:
        self.kids = set(operators)

    def __call__(self, what: str) -> bool:
        return any(op(what) for op in self.kids)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.kids == other.kids

    def __hash__(self) -> int:
        return hash(self.kids)

    def __iter__(self):
        return iter(self.kids)

    def map_leaves(self, projection: Callable[[Op], Iterable[Op]]):
        return And({op for op in self.kids if not projection(op)})

    def map_kids(self, projection: Callable[[Op], Op]):
        return Or({projection(op) for op in self.kids})


class And(Op):
    __match_args__ = ("kids",)
    kids: set[Op]

    @staticmethod
    def of(*operators: Op) -> "And":
        return And(set(operators))

    def __init__(self, operators: Iterable[Op]) -> None:
        self.kids = {
            x for op in operators for x in (op.kids if isinstance(op, And) else [op])
        }

    def __iter__(self):
        return iter(self.kids)

    def __call__(self, what: str) -> bool:
        return all(op(what) for op in self.kids)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.kids == other.kids

    def __hash__(self) -> int:
        return hash(self.kids)

    def meap_leaves(self, projection: Callable[[Op], Iterable[Op]]):
        return And({op for op in self.kids if not projection(op)})

    def map_kids(self, projection: Callable[[Op], Op]):
        return And({projection(op) for op in self.kids})


type BooleanOp = Or | And


def to_normal_form(op: Op) -> Or:
    if not isinstance(op, Or) and not isinstance(op, And):
        return Or.of(op)
    kids = list(op.kids)
    last = to_normal_form(kids[0])
    for kid in kids[1:]:
        normal_kid = to_normal_form(kid)
        last = Or(And([x, y]) for x, y in product(last.kids, normal_kid.kids))
    return last


def to_simplified_normal_form(op: Op) -> Or:
    x = simplify_deep(to_normal_form(op))
    match x:
        case Or():
            return x
        case _:
            return Or({x})


def simplify_kids[X: And | Or](cls: type[X], kids: set[Op]) -> list[Op]:
    result_kids = []
    for kid in kids:
        simplified_kid = simplify_deep(kid)
        if isinstance(simplified_kid, cls):
            result_kids.extend(simplified_kid.kids)
        else:
            result_kids.append(simplified_kid)
    return result_kids


def simplify_deep(parent: Op) -> Op:

    match parent:
        case And(kids) | Or(kids):
            cls = And if isinstance(parent, And) else Or
            simplified = simplify_kids(cls, kids)
            if len(simplified) == 1:
                return simplified[0]
            return cls(simplify_kids(cls, kids))  # type: ignore
        case _:
            return parent
