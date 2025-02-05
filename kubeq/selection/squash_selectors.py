from itertools import groupby
import selectors
from typing import Iterable

from kubeq import attr
from kubeq.operators.boolean.op_and import op_And
from kubeq.selection.to_simplified_dnf import to_simplified_dnf
from kubeq.selection.selector import Selector


def squash_simplify_selectors(
    selectors: Iterable[Selector],
) -> dict[attr.Any, Selector]:
    grouped = groupby(selectors, lambda x: x.attr)
    d = {}
    for attr, group in grouped:
        all_operators = [sel.operator for sel in group]
        anded = op_And(all_operators)
        simplified = to_simplified_dnf(Selector(attr, anded))
        d[attr] = simplified
    return d
