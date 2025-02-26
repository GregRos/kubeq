from typing import Mapping
from kubeq.entities._resource._resource import KubeResource
from kubeq.query._selection._selection_formula import SelectionFormula
import kubeq.query._attr as attr
import kubeq.query._operators as oprs


class ResourceFormula(SelectionFormula):
    def __init__(self, resource: KubeResource, formula: Mapping[attr.Any, oprs.Op]):
        self.resource = resource
        self.formula = formula
