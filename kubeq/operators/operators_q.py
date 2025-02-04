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

from kubeq.operators.op_base import Op


class InOp(Op[set[str]], name="in", symbol=":", arg_type=set[str]):

    def __call__(self, what: str) -> bool:
        return what in self.value

    def to_normalized(self):
        return self


class NotInOp(Op[set[str]], name="not in", symbol="!:", arg_type=set[str]):

    def __call__(self, what: str) -> bool:
        return what not in self.value

    def to_normalized(self):
        return self


class GlobOp(Op[str], name="glob", symbol="~", arg_type=str):

    def __call__(self, what: str) -> bool:
        return fnmatch.fnmatch(what, self.value)

    def to_normalized(self):
        return RegexOp(fnmatch.translate(self.value))


class NotGlobOp(Op[str], name="not glob", symbol="!~", arg_type=str):
    def __call__(self, what: str) -> bool:
        return not fnmatch.fnmatch(what, self.value)

    def to_normalized(self):
        return NotRegexOp(fnmatch.translate(self.value))


class RegexOp(Op[str], name="regex", symbol="~~", arg_type=str):
    def __call__(self, what: str) -> bool:
        return bool(re.match(self.value, what))

    def to_normalized(self):
        return self


class NotRegexOp(Op[str], name="not regex", symbol="!~~", arg_type=str):
    def __call__(self, what: str) -> bool:
        return not bool(re.match(self.value, what))

    def to_normalized(self):
        return self


Never = InOp(set())
type NormedOp = InOp | NotInOp | RegexOp | NotRegexOp


def reduce_and(a: Op, b: Op) -> Sequence[Op]:
    a = a.to_normalized()
    b = b.to_normalized()
    match a, b:
        case InOp(v), InOp(u):
            return [InOp(v & u)]
        case InOp(v), RegexOp(x) as r:
            return [InOp({u for u in v if r(u)})]
        case InOp(u), NotInOp(v):
            return [InOp(u - v)]
        case InOp(u), NotRegexOp(x) as r:
            return [InOp({v for v in u if not r(v)})]
        case a, b:
            return [a, b]
