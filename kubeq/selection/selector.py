from itertools import groupby
from typing import Protocol
from kr8s.objects import APIObject


from dataclasses import dataclass
from typeguard import check_type

from kubeq.attrs.attrs import Field, Kind, Label
from kubeq.operators.boolean_ops import And
from kubeq.operators.core import Op

type ApiAttr = Label | Field

type Attr = Label | Field | Kind


class ApiObjectFilter(Protocol):
    def __call__(self, object: APIObject) -> bool: ...


@dataclass
class Selector(ApiObjectFilter):
    attr: Attr
    operator: And

    def with_op(self, operator: And) -> "Selector":
        return Selector(self.attr, operator)

    @property
    def is_field(self):
        return isinstance(self.attr, Field)

    @property
    def is_label(self):
        return isinstance(self.attr, Label)

    def __call__(self, object: APIObject) -> bool:
        return self.operator(self.attr.get(object))


def and_selectors(selectors: list[Selector]) -> Selector:
    grouped = groupby(selectors, lambda s: s.attr)
