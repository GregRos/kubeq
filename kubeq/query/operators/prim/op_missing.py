from kubeq.query.operators.op_base import Op
from kubeq.query.operators.prim.primitive_op import Primitive


class Missing(Primitive):
    def __call__(self, what: str) -> bool:
        return False
