from kubeq.operators.op_base import Op
from kubeq.operators.prim.primitive_op import Primitive


class Missing(Primitive):
    def __call__(self, what: str) -> bool:
        return False
