from kubeq.query._operators._prim.primitive_op import Primitive


class Never(Primitive):
    def __call__(self, what: str) -> bool:
        return False

    def __eq__(self, other):
        return isinstance(other, Never)

    def __repr__(self):
        return "※"
