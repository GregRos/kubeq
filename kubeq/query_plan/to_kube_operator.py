from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import Op
from kubeq.operators.primitives.op_always import op_Always
from kubeq.operators.value_ops.op_in import op_In
from kubeq.operators.value_ops.op_not_in import op_NotIn
from kubeq.query_plan.kube_ops import op_Eq, op_NotEq
from kubeq.selection.formula import SelectionFormula


def _to_kube_operator(op: Op) -> op_Or | op_And | op_Always:
    if isinstance(op, op_In):
        return op_Or(op_Eq(v) for v in op.value)
    if isinstance(op, op_NotIn):
        return op_And(op_NotEq(v) for v in op.value)
    return op_Always()


def _to_kube_operators(formula: Op):
    if isinstance(formula, op_And):
        return op_And(_to_kube_operator(v) for v in formula.operands)
    if isinstance(formula, op_Or):
        return op_Or(_to_kube_operator(v) for v in formula.operands)
    return _to_kube_operator(formula)
