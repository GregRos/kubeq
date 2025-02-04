from kubeq.operators.op_base import Op


class PrimitiveOp(Op):

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(self.__class__)
