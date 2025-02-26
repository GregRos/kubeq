from dataclasses import dataclass
from typing import Self, Sequence
from kubeq.query import _attr
import kubeq.query._operators as oprs


class Selector[A: _attr.Any = _attr.Any]:
    attr: A
    operator: oprs.Op

    def __init__(self, attr: A, operator: oprs.Op):
        self.attr = attr
        self.operator = operator

    @staticmethod
    def empty(attr: A) -> "Selector[A]":
        return Selector(attr, oprs.Always())

    def __call__(self, object: object) -> bool:
        return self.operator(self.attr.get(object))

    def __repr__(self) -> str:
        return f"{self.attr}[{repr(self.operator)}]"

    def and_(self, *ops: oprs.Op) -> Self:
        return self.__class__(self.attr, oprs.And(self.operator, *ops))

    def or_(self, *ops: oprs.Op) -> Self:
        return self.__class__(self.attr, oprs.Or(self.operator, *ops))

    def destructure_or(self) -> "Sequence[Selector[A]]":
        match self.operator:
            case oprs.Or(*ops):
                return [self.__class__(self.attr, op) for op in ops]
            case _:
                return [self]