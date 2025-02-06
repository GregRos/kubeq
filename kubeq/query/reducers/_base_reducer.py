from abc import ABC

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
