from kubeq.operators.boolean.op_or import Or
from kubeq.selection.attrs import Attr
from kubeq.selection.formula import ApiObjectFilter


from kr8s.objects import APIObject


from dataclasses import dataclass


@dataclass
class Selector(ApiObjectFilter):
    attr: Attr
    operator: Or

    def __call__(self, object: APIObject) -> bool:
        return self.operator(self.attr.get(object))
