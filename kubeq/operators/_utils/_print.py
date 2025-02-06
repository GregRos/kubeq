from ast import Or
from math import ceil
from typing import TYPE_CHECKING, Any, Iterable
from PrettyPrint import PrettyPrintTree
from colorama import Back
import colorama
import termcolor
from kubeq import operators as oprs

from kubeq.operators.op_base import Op


def visualize_operator(x: Op):
    def _get_children(x: Op):
        match x:
            case oprs.Bool():
                return x.operands
            case _:
                return []

    def _title(s: str):
        return (
            termcolor.colored(s, color="white", attrs=["bold"])
            + colorama.Back.LIGHTBLACK_EX
        )

    def _value(s: str):
        return (
            termcolor.colored(s, color="black", on_color="on_cyan")
            + colorama.Back.LIGHTBLACK_EX
        )

    def _print_value(v: str | list[str]):
        match v:
            case list(x) | set(x):
                return ", ".join(x)
            case str(x):
                return x

    def _two_line_value(title: str, subvalue: Any):
        printed = _print_value(subvalue).strip()
        max_length = max(len(title), len(printed))

        title = title.center(max_length)
        printed = printed.center(max_length)
        return "\n".join([_title(title), _value(printed)])

    def _get_value(x: Op):
        class_name = x.__class__.__name__
        match x:
            case oprs.Bool():
                return _title(class_name)
            case oprs.ValueOp():
                return _two_line_value(class_name, x.value)
            case oprs.Primitive():
                return _title(class_name)
            case _:
                raise ValueError(f"Unknown type {class_name}")

    pt = PrettyPrintTree(
        get_children=_get_children, get_val=_get_value, return_instead_of_print=True
    )  # type: ignore
    return pt(x)  # type: ignore


def collection_repr(name: str, sep: str, collection: Iterable[Any]) -> str:
    stuff = sep.join([f"{v!r}" for v in collection])
    return f"{name}({stuff})"
