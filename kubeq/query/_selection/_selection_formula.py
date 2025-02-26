from typing import Any, Callable, Mapping
import kubeq.query._attr as attr
import kubeq.query._operators as oprs
from kubeq.query._reductions._base_reduction import BaseReducer


class SelectionFormula(Mapping[attr.Any, oprs.Op[Any]]):
    def __init__(self, selectors: Mapping[attr.Any, oprs.Op[Any]]):
        self.selectors = selectors

    def __iter__(self):
        return iter(self.selectors)

    def set(self, attr: attr.Any, op: oprs.Op[Any]):
        return SelectionFormula({**self.selectors, attr: op})

    def __getitem__(self, key):
        return self.selectors[key]

    def __len__(self):
        return len(self.selectors)

    def __bool__(self):
        return self.is_empty

    def reduce(
        self, make_reducer: Callable[[attr.Any], BaseReducer]
    ) -> "SelectionFormula":
        d = {}
        for attr, op in self.selectors.items():
            reducer = make_reducer(attr)
            op = reducer.reduce(op)
            d[attr] = op
        return SelectionFormula(d)

    @property
    def is_empty(self):
        return not self.selectors

    def __repr__(self):
        clauses = []
        for attr, op in self.selectors.items():
            attr_str = str(attr)
            op_str = str(op)
            clauses.append(f"-s {attr_str}[{op_str}]")
        return "\n".join(clauses)

    def __call__(self, x: object):
        return all(op(attr.get(x)) for attr, op in self.selectors.items())

    def only_of(self, t: type[attr.Any]):
        filtered = {
            attr: op for attr, op in self.selectors.items() if isinstance(attr, t)
        }
        return SelectionFormula(filtered)


# -k verbs[has(delete) & !has(create)]
# -s %Label[=12 & in(1, 2, 3) & glob(a/*) & regex(.*a.*)]
# -s @Field[=12 & in(1, 2, 3) & glob(a/*) & | regex(.*a.*)]
# -s @Field[=12 & in(1, 2, 3) & glob(a/*) & regex(.*a.*) & ]

# @spec.replicas
# @spec.template.spec.containers[0].image
#
