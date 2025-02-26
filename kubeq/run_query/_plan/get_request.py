from kubeq.http._requests._helpers._kube_selector import KubeSelector
from kubeq.query._selection._selection_formula import SelectionFormula


class KubeSelectionFormulas:
    def __init__(self, cf_formula: SelectionFormula):
        self.cf_formula = cf_formula

    def separate(self):
        return separate_formula(self.cf_formula)
