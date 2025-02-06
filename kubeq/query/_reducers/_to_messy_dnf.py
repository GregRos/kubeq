from itertools import product
from typing import Iterable
from kubeq.query._operators import *
from kubeq.query._reducers._base_reducer import BaseReducer


class To_Messy_Dnf(BaseReducer):

    def _pair_reduce(self, a: Or, b: Or):
        x = [And([x, y]) for x, y in product(a.operands, b.operands)]
        if len(x) > 1:
            self.increment()
        return Or(x)

    def _and_reduce(self, op: And):
        kids = list(op.operands)
        last = self.reduce(kids[0])
        for kid in kids[1:]:
            reduced_kid = self.reduce(kid)
            last = self._pair_reduce(last, reduced_kid)
        return last

    def reduce(self, op: Op) -> Or:
        match op:
            case Or(kids):
                reduced_kids = [self.reduce(kid) for kid in kids]
                return Or(reduced_kids)
            case And(kids):
                return self._and_reduce(op)
            case _:
                return Or.of(op)


def get_dnf_reduction_count(op: Op) -> int:
    reducer = To_Messy_Dnf()
    reducer.reduce(op)
    return reducer.reductions


def assert_dnf(s: Op):
    count = get_dnf_reduction_count(s)
    assert count == 0, f"DNF reduction count is {count}, expected 0"
