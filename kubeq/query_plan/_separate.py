from dataclasses import dataclass
from itertools import product
from typing import Sequence
from kubeq.entities._resource._resource import KubeResource
from kubeq.query_plan._kube_list_request import KubeListRequest
from kubeq.query_plan.op_to_str import formula_to_kube_api
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


def separate_formula(formula: SelectionFormula) -> Sequence[SelectionFormula]:
    destructured = [_separate_selector(selector) for selector in formula.selectors]
    prod = list(product(*destructured))
    return [SelectionFormula.of_selectors(part) for part in prod]
