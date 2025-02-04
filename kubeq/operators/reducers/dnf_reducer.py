from itertools import product
from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import Op
from kubeq.operators.reducers.base_reducer import BaseReducer


class DnfReducer(BaseReducer):

    def _pair_reduce(self, a: op_Or, b: op_Or):
        self.increment()
        return op_Or(op_And([x, y]) for x, y in product(a.operands, b.operands))

    def _and_reduce(self, op: op_And):
        kids = list(op.operands)
        last = self.reduce(kids[0])
        for kid in kids[1:]:
            reduced_kid = self.reduce(kid)
            last = self._pair_reduce(last, reduced_kid)
        return last

    def reduce(self, op: Op) -> op_Or:
        match op:
            case op_Or(kids):
                reduced_kids = [self.reduce(kid) for kid in kids]
                return op_Or(reduced_kids)
            case op_And(kids):
                return self._and_reduce(op)
            case _:
                return op_Or.of(op)
