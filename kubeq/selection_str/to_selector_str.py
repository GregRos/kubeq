from kubeq.query import *


from kubeq.query._selection._instance_selector import InstanceSelector
from kubeq.selection_str.op_to_str import format_op


def _validated_selector(sel: InstanceSelector):
    assert not isinstance(sel.attr, attrs.Kind), f"Selectors are not allowed for kinds"
    op = oprs.And.of(sel.operator)
    for x in op.operands:
        assert not isinstance(
            x, (oprs.Or, oprs.And, oprs.Regex, oprs.Glob)
        ), f"Invalid operator {x}"
        assert isinstance(sel.attr, attrs.Label) or not isinstance(
            x, (oprs.In, oprs.NotIn, oprs.Missing, oprs.Exists)
        ), f"Operator {x} not allowed for {sel.attr}"
    return op


def to_selector_str(selector: InstanceSelector) -> str:
    and_form = _validated_selector(selector)
    strs = []
    for op in and_form.operands:
        strs.append(format_op(selector.attr, op))
    return ",".join(strs)
