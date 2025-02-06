from kubeq.query import *
from kubeq.query._attr.kind import Kind
from ._kube_reductions import to_finite_set, To_Kube_Api_Supported

def _is_trivial(selectors: SelectionFormula) -> oprs.Always | oprs.Never | None:
    for k, v in selectors.items():
        match v:
            case oprs.Always() | oprs.Never():
                return v
    return None

def _resource_kinds(selectors: SelectionFormula);
    kind_operator = selectors[Kind()]
    maybe_finite = to_finite_set(kind_operator)
    assert not isinstance(maybe_finite, oprs.Never), "Never should've been filtered out"
    match maybe_finite:
        case oprs.Always():

def decide(selectors: list[Selector]):
    squashed = SelectionFormula(selectors)
    for k, v in squashed.items():
        match v:
            case oprs.Always():
                return ["everything"]
            case oprs.Never():
                return []

            
