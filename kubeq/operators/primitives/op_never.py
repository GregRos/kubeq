from kubeq.operators.primitives.primitive_op import PrimitiveOp


class op_Never(PrimitiveOp):
    def __call__(self, what: str) -> bool:
        return False
