from kubeq.operators.op_base import Op


from typeguard import check_type


from typing import Any


class op_ValueOp(Op):
    __match_args__ = ("value",)
    value: Any

    def __init_subclass__(cls, value_type: type) -> None:
        cls.value_type = value_type
        return super().__init_subclass__()

    def __init__(self, value: Any) -> None:
        check_type("value", value, self.value_type)
        self.value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
