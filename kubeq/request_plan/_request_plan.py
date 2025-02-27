from dataclasses import dataclass
from itertools import product
from typing import Iterable, Sequence
from kubeq.entities._resource._resource import KubeResource
from kubeq.request_plan._make_request import create_request
from kubeq.request_plan._separate import separate_formula
from kubeq.request_plan.op_to_str import formula_to_kube_api
from kubeq.selection._selection_formula import SelectionFormula
from kubeq.selection._selector import Selector
import kubeq.query._operators as oprs
import kubeq.query._attr as attr


@dataclass
class QpStats:
    resources: int
    subqueries: int
    requests: int

    def to_dict(self):
        return {
            "resources": self.resources,
            "subqueries": self.subqueries,
            "requests": self.requests,
        }


def trunc(input: Iterable[str], limit: int = 3):
    parts = []
    for i, x in enumerate(input):
        parts.append(x)
        if i >= limit:
            parts.append("...")
            break
    return ", ".join(parts)


class RequestPlan:
    resources: Sequence[KubeResource]
    separated_formulas: Sequence[SelectionFormula]

    def __init__(self, resources: Sequence[KubeResource], formula: SelectionFormula):
        self.resources = resources
        self.separated_formulas = separate_formula(formula)

    @property
    def stats(self):
        return QpStats(
            resources=len(self.resources),
            subqueries=len(self.separated_formulas),
            requests=len(self.resources) * len(self.separated_formulas),
        )

    def to_requests(self):
        return [
            create_request(res, formula)
            for res, formula in product(self.resources, self.separated_formulas)
        ]

    def to_dict_desc(self):
        viz_resources = trunc([f"{x:short}" for x in self.resources], 3)
        subqueries = [x.to_visual_dict() for x in self.separated_formulas]
        return {
            "resources": viz_resources,
            "subqueries": subqueries,
            "stats": self.stats.to_dict(),
        }


"""
QUERY PLAN
args:
    - --kind verbs[ has(delete) ] 
    - --kind version[ =v1 ]
    - --where %app[ in(bar, baz) ]
    - --where %env[ in(prod, dev) ]
    - --where @ns[ in(default, kube-system) ]
parsed:
    kind: 
        verbs: has(delete)
        version: =v1
    instance:
        ~%baz: always~
        %app: in(bar, baz)
        %env: in(prod, dev)
        @namespace: in(default, kube-system)
requests:
    from: Deployment, Pod, ClusterIssuer, ...
    where: 
        - %app: in(bar, baz)
          %env: in(prod, dev)
          @namespace: =default
        - %app: in(bar, baz)
          %env: in(prod, dev)
          @namespace: =kube-system
    total:
        resources: 10
        subqueries: 2
        requests: 20
limits:
    scanned: 500 (default)
    subqueries: 100 (default)
    requests: 300 (default)
    
    
    
    
"""
