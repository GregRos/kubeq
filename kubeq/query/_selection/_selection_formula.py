from collections import defaultdict
from itertools import groupby
from typing import Hashable, Iterable, Mapping, override
from kubeq.query._selection import Selector
from kubeq.query import *
from kubeq.utils.dict import keys_of_type


class SelectionFormula(Mapping[attrs.Any, oprs.Op]):

    def __init__(self, selectors: Iterable[Selector]):
        squashed = _squash(selectors)
        self._label_ops = keys_of_type(squashed, attrs.Label)
        self._field_ops = keys_of_type(squashed, attrs.Field)
        self._kind_ops = keys_of_type(squashed, attrs.Kind)
        super().__init__()

    @property
    def label_ops(self):
        return self._label_ops

    @override
    def __getitem__(self, key: attrs.Any) -> oprs.Op:
        match key:
            case attrs.Label():
                return self._label_ops[key]
            case attrs.Field():
                return self._field_ops[key]
            case attrs.Kind():
                return self._kind_ops[key]
            case _:
                raise KeyError(key)


def _squash(
    selectors: Iterable[Selector],
) -> Mapping[type, Mapping[attrs.Any, oprs.Op]]:
    grouped = groupby(selectors, lambda x: x.attr)
    dd = defaultdict(default_factory=lambda: {})
    for attr, group in grouped:
        all_operators = [sel.operator for sel in group]
        anded = oprs.And(all_operators)
        d[attr] = Selector(attr, anded)
    return SelectionFormula(d)
