from ast import Or
from itertools import groupby
from typing import Protocol
from kr8s.objects import APIObject


from dataclasses import dataclass
from typeguard import check_type


from kubeq.operators.boolean.op_and import And
from kubeq.operators.boolean.op_or import Or
from kubeq.operators.boolean.to_dnf import to_simplified_dnf
from kubeq.selection.attrs.field import Field
from kubeq.selection.attrs.kind import Kind
from kubeq.selection.attrs.label import Label

type ApiAttr = Label | Field

type Attr = Label | Field | Kind


class ApiObjectFilter(Protocol):
    def __call__(self, object: APIObject) -> bool: ...


@dataclass
class Selector(ApiObjectFilter):
    attr: Attr
    operator: Or

    def with_op(self, operator: Or) -> "Selector":
        return Selector(self.attr, operator)

    @property
    def is_field(self):
        return isinstance(self.attr, Field)

    @property
    def is_label(self):
        return isinstance(self.attr, Label)

    def __call__(self, object: APIObject) -> bool:
        return self.operator(self.attr.get(object))


def merge_selectors(selectors: list[Selector]) -> list[Selector]:
    grouped = groupby(selectors, lambda s: s.attr)
    results: list[Selector] = []
    for attr, group in grouped:
        group = list(group)
        merged_dnf = to_simplified_dnf(And([s.operator for s in group]))
        results.append(Selector(attr, merged_dnf))
    return results
