from kubeq.operators.boolean.op_or import op_Or
from kubeq.selection.formula import ApiObjectFilter


from kr8s.objects import APIObject


from dataclasses import dataclass


@dataclass
class Selector(ApiObjectFilter):
    attr: Attr
    operator: op_Or

    def __call__(self, object: APIObject) -> bool:
        return self.operator(self.attr.get(object))
