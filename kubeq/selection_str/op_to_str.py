from typing import Iterable
from kubeq.query import *


def _format_in_list(vals: Iterable[str]):
    return f"({",".join(vals)})"


def _make_options_formatter(op: str):
    def _formatter(key: str, options: Iterable[str]):
        return f"{key} {op} {_format_in_list(options)}"

    return _formatter


def _make_binary_formatter(op: str):
    def _formatter(key: str, value: str):
        return f"{key} {op} {value}"

    return _formatter


def _make_unary_formatter(op: str):
    def _formatter(key: str):
        return f"{op}{key}"

    return _formatter


_format_in = _make_options_formatter("in")
_format_not_in = _make_options_formatter("notin")
_format_eq = _make_binary_formatter("=")
_format_not_eq = _make_binary_formatter("!=")
_format_exists = _make_unary_formatter("")
_format_missing = _make_unary_formatter("!")


def format_op(attr: attr.Any, op: oprs.Op):
    match op:
        case oprs.In(values):
            return _format_in(attr.name, values)
        case oprs.NotIn(values):
            return _format_not_in(attr.name, values)
        case oprs.Eq(value):
            return _format_eq(attr.name, value)
        case oprs.NotEq(value):
            return _format_not_eq(attr.name, value)
        case oprs.Exists():
            return _format_exists(attr.name)
        case oprs.Missing():
            return _format_missing(attr.name)
        case _:
            raise ValueError(f"Kubernetes API does not support {op}")
