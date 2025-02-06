from itertools import groupby
from typing import Iterable, Mapping, override
from kubeq.query._selection import Selector
import kubeq.query._operators as oprs
import kubeq.query._attr as _attr


class SelectionFormula(Mapping[_attr.Any, oprs.Op]):
    _op_by_attr: dict[_attr.Any, oprs.Op]

    def __init__(self, op_by_attr: dict[_attr.Any, oprs.Op]):
        self.op_by_attr = op_by_attr
        super().__init__()

    @override
    def __getitem__(self, key: _attr.Any) -> oprs.Op:
        return self._op_by_attr[key]

    @staticmethod
    def squash(selectors: Iterable[Selector]):
        grouped = groupby(selectors, lambda x: x.attr)
        d = {}
        for attr, group in grouped:
            all_operators = [sel.operator for sel in group]
            anded = oprs.And(all_operators)
            d[attr] = Selector(attr, anded)
        return SelectionFormula(d)
