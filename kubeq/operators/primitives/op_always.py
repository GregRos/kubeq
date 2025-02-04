from kubeq.operators.primitives.primitive_op import PrimitiveOp


class Always(PrimitiveOp):
    def __call__(self, what: str) -> bool:
        return True
