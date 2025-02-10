from abc import abstractmethod
from typing import Callable
from kubeq.query._utils.render_op import print_operator
from kubeq.query._operators import *
from ._base_reduction import BaseReducers
from ._squash_leaf_ops import Squash_Leaf_Ops
from ._prune_squash_bools import Prune_Squash_Bools
from ._nullary_terms_to_prims import Nullary_Terms_To_Prims


class MinimizingReduction(BaseReducers):

    def __init__(
        self,
        max_iterations: int = 10,
        normalize_ops=True,
    ):
        self.max_iterations = max_iterations
        self.normalize_ops = normalize_ops

    @abstractmethod
    def make_reducer(self) -> BaseReducers: ...

    @abstractmethod
    def cleanup(self, op: Op) -> None: ...

    def simplify_squash_until_done(self, op: Op) -> Op:

        iterations = 0
        while True:
            squash_leaf_ops = Squash_Leaf_Ops(normalize_operators=self.normalize_ops)
            nullary_terms_to_prims = Nullary_Terms_To_Prims()
            prune_squash_bools = Prune_Squash_Bools()
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

        print_operator("input", op)
        op = self.simplify_squash_until_done(op)
        print_operator("pre-squash", op)
        reducer_instance = self.make_reducer()
        messy_dnf = reducer_instance.reduce(op)
        print_operator("post-dnf", op)
        op = self.simplify_squash_until_done(messy_dnf)
        print_operator("post-squash", op)
        self.cleanup(op)
        return op
