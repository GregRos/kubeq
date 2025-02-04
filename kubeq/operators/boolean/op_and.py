from kubeq.operators.op_base import Op


from typing import Callable, Iterable


class And(Op):
    __match_args__ = ("kids",)
    operands: set[Op]

    @staticmethod
    def of(*operators: Op) -> "And":
        return And(set(operators))

    def __init__(self, operators: Iterable[Op]) -> None:
        self.operands = {
            x
            for op in operators
            for x in (op.operands if isinstance(op, And) else [op])
        }

    def __iter__(self):
        return iter(self.operands)

    def __call__(self, what: str) -> bool:
        return all(op(what) for op in self.operands)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.operands == other.operands

    def __hash__(self) -> int:
        return hash(self.operands)
