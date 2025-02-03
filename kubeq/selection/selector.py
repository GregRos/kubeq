from typing import Protocol
from kr8s.objects import APIObject


from dataclasses import dataclass
from typeguard import check_type

from kubeq.attrs.attrs import Field, Kind, Label
from kubeq.operators.operators import AnyOp, ApiOp, EqOp

type ApiAttr = Label | Field

type Attr = Label | Field | Kind


class ApiObjectFilter(Protocol):
    def __call__(self, object: APIObject) -> bool: ...


@dataclass
class Selector[E: Attr = Attr, O: AnyOp = AnyOp](ApiObjectFilter):
    attr: E
    operator: O

    @property
    def is_field(self):
        return isinstance(self.attr, Field)

    def is_compatible_with(self, other: "Selector") -> bool:
        if self.attr == other.attr:
            match self.operator, other.operator:
                case EqOp(x), EqOp(y):
                    return x == y

    @property
    def is_label(self):
        return isinstance(self.attr, Label)

    def __call__(self, object: APIObject) -> bool:
        return self.operator(self.attr.get(object))


def simplify_selectors(selectors: list[Selector]):

    grouped_by_attr = {
        attr: [selector for selector in selectors if selector.attr == attr]
        for attr in set(selector.attr for selector in selectors)
    }

    for attr, selectors in grouped_by_attr.items():
        eq_selectors = [
            selector for selector in selectors if isinstance(selector.operator, EqOp)
        ]
        if len(eq_selectors) > 1:
            grouped_by_attr[attr] = [
                Selector(attr, EqOp(eq_selectors[0].operator.value))
            ]


type ApiSelector = Selector[ApiAttr, ApiOp]
type KindSelector = Selector[Kind, AnyOp]
