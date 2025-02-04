from xml.dom.minidom import Attr
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.reducers.dnf_reducer import DnfReducer
from kubeq.operators.reducers.squash_reducer import SquashReducer
from kubeq.query_plan.query_structure.kube_leaf_reducer import KubeLeafReducer
from kubeq.selection.selector import Selector


def reduce_to_supported_downstream(ops: op_Or):
    reducer = KubeLeafReducer()

    reduced = reducer.reduce(ops)

    squasher = SquashReducer()
    reduced = squasher.reduce(reduced)
    dnf_reducer = DnfReducer()
    _ = dnf_reducer.reduce(reduced)
    assert dnf_reducer.reductions == 0
    return reduced
