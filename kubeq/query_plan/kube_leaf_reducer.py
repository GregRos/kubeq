from kubeq.attr.field import Field
from kubeq.attr.label import Label
from kubeq.operators.boolean.boolean_ops import op_Bool
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import op_Any
from kubeq.operators.primitives.op_exists import op_Exists
from kubeq.operators.reducers.base_reducer import BaseReducer
from kubeq.operators.value_ops.kube_op_eq import kube_op_Eq
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
            case Label(), op_In() | op_NotIn():
                # in, not in okay for labels
                return op
            case _, op_In(kids):
                self.increment()
                return op_Or([kube_op_Eq(kid) for kid in kids])
            case _, op_NotIn(kids):
                self.increment()
                return op_Or([kube_op_Eq(kid) for kid in kids])
            case _, op_Regex() | op_Glob() | op_NotGlob() | op_NotRegex():
                self.increment()
                return op_Exists()
            case _, (op_Bool(kids) as r):
                return r.__class__([self.reduce(kid) for kid in kids])
            case _, r:
                return r
