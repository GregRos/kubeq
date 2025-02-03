from abc import ABC, abstractmethod
import fnmatch
from typeguard import check_type
import re
from typing import Callable, ClassVar, Literal, Protocol, TypeAlias


_ops_by_symbol = {}


class OpP[X](Protocol):
    name: ClassVar[str]
    symbol: ClassVar[str]
    arg_type: ClassVar[type]


class OpImpl[X](OpP[X]):
    def __init__(self, value: X) -> None:
        check_type("value", value, self.arg_type)
        self.value = value


class EqOp(OpImpl[str], OpP[str]):
    def __call__(self, what: str) -> bool:
        return what == self.value


class NotEqOp(OpImpl[str]):

    def __call__(self, what: str) -> bool:
        return what != self.value


class InOp(OpImpl[list[str]], name="in", symbol=":", arg_type=list[str]):
    def __call__(self, what: str) -> bool:
        return what in self.value


class NotInOp(OpImpl[list[str]], name="not in", symbol="!:", arg_type=list[str]):
    def __call__(self, what: str) -> bool:
        return what not in self.value


class GlobOp(OpImpl[str], name="glob", symbol="~", type=str):
    def __call__(self, what: str) -> bool:
        return fnmatch.fnmatch(what, self.value)


class NotGlobOp(OpImpl[str], name="not glob", symbol="!~", arg_type=str):
    def __call__(self, what: str) -> bool:
        return not fnmatch.fnmatch(what, self.value)


class RegexOp(OpImpl[str], name="regex", symbol="~~", arg_type=str):
    def __call__(self, what: str) -> bool:
        return bool(re.match(self.value, what))


class NotRegexOp(OpImpl[str], name="not regex", symbol="!~~", arg_type=str):
    def __call__(self, what: str) -> bool:
        return not bool(re.match(self.value, what))


type ApiOp = EqOp | NotEqOp
type AnyOp = ApiOp | InOp | NotInOp | GlobOp | NotGlobOp | RegexOp | NotRegexOp
