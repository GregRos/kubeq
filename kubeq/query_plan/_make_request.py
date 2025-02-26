from dataclasses import dataclass
from itertools import product
from typing import Sequence
from kubeq.entities._resource._resource import KubeResource
from kubeq.http._requests._list_request import KubeListRequest
from kubeq.query_plan.op_to_str import formula_to_kube_api
from kubeq.selection._selection_formula import SelectionFormula
from kubeq.selection._selector import Selector
import kubeq.query._operators as oprs
import kubeq.query._attr as attr


def create_request(target: KubeResource, cf_formula: SelectionFormula):
    labels = cf_formula.only(attr.Label)
    fields = cf_formula.only(attr.Field)
    labels_kube = formula_to_kube_api(labels)
    fields_kube = formula_to_kube_api(fields)
    return KubeListRequest(target, None, labels_kube, fields_kube)
