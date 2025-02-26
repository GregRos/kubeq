from itertools import groupby, product
from typing import Any, Callable, Iterable, Mapping
import kubeq.query._attr as attr
import kubeq.query._operators as oprs
from kubeq.query._reductions._base_reduction import BaseReducer
from kubeq.selection._instance_selector import InstanceSelector
from kubeq.selection._selector import Selector


class SelectionFormula(Mapping[attr.Any, oprs.Op[Any]]):
    def __init__(self, _formula: Mapping[attr.Any, oprs.Op[Any]]):
        self._formula = _formula

    def __iter__(self):
        return iter(self._formula)

    @staticmethod
    def _make_selector(attrx: attr.Any, op: oprs.Op[Any]) -> Selector:

        match attrx:
            case attr.Kind() as kind:
                return Selector(kind, op)
            case _:
                return Selector(attrx, op)

    @property
    def selectors(self):
        return {self._make_selector(attr, op) for attr, op in self._formula.items()}

    def set(self, attr: attr.Any, op: oprs.Op[Any]):
        return SelectionFormula({**self._formula, attr: op})

    def __getitem__(self, key):
        return self._formula[key]

    def __len__(self):
        return len(self._formula)

    def __bool__(self):
        return self.is_empty

    @staticmethod
    def of_selectors(selectors: Iterable[Selector]):
        grouped_selectors = groupby(selectors, lambda s: s.attr)
        d = {}
        for attr, selectors in grouped_selectors:
            selectors = list(selectors)
            if len(selectors) == 1:
                selector = selectors[0]
                d[attr] = selector.operator
            else:
                d[attr] = oprs.And(*[selector.operator for selector in selectors])
        return SelectionFormula(d)

    def reduce(
        self, make_reducer: Callable[[attr.Any], BaseReducer]
    ) -> "SelectionFormula":
        d = {}
        for attr, op in self._formula.items():
            reducer = make_reducer(attr)
            op = reducer.reduce(op)
            d[attr] = op
        return SelectionFormula(d)

    @property
    def is_empty(self):
        return not self._formula

    def __repr__(self):
        clauses = []
        for attr, op in self._formula.items():
            attr_str = str(attr)
            op_str = str(op)
            clauses.append(f"-s {attr_str}[{op_str}]")
        return "\n".join(clauses)

    def __call__(self, x: object):
        return all(op(attr.get(x)) for attr, op in self._formula.items())

    def only_of(self, t: type[attr.Any]):
        filtered = {
            attr: op for attr, op in self._formula.items() if isinstance(attr, t)
        }
        return SelectionFormula(filtered)


# -k verbs[has(delete) & !has(create)]
# -s %Label[=12 & in(1, 2, 3) & glob(a/*) & regex(.*a.*)]
# -s @Field[=12 & in(1, 2, 3) & glob(a/*) & | regex(.*a.*)]
# -s @Field[=12 & in(1, 2, 3) & glob(a/*) & regex(.*a.*) & ]

# @spec.replicas
# @spec.template.spec.containers[0].image
#
