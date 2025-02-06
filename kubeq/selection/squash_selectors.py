from itertools import groupby
import selectors
from typing import Iterable

from kubeq import attr
import kubeq.operators as oprs
from kubeq.selection.to_simplified_dnf import to_simplified_dnf
from kubeq.selection.selector import Selector


def squash_simplify_selectors(
    selectors: Iterable[Selector],
) -> dict[attr.Any, Selector]:
    grouped = groupby(selectors, lambda x: x.attr)
    d = {}
    for attr, group in grouped:
        all_operators = [sel.operator for sel in group]
        anded = oprs.And(all_operators)
        simplified = to_simplified_dnf(anded)
        d[attr] = Selector(attr, simplified)
    return d
