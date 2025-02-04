from itertools import groupby
from typing import Protocol
from kr8s.objects import APIObject


from dataclasses import dataclass
from typeguard import check_type


from kubeq.operators.boolean.op_and import And
from kubeq.operators.boolean.op_or import Or
from kubeq.operators.boolean.to_dnf import to_simplified_dnf
from kubeq.selection.attrs import Attr
from kubeq.selection.selector import Selector


class ApiObjectFilter(Protocol):
    def __call__(self, object: APIObject) -> bool: ...


@dataclass
class SelectionFormula:
    formula: dict[Attr, Or]


def merge_selectors(selectors: list[Selector]):
    grouped = groupby(selectors, lambda s: s.attr)
    formula: dict[Attr, Or] = {}
    for attr, group in grouped:
        group = list(group)
        merged_dnf = to_simplified_dnf(And(s.operator for s in group))
        formula[attr] = merged_dnf
    return SelectionFormula(formula)
