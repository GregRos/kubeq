from typing import Mapping
import kubeq.query._attr as attr
import kubeq.query._operators as oprs
from kubeq.query._reductions._base_reduction import BaseReducer


class SelectionFormula:
    def __init__(self, selectors: Mapping[attr.Api, oprs.Op]):
        self.selectors = selectors

    def reduce(self, r: BaseReducer):
        return SelectionFormula({k: r.reduce(v) for k, v in self.selectors.items()})

    def __repr__(self):
        clauses = []
        for attr, op in self.selectors.items():
            attr_str = str(attr)
            op_str = str(op)
            clauses.append(f"-s {attr_str}[{op_str}]")
        return "\n".join(clauses)


# -s %Label[=12 & in(1, 2, 3) & glob(a/*) & regex(.*a.*)]
# -s @Field[=12 & in(1, 2, 3) & glob(a/*) & | regex(.*a.*)]
# -s @Field[=12 & in(1, 2, 3) & glob(a/*) & regex(.*a.*) & ]

# @spec.replicas
# @spec.template.spec.containers[0].image
#
