from kubeq.operators.op_base import op_Any


from typeguard import check_type


from typing import Any


class op_ValueOp[V](op_Any):
    __match_args__ = ("value",)
    value: V

    def __init_subclass__(cls, value_type: type[V]) -> None:
        cls.value_type = value_type
        return super().__init_subclass__()

    def __init__(self, value: V) -> None:
        check_type("value", value, self.value_type)
        self.value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
