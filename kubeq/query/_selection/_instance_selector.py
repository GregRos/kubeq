from kubeq.query import _operators as oprs
from kubeq.query._attr.field import Field
from kubeq.query._attr.label import Label


from dataclasses import dataclass


@dataclass
class InstanceSelector:
    attr: Field | Label
    operator: oprs.Op

    def __call__(self, object: object) -> bool:
        return self.operator(self.attr.get(object))

    def with_op(self, operator: oprs.Op) -> "InstanceSelector":
        return InstanceSelector(self.attr, operator)
