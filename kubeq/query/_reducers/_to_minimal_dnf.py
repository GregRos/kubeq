from kubeq.query._utils.render_op import print_operator
from kubeq.query.operators import *
from ._base_reducer import BaseReducer
from ._to_messy_dnf import To_Messy_Dnf, assert_dnf
from ._squash_leaf_ops import Squash_Leaf_Ops
from ._prune_squash_bools import Prune_Squash_Bools
from ._nullary_terms_to_prims import Nullary_Terms_To_Prims


class To_Minimal_Dnf(BaseReducer):

    def __init__(self, max_iterations: int = 10, normalize_operators: bool = True):
        self.max_iterations = max_iterations

    def simplify_squash_until_done(self, op: Op) -> Op:
        squash_leaf_ops = Squash_Leaf_Ops()
        nullary_terms_to_prims = Nullary_Terms_To_Prims()
        prune_squash_bools = Prune_Squash_Bools()
        iterations = 0
        while True:
            op = squash_leaf_ops.reduce(op)
            op = nullary_terms_to_prims.reduce(op)
            op = prune_squash_bools.reduce(op)
            vector = tuple(
                x.reductions
                for x in [squash_leaf_ops, nullary_terms_to_prims, prune_squash_bools]
            )
            if vector == (0, 0, 0):
                return op
            iterations += 1
            if iterations > self.max_iterations:
                return op

    def reduce(self, op: Op) -> Op:

        to_messy_dnf = To_Messy_Dnf()
        print_operator("input", op)
        op = self.simplify_squash_until_done(op)
        print_operator("pre-squash", op)

        messy_dnf = to_messy_dnf.reduce(op)
        print_operator("post-dnf", op)
        op = self.simplify_squash_until_done(messy_dnf)
        print_operator("post-squash", op)
        assert_dnf(op)
        return op


def to_minimal_dnf(s: Op) -> Op:
    reducer = To_Minimal_Dnf()
    return reducer.reduce(s)
