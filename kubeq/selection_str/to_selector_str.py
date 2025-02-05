from kubeq import attr
from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import op_Any
from kubeq.operators.primitives.op_exists import op_Exists
from kubeq.operators.primitives.op_missing import op_Missing
from kubeq.operators.value_ops.kube_op_eq import op_Eq
from kubeq.operators.value_ops.kube_op_not_eq import op_NotEq
from kubeq.operators.value_ops.op_glob import op_Glob
from kubeq.operators.value_ops.op_in import op_In
from kubeq.operators.value_ops.op_not_in import op_NotIn
from kubeq.operators.value_ops.op_regexp import op_Regex
from kubeq.selection.selector import Selector
from kubeq.selection_str.op_to_str import format_op


def _validated_selector(sel: Selector):
    assert not isinstance(sel.attr, attr.Kind), f"Selectors are not allowed for kinds"
    op = op_And.of(sel.operator)
    for x in op.operands:
        assert not isinstance(
            x, (op_Or, op_And, op_Regex, op_Glob)
        ), f"Invalid operator {x}"
        assert isinstance(sel.attr, attr.Label) or not isinstance(
            x, (op_In, op_NotIn, op_Missing, op_Exists)
        ), f"Operator {x} not allowed for {sel.attr}"
    return op


def to_selector_str(selector: Selector) -> str:
    and_form = _validated_selector(selector)
    strs = []
    for op in and_form.operands:
        strs.append(format_op(selector.attr, op))
    return ",".join(strs)
