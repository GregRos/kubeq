from itertools import product
from kubeq.operators.boolean.boolean_ops import Bool
from kubeq.operators.boolean.op_and import And
from kubeq.operators.boolean.op_or import Or
from kubeq.operators.op_base import Op
from kubeq.operators.primitives.op_always import Always
from kubeq.operators.primitives.op_exists import Exists
from kubeq.operators.primitives.op_never import Never
from kubeq.operators.reducers.base_reducer import BaseReducer


class SquashReducer(BaseReducer):

    def reduce(self, op: Op) -> Op:
        if not isinstance(op, Bool):
            # no squishing leaf nodes
            return op

        kids = []
        for x in op.operands:
            x = self.reduce(x)
            match op, x:
                case And(), Always():
                    self.increment()
                    continue
                case Or(), Never():
                    self.increment()
                    continue
                case And(), Never():
                    return Never()
                case Or(), Always():
                    return Exists()
            if isinstance(x, op.__class__):
                self.increment()
                kids.extend(x.operands)
            else:
                kids.append(x)
        return op.__class__(kids)
