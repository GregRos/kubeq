from itertools import groupby
from typing import Iterable, Mapping

from kubeq.query._attr.kind import Kind
from kubeq.query._selection._instance_selector import InstanceSelector
from kubeq.query._selection._kind_selector import KindSelector
from kubeq.query._selection._selector import Selector
from .. import _attr as attrs
from .. import _operators as oprs


type SelectorSquash = Mapping[attrs.Any, Selector]
type SquashedSelectors = Mapping[type, SelectorSquash]


def squash_selectors(
    selectors: Iterable[Selector],
) -> SquashedSelectors:
    grouped = groupby(selectors, lambda x: x.attr)
    dd = dict[type, dict[attrs.Any, Selector]]()
    dd.setdefault(attrs.Label, dict())
    dd.setdefault(attrs.Field, dict())
    dd.setdefault(attrs.Kind, dict())
    for attr, group in grouped:
        all_operators = [sel.operator for sel in group]
        anded = oprs.And(all_operators)
        ops = dd.setdefault(type(attr), dict())
        match attr:
            case Kind():
                ops[attr] = KindSelector(attr, anded)
            case _:
                ops[attr] = InstanceSelector(attr, anded)
    return dd
