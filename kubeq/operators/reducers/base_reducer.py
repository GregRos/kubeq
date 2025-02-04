from abc import ABC

from kubeq.operators.op_base import Op


class BaseReducer(ABC):
    reductions = 0

    def increment(self):
        self.reductions += 1

    def decrement(self):
        self.reductions -= 1

    def reduce(self, op: Op) -> Op: ...
