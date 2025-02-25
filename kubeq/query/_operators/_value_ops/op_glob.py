from typing import TYPE_CHECKING
from kubeq.query._operators._value_ops.op_value import ValueOp

if TYPE_CHECKING:
    from kubeq.query._operators._value_ops.op_regexp import Regex


import fnmatch


class Glob(ValueOp[str], value_type=str):

    def __call__(self, what: str) -> bool:
        return fnmatch.fnmatch(what, self.value)

    def normalize(self) -> "Regex":
        return Regex(fnmatch.translate(self.value), original=self)

    def __repr__(self, /) -> str:
        return f"glob({self.value})"
