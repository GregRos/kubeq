from typing import Callable
from kubeq.operators.op_base import Op


def apply_pair_reduction(
    ops: list[Op], pair_reduction: Callable[[Op, Op], tuple[Op, Op]]
):

    i = 0
    j = 1
    for i in range(len(ops)):
        for j in range(i + 1, len(ops)):
            ops[i], ops[j] = pair_reduction(ops[i], ops[j])
