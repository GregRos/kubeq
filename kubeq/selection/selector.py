from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import op_Any
from kubeq.selection.formula import ApiObjectFilter
from kubeq.attrs import attr_Any

from kr8s.objects import APIObject


from dataclasses import dataclass


@dataclass
class Selector[O: op_Any = op_Any](ApiObjectFilter):
    attr: attr_Any
    operator: O

    def __call__(self, object: APIObject) -> bool:
        return self.operator(self.attr.get(object))
