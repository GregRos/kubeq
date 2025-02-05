from dataclasses import  dataclass
import string
from kubeq.attrs.field import attr_Field
from kubeq.attrs.label import attr_Label
from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import op_Any
from kubeq.attrs import attr_Any
from kubeq.operators.primitives.op_exists import op_Exists
from kubeq.operators.primitives.op_never import op_Never
from kubeq.operators.reducers.dnf_reducer import DnfReducer, assert_dnf
from kubeq.operators.reducers.squash_reducer import SquashReducer
from kubeq.operators.reducers.to_simplified_dnf import to_simplified_dnf
from kubeq.query_plan.query_structure.kube_leaf_reducer import KubeLeafReducer
from kubeq.selection.selector import Selector


def _reduce_to_supported_downstream(ops: op_Any):
    kube_leaf_reducer = KubeLeafReducer()

    reduced = kube_leaf_reducer.reduce(ops)

    dnf = to_simplified_dnf(reduced)
    return dnf

@dataclass
class SelectorString:
    attr: attr_Any
    value: str
    
    def is_label(self) -> bool:
        return isinstance(self.attr, attr_Label)
    
    def is_field(self) -> bool:
        return isinstance(self.attr, attr_Field)
    
    def __str__(self):
        return f"{self.attr}={self.value}"



def _to_selector_strings(
    attr: attr_Any, op: op_Any
) -> list[str] | op_Never | op_Exists:
    match op:
        case op_Never():
            return op
        case op_Exists():
            return op
        case op_And():
             
