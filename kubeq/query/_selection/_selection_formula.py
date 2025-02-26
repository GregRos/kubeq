from typing import Any, Mapping
import kubeq.query._attr as attr
import kubeq.query._operators as oprs
from kubeq.query._reductions._base_reduction import BaseReducer


class SelectionFormula:
    def __init__(self, selectors: Mapping[attr.Any, oprs.Op[Any]]):
        self.selectors = selectors

    def reduce(self, r: BaseReducer):
        result = {k: r.reduce(v) for k, v in self.selectors.items()}
        # get rid of always clauses and reduce never clauses
        for k, v in result.items():
            match v:
                case oprs.Always():
                    del result[k]
                case oprs.Never():
                    return SelectionFormula({})

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
