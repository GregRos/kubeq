from itertools import groupby
from typing import Protocol
from kr8s.objects import APIObject


from dataclasses import dataclass
from typeguard import check_type


from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.boolean.op_or import op_Or
from kubeq.selection.attrs import Attr
from kubeq.selection.selector import Selector


class ApiObjectFilter(Protocol):
    def __call__(self, object: APIObject) -> bool: ...


@dataclass
class SelectionFormula:
    formula: dict[Attr, op_Or]


def merge_selectors(selectors: list[Selector]):
    grouped = groupby(selectors, lambda s: s.attr)
    formula: dict[Attr, op_Or] = {}
    for attr, group in grouped:
        group = list(group)

        formula[attr] = merged_dnf
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   return SelectionFormula(formula)
