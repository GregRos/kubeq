from dataclasses import dataclass
from itertools import product
from typing import Sequence
from kubeq.entities._resource._resource import KubeResource
from kubeq.run_query.kube_list_request import KubeListRequest
from kubeq.run_query.op_to_str import formula_to_kube_api
from kubeq.selection._selection_formula import SelectionFormula
from kubeq.selection._selector import Selector
import kubeq.query._operators as oprs
import kubeq.query._attr as attr
def _separate_selector[A: attr.Any](selector: Selector[A]) -> Sequence[Selector[A]]:
    match selector.operator:
        case oprs.Or(*ops):
            return [Selector[A](selector.attr, op) for op in ops]
        case _:
            return [selector]


def _separate_formula(formula: SelectionFormula) -> Sequence[SelectionFormula]:
    destructured = [_separate_selector(selector) for selector in formula.selectors]
    prod = list(product(*destructured))
    return [SelectionFormula.of_selectors(part) for part in prod]


class QueryPlan:
    resources: Sequence[KubeResource]
    separated_formulas: Sequence[SelectionFormula]

    def __init__(self, resources: Sequence[KubeResource], formula: SelectionFormula):
        self.resources = resources
        self.separated_formulas = _separate_formula(formula)
    
    @classmethod
    def _new_request(cls, target: KubeResource, cf_formula: SelectionFormula):
        labels = cf_formula.only_of(attr.Label)
        fields = cf_formula.only_of(attr.Field)
        labels_kube = formula_to_kube_api(labels)
        fields_kube = formula_to_kube_api(fields)
        return KubeListRequest(target, labels_kube, fields_kube)
    
    
