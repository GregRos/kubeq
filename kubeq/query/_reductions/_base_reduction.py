from abc import ABC
from re import S

from kubeq.query._operators import *


class BaseReducer(ABC):
    reductions = 0

    def increment(self):
        self.reductions += 1

    def decrement(self):
        self.reductions -= 1

    def reset(self):
        self.reductions = 0

    def reduce(self, op: Op) -> Op: ...


class ComboReduction(BaseReducer):
    def __init__(self, *reducers: BaseReducer):
        self.reducers = reducers

    def reduce(self, op: Op) -> Op:
        for reduction in self.reducers:
            op = reduction.reduce(op)
            self.reductions += reduction.reductions
        return op
