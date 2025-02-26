from kubeq.entities._resource._resource import KubeResource
from kubeq.query._selection._selection_formula import SelectionFormula
from kubeq.run_query._plan.kube_list_request import KubeListRequest
import kubeq.query._attr as attr

from typing import Sequence

from kubeq.run_query.op_to_str import formula_to_kube_api


class KubeMatchedResources:
    def __init__(self, resources: Sequence[KubeResource]):
        self.resources = resources

    @classmethod
    def new_request(cls, target: KubeResource, cf_formula: SelectionFormula):
        labels = cf_formula.only_of(attr.Label)
        fields = cf_formula.only_of(attr.Field)
        labels_kube = formula_to_kube_api(labels)
        fields_kube = formula_to_kube_api(fields)
        return KubeListRequest(target, labels_kube, fields_kube)

    def make_requests(self, cf_formula: SelectionFormula):
        return [self.new_request(r, cf_formula) for r in self.resources]

    def __len__(self):
        return len(self.resources)
