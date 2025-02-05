from kubeq.operators.boolean.boolean_ops import op_Bool
from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import op_Any
from kubeq.operators.primitives.op_always import op_Always
from kubeq.operators.primitives.op_exists import op_Exists
from kubeq.operators.primitives.op_missing import op_Missing
from kubeq.operators.primitives.op_never import op_Never
from kubeq.operators.reducers.base_reducer import BaseReducer
from kubeq.operators.value_ops.op_in import op_In
from kubeq.operators.value_ops.op_not_in import op_NotIn


class Simplifier(BaseReducer):

    def reduce(self, op: op_Any) -> op_Any:

        match op:
            case op_And([]):
                self.increment()
                return op_Always()
            case op_Or([]):
                self.increment()
                return op_Never()
            case op_In([]):
                self.increment()
                return op_Exists()
            case op_NotIn([]):
                self.increment()
                return op_Missing()
            case op_Bool([one]):
                self.increment()
                return self.reduce(one)
            case op_And([]):
                self.increment()
                return op_Exists()
            case op_Or([]):
                self.increment()
                return op_Never()
            case op_Bool(kids) as r:
                return r.__class__(self.reduce(kid) for kid in kids)
            case _:
                return op
