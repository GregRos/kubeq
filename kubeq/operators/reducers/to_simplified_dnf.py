from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import op_Any
from kubeq.operators.reducers.dnf_reducer import DnfReducer, assert_dnf
from kubeq.operators.reducers.leaf_reducer import LeafReducer
from kubeq.operators.reducers.pruner import Pruner
from kubeq.operators.reducers.simplifier import Simplifier
from kubeq.operators.reducers.squash_reducer import SquashReducer
from kubeq.attrs import attr_Any
from kubeq.selection.selector import Selector


def to_simplified_dnf(selector: Selector) -> op_Any:
    leaf_reducer = LeafReducer()
    simplifier = Simplifier()
    pruner = Pruner()
    dnf_reducer = DnfReducer()
    squasher = SquashReducer()
    # reduce leaves
    op = leaf_reducer.reduce(and_op)
    # simplify 1st time
    op = simplifier.reduce(op)

    # prune out null terms
    op = pruner.reduce(op)

    # simplify 2nd time
    op = simplifier.reduce(op)

    # reduce to DNF
    op = dnf_reducer.reduce(op)

    # squash like boolean terms and logical clauses with never/always
    op = squasher.reduce(op)

    # prune and simplify again:
    op = pruner.reduce(op)

    op = simplifier.reduce(op)

    assert_dnf(op)
    return op
