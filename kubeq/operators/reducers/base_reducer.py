from abc import ABC

from kubeq.operators.op_base import Op
from kubeq import attr


class BaseReducer(ABC):
    reductions = 0

    def __init__(self, attr: attr.Any):
        self.attr = attr

    def increment(self):
        self.reductions += 1

    def decrement(self):
        self.reductions -= 1

    def reduce(self, op: Op) -> Op: ...
