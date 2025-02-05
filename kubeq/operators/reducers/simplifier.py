from kubeq.operators.boolean.boolean_ops import Bool
from kubeq.operators.boolean.op_and import And
from kubeq.operators.boolean.op_or import Or
from kubeq.operators.op_base import Op
from kubeq.operators.primitives.op_always import Always
from kubeq.operators.primitives.op_exists import Exists
from kubeq.operators.primitives.op_missing import Missing
from kubeq.operators.primitives.op_never import Never
from kubeq.operators.reducers.base_reducer import BaseReducer
from kubeq.operators.value_ops.op_in import In
from kubeq.operators.value_ops.op_not_in import NotIn


class Simplifier(BaseReducer):

    def reduce(self, op: Op) -> Op:

        match op:
            case And([]):
                self.increment()
                return Always()
            case Or([]):
                self.increment()
                return Never()
            case In([]):
                self.increment()
                return Exists()
            case NotIn([]):
                self.increment()
                return Missing()
            case Bool([one]):
                self.increment()
                return self.reduce(one)
            case And([]):
                self.increment()
                return Exists()
            case Or([]):
                self.increment()
                return Never()
            case Bool(kids) as r:
                return r.__class__(self.reduce(kid) for kid in kids)
            case _:
                return op
