from kubeq.operators.primitives.primitive_op import op_Primitive


class op_Never(op_Primitive):
    def __call__(self, what: str) -> bool:
        return False

    def __eq__(self, other):
        return isinstance(other, op_Never)
