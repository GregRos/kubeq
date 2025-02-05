from kubeq.operators.op_base import op_Any
from kubeq.operators.primitives.primitive_op import op_Primitive


class op_Missing(op_Primitive):
    def __call__(self, what: str) -> bool:
        return False
