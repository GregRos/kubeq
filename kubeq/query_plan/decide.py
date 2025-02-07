from kubeq.query import *
from kubeq.query._attr.kind import Kind
from ._kube_reductions import to_finite_set, To_Kube_Api_Supported


def _is_trivial(selectors: SelectionFormula) -> oprs.Always | oprs.Never | None:
    for k, v in selectors.items():
        match v:
            case oprs.Always() | oprs.Never():
                return v
    return None
