from kubeq.attr.field import Field
from kubeq.attr.label import Label
from kubeq.operators.boolean.boolean_ops import op_Bool
from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import op_Any
from kubeq.operators.primitives.op_always import op_Always
from kubeq.operators.primitives.op_exists import op_Exists
from kubeq.operators.primitives.op_missing import op_Missing
from kubeq.operators.reducers.base_reducer import BaseReducer
from kubeq.operators.value_ops.kube_op_eq import op_Eq
from kubeq.operators.value_ops.op_glob import op_Glob
from kubeq.operators.value_ops.op_in import op_In
from kubeq.operators.value_ops.op_not_glob import op_NotGlob
from kubeq.operators.value_ops.op_not_in import op_NotIn
from kubeq.operators.value_ops.op_not_regexp import op_NotRegex
from kubeq.operators.value_ops.op_regexp import op_Regex
from kubeq import attr


class KubeLeafReducer(BaseReducer):
    def reduce(self, op: op_Any) -> op_Any:
        match self.attr, op:
            case Label(), op_In() | op_NotIn() | op_Missing() | op_Exists():
                # in, notin, exists, missing: allowed for labels
                return op
            case _, op_In(kids):
                self.increment()
                return op_Or([op_Eq(kid) for kid in kids])
            case _, op_NotIn(kids):
                self.increment()
                return op_Or([op_Eq(kid) for kid in kids])
            case (
                _,
                op_Regex()
                | op_Glob()
                | op_NotGlob()
                | op_NotRegex()
                | op_Missing()
                | op_Exists(),
            ):
                self.increment()
                return op_Always()
            case _, op_And(kids):
                return op_And([self.reduce(kid) for kid in kids])
            case _, op_Or(kids):
                raise ValueError("Or should not be here")
            case _, r:
                return r
