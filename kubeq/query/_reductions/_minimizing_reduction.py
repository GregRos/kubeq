from abc import abstractmethod
from typing import Callable
from kubeq.query._utils.render_op import print_operator
from kubeq.query._operators import *
from ._base_reduction import BaseReducers, ComboReduction
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

    def _make_combo(self):
        return ComboReduction(
            Squash_Leaf_Ops(normalize_operators=self.normalize_ops),
            Nullary_Terms_To_Prims(),
            Prune_Squash_Bools(),
        )

    def simplify_squash_until_done(self, op: Op) -> Op:

        iterations = 0
        while True:
            combo = self._make_combo()
            op = combo.reduce(op)
            if combo.reductions == 0:
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
