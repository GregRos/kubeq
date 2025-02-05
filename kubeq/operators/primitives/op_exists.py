from kubeq.operators.primitives.primitive_op import op_Primitive


class op_Exists(op_Primitive):
    def __call__(self, what: str) -> bool:
        return True
