from itertools import product
from kubeq.operators.boolean.boolean_ops import op_Bool
from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import Op
from kubeq.operators.primitives.op_always import op_Always
from kubeq.operators.primitives.op_never import op_Never
from kubeq.operators.reducers.base_reducer import BaseReducer


class SquashReducer(BaseReducer):

    def reduce(self, op: Op) -> Op:
        if not isinstance(op, op_Bool):
            # no squishing leaf nodes
            return op

        kids = []
        for x in op.operands:
            x = self.reduce(x)
            match op, x:
                case op_And(), op_Always():
                    self.increment()
                    continue
                case op_Or(), op_Never():
                    self.increment()
                    continue
                case op_And(), op_Never():
                    return op_Never()
                case op_Or(), op_Always():
                    return op_Always()
            if isinstance(x, op.__class__):
                self.increment()
                kids.extend(x.operands)
            else:
                kids.append(x)
        return op.__class__(kids)
