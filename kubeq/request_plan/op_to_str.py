from typing import Iterable
from kubeq.http._requests._helpers._kube_selector import (
    KubeBinSelector,
    KubeSelector,
    KubeUnarySelector,
)
from kubeq.query import *
from kubeq.selection._selection_formula import SelectionFormula


def _format_in_list(vals: Iterable[str]):
    return f"({",".join(vals)})"


def _selector_to_kube_api(attr: attrs.Any, op: oprs.Op):
    match op:
        case oprs.In(values):
            return KubeBinSelector(attr.name, "in", _format_in_list(values))
        case oprs.NotIn(values):
            return KubeBinSelector(attr.name, "notin", _format_in_list(values))
        case oprs.Eq(value):
            return KubeBinSelector(attr.name, "=", value)
        case oprs.NotEq(value):
            return KubeBinSelector(attr.name, "!=", value)
        case oprs.Exists():
            return KubeUnarySelector(attr.name, "")
        case oprs.Missing():
            return KubeUnarySelector(attr.name, "!")
        case _:
            raise ValueError(f"Kubernetes API does not support {op}")


def formula_to_kube_api(formula: SelectionFormula) -> list[KubeSelector]:
    return [_selector_to_kube_api(attr, op) for attr, op in formula.items()]
