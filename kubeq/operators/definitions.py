from abc import ABC, abstractmethod
import fnmatch
from typeguard import check_type
import re
from typing import Callable, ClassVar, Literal, Protocol, TypeAlias


_ops_by_symbol = {}


class Op[X]:
    def __init_subclass__(cls, name: str, symbol: str, arg_type: type) -> None:
        cls.name = name
        cls.symbol = symbol
        cls.arg_type = arg_type
        super().__init_subclass__()

    def __init__(self, value: X) -> None:
        check_type(value, self.arg_type)
        self.value = value


class EqOp(Op[str], name="eq", symbol="=", arg_type=str):
    def __call__(self, what: str) -> bool:
        return what == self.value


class NotEqOp(Op[str], name="not eq", symbol="!=", arg_type=str):

    def __call__(self, what: str) -> bool:
        return what != self.value


class InOp(Op[list[str]], name="in", symbol=":", arg_type=list[str]):
    def __call__(self, what: str) -> bool:
        return what in self.value


class NotInOp(Op[list[str]], name="not in", symbol="!:", arg_type=list[str]):
    def __call__(self, what: str) -> bool:
        return what not in self.value


class GlobOp(Op[str], name="glob", symbol="~", type=str):
    def __call__(self, what: str) -> bool:
        return fnmatch.fnmatch(what, self.value)


class NotGlobOp(Op[str], name="not glob", symbol="!~", arg_type=str):
    def __call__(self, what: str) -> bool:
        return not fnmatch.fnmatch(what, self.value)


class RegexOp(Op[str], name="regex", symbol="~~", arg_type=str):
    def __call__(self, what: str) -> bool:
        return bool(re.match(self.value, what))


class NotRegexOp(Op[str], name="not regex", symbol="!~~", arg_type=str):
    def __call__(self, what: str) -> bool:
        return not bool(re.match(self.value, what))


type ApiOp = EqOp | NotEqOp
type AnyOp = ApiOp | InOp | NotInOp | GlobOp | NotGlobOp | RegexOp | NotRegexOp
