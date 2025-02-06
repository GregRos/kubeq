import kubeq.operators as oprs

from kubeq.operators._utils._print import print_operator
from kubeq.operators.op_base import Op
from kubeq.operators.reducers.dnf_reducer import DnfReducer, assert_dnf
from kubeq.operators.reducers.leaf_reducer import LeafReducer
from kubeq.operators.reducers.pruner import Pruner
from kubeq.operators.reducers.reduces_nullary_terms_to_prims import (
    Reduced_Nullary_Terms_To_Prims,
)
from kubeq.operators.reducers.squash_reducer import SquashReducer
import kubeq.attr
from kubeq.selection.selector import Selector


def to_simplified_dnf(operator: Op) -> Op:
    leaf_reducer = LeafReducer()
    simplifier = Reduced_Nullary_Terms_To_Prims()
    pruner = Pruner()
    dnf_reducer = DnfReducer()
    squasher = SquashReducer()
    print_operator("input", operator)
    # reduce leaves

    op = leaf_reducer.reduce(operator)
    print_operator("0) leaf_reducer", op)
    # simplify 1st time
    op = simplifier.reduce(op)
    print_operator("1) simplifier", op)

    # prune out null terms
    op = pruner.reduce(op)
    print_operator("2) pruner", op)
    # simplify 2nd time
    op = simplifier.reduce(op)
    print_operator("3) simplifier 2", op)
    # reduce to DNF
    op = dnf_reducer.reduce(op)
    print_operator("4) dnf", op)
    # squash like boolean terms and logical clauses with never/always
    op = simplifier.reduce(op)
    print_operator("5) simplifier 3", op)
    op = squasher.reduce(op)
    print_operator("6) squasher", op)
    # prune and simplify again:
    op = pruner.reduce(op)
    print_operator("7) pruner 2", op)

    op = leaf_reducer.reduce(op)
    print_operator("8) leaf_reducer 2", op)
    return op
