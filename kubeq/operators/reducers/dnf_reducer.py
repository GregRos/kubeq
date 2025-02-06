from itertools import product
from kubeq.operators.boolean.op_and import And
from kubeq.operators.boolean.op_or import Or
from kubeq.operators.op_base import Op
from kubeq.operators.reducers.base_reducer import BaseReducer
from kubeq.selection.selector import Selector


class DnfReducer(BaseReducer):

    def _pair_reduce(self, a: Or, b: Or):
        self.increment()
        return Or(And([x, y]) for x, y in product(a.operands, b.operands))

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
    reducer = DnfReducer()
    reducer.reduce(op)
    return reducer.reductions


def assert_dnf(s: Op):
    count = get_dnf_reduction_count(s)
    assert count == 0, f"DNF reduction count is {count}, expected 0"
