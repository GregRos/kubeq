from typing import overload
from kubeq.operators._utils._print import collection_repr
from kubeq.operators.op_base import Op
from kubeq.operators.value_ops.op_value import ValueOp
from kubeq.operators.value_ops.repr_collection import repr_collection


class MultiValueOp(ValueOp[set[str]], value_type=set[str]):
    @overload
    def __init__(self, *values: str) -> None: ...
    @overload
    def __init__(self, value: set[str], *, original: "Op | None" = None) -> None: ...
    def __init__(self, *rest, **kwargs) -> None:
        if len(rest) == 1:
            super().__init__(rest[0], **kwargs)
        else:
            super().__init__(set(rest), **kwargs)

    def __repr__(self) -> str:
        return collection_repr(self.__class__.__name__, ", ", self.value)

    def normalize(self) -> Op:
        return self
