from kubeq.operators.op_base import op_Any


class op_Primitive(op_Any):

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(self.__class__)

    def normalize(self) -> op_Any:
        return self
