from typing import overload
from kubeq.operators.op_base import Op
from kubeq.operators.value_ops.op_value import ValueOp


class NotIn(ValueOp[set[str]], value_type=set[str]):

    @overload
    def __init__(self, *values: str, original: "Op | None") -> None: ...
    @overload
    def __init__(self, value: set[str], *, original: "Op | None" = None) -> None: ...
    def __init__(self, *rest, **kwargs) -> None:
        if len(rest) == 1:
            super().__init__(rest[0], **kwargs)
        else:
            super().__init__(set(rest), **kwargs)

    def __call__(self, what: str) -> bool:
        return what not in self.value

    def normalize(self) -> Op:
        return self
