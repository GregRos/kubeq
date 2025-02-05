from typing import ReadOnly
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import op_Any
from kubeq import attr

from kr8s.objects import APIObject


from dataclasses import dataclass


@dataclass
class Selector:
    attr: attr.Any
    operator: op_Any

    def __call__(self, object: APIObject) -> bool:
        return self.operator(self.attr.get(object))

    def with_op(self, operator: op_Any) -> "Selector":
        return Selector(self.attr, operator)
