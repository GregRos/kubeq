from kubeq.query._operators._prim.primitive_op import Primitive


class Exists(Primitive):
    def __call__(self, what: str) -> bool:
        return True

    def __repr__(self):
        return "∃"
