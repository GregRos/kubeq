from typing import Mapping
from kubeq.entities._resource._resource import KubeResource
import kubeq.query._attr as attr
import kubeq.query._operators as oprs
from kubeq.selection._selection_formula import SelectionFormula


class ResourceFormula(SelectionFormula):
    def __init__(self, resource: KubeResource, formula: Mapping[attr.Any, oprs.Op]):
        self.resource = resource
        self.formula = formula
