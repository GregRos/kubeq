from dataclasses import dataclass
from typing import Sequence
from attrs import attr_Any

from kubeq.operators import op_LeafOp, op_And, kube_op_Eq, kube_op_NotEq
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import op_Any
from kubeq.operators.primitives.op_exists import op_Exists
from kubeq.operators.primitives.op_never import op_Never
from kubeq.selection.selector import Selector

type KubeOperator = kube_op_Eq | kube_op_NotEq | op_Exists | op_Never


@dataclass
class KubeSelectorRepr:
    def __init__(self, attr: attr_Any, op: Sequence[KubeOperator]):
        self.attr = attr
        self.op = op

    @classmethod
    def _must_be_kube_leaf(cls, attr: attr_Any, op: op_Any):
        assert (
            isinstance(op, kube_op_Eq)
            or isinstance(op, kube_op_NotEq)
            or isinstance(op, op_Exists)
            or isinstance(op, op_Never)
        )
        return op

    @classmethod
    def from_and_clause(cls, attr: attr_Any, op: op_Any):
        assert isinstance(op, op_And)
        return KubeSelectorRepr(
            attr, [cls._must_be_kube_leaf(attr, kid) for kid in op.operands]
        )

    @classmethod
    def from_or_clause(cls, attr: attr_Any, op: op_Any):
        assert isinstance(op, op_Or)
        return [cls.from_and_clause(attr, kid) for kid in op.operands]

def create_kube_selector_set(selectors: Selector)