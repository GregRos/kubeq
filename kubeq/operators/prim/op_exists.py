from kubeq.operators.prim.primitive_op import Primitive


class Exists(Primitive):
    def __call__(self, what: str) -> bool:
        return True
