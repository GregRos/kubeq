from itertools import groupby
from typing import Iterable, Mapping, override
from kubeq import attr
from kubeq import operators as oprs
from kubeq.selection.selector import Selector


class SelectionFormula(Mapping[attr.Any, oprs.Op]):
    _op_by_attr: dict[attr.Any, oprs.Op]

    def __init__(self, op_by_attr: dict[attr.Any, oprs.Op]):
        self.op_by_attr = op_by_attr
        super().__init__()

    @override
    def __getitem__(self, key: attr.Any) -> oprs.Op:
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
