from abc import ABC

from kubeq.operators.op_base import op_Any
from kubeq.attrs import attr_Any


class BaseReducer(ABC):
    reductions = 0

    def __init__(self, attr: attr_Any):
        self.attr = attr

    def increment(self):
        self.reductions += 1

    def decrement(self):
        self.reductions -= 1

    def reduce(self, op: op_Any) -> op_Any: ...
