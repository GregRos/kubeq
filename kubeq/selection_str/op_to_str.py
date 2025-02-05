from typing import Iterable
from kubeq import attr
from kubeq.operators import op_In, op_And
from kubeq.operators.op_base import op_Any
from kubeq.operators.primitives.op_exists import op_Exists
from kubeq.operators.primitives.op_missing import op_Missing
from kubeq.operators.value_ops.kube_op_eq import op_Eq
from kubeq.operators.value_ops.kube_op_not_eq import op_NotEq
from kubeq.operators.value_ops.op_not_in import op_NotIn


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


def format_op(attr: attr.Any, op: op_Any):
    match op:
        case op_In(values):
            return _format_in(attr.name, values)
        case op_NotIn(values):
            return _format_not_in(attr.name, values)
        case op_Eq(value):
            return _format_eq(attr.name, value)
        case op_NotEq(value):
            return _format_not_eq(attr.name, value)
        case op_Exists():
            return _format_exists(attr.name)
        case op_Missing():
            return _format_missing(attr.name)
        case _:
            raise ValueError(f"Kubernetes API does not support {op}")
