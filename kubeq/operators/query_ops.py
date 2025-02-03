from abc import ABC, abstractmethod
import fnmatch
from typeguard import check_type
import re
from typing import (
    Any,
    Callable,
    ClassVar,
    Literal,
    Protocol,
    Self,
    Sequence,
    TypeAlias,
    override,
    runtime_checkable,
)

from kubeq.operators.core import Op
from kubeq.operators.primitive_ops import Always
from kubeq.operators.value_op import ValueOp


class InOp(ValueOp, value_type=set[str]):

    def __call__(self, what: str) -> bool:
        return what in self.value


class NotInOp(ValueOp, value_type=set[str]):

    def __call__(self, what: str) -> bool:
        return what not in self.value

    def to_normalized(self):
        return self


class GlobOp(ValueOp, value_type=str):

    def __call__(self, what: str) -> bool:
        return fnmatch.fnmatch(what, self.value)


class NotGlobOp(ValueOp, value_type=str):
    def __call__(self, what: str) -> bool:
        return not fnmatch.fnmatch(what, self.value)


class RegexOp(ValueOp, value_type=str):
    original: GlobOp | None = None

    def __call__(self, what: str) -> bool:
        return bool(re.match(self.value, what))

    def to_normalized(self):
        return self


class NotRegexOp(ValueOp, value_type=str):
    original: NotGlobOp | None = None

    def __call__(self, what: str) -> bool:
        return not bool(re.match(self.value, what))

    def to_normalized(self):
        return self


type NormedOp = InOp | NotInOp | RegexOp | NotRegexOp
