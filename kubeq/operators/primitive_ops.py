from dataclasses import dataclass
from kubeq.operators.core import Op


@dataclass(eq=True)
class PrimitiveOp(Op):
    pass


class Always(Op):
    def __call__(self, what: str) -> bool:
        return True


class Never(Op):
    def __call__(self, what: str) -> bool:
        return False
