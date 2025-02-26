from dataclasses import dataclass
from itertools import product
from typing import Sequence
from kubeq.entities._resource._resource import KubeResource
from kubeq.query_plan._make_request import create_request
from kubeq.query_plan._separate import separate_formula
from kubeq.query_plan.op_to_str import formula_to_kube_api
from kubeq.selection._selection_formula import SelectionFormula
from kubeq.selection._selector import Selector
import kubeq.query._operators as oprs
import kubeq.query._attr as attr


@dataclass
class QpStats:
    count_resources: int
    count_subqeries: int
    total_requests: int


class QueryPlan:
    resources: Sequence[KubeResource]
    separated_formulas: Sequence[SelectionFormula]

    def __init__(self, resources: Sequence[KubeResource], formula: SelectionFormula):
        self.resources = resources
        self.separated_formulas = separate_formula(formula)

    @property
    def stats(self):
        return QpStats(
            count_resources=len(self.resources),
            count_subqeries=len(self.separated_formulas),
            total_requests=len(self.resources) * len(self.separated_formulas),
        )

    def to_requests(self):
        return [
            create_request(res, formula)
            for res, formula in product(self.resources, self.separated_formulas)
        ]


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
