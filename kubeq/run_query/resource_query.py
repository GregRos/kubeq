from kr8s import Api

from kubeq.query._selection._selection_formula import SelectionFormula
import kubeq.query._attr as attr
from ._kube_reductions import To_Min_Kube_Api_Supported


class RemoteQueryDriver:
    def __init__(self, api: Api):
        self._api = api

    def run(self, selection_formula: SelectionFormula):
        kube_reduced = selection_formula.reduce(To_Min_Kube_Api_Supported())
