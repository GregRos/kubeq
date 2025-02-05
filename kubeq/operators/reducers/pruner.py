from kubeq.operators.boolean.op_and import op_And
from kubeq.operators.boolean.op_or import op_Or
from kubeq.operators.op_base import op_Any
from kubeq.operators.primitives.op_exists import op_Exists
from kubeq.operators.primitives.op_never import op_Never
from kubeq.operators.reducers.base_reducer import BaseReducer


class Pruner(BaseReducer):

    def _prune_and(self, op: op_And):
        pruned = []
        for kid in op:
            match kid:
                case op_Exists():
                    self.increment()
                    continue
                case op_Never():
                    self.increment()
                    return op_Never()
                case op_And(kids):
                    pruned.extend([self.reduce(kid) for kid in kids])
                case _:
                    pruned.append(self.reduce(kid))
        return op_And(pruned)

    def _prune_or(self, op: op_Or):
        pruned = []
        for kid in op:
            match kid:
                case op_Never():
                    self.increment()
                    continue
                case op_Exists():
                    self.increment()
                    return op_Exists()
                case op_Or(kids):
                    pruned.extend([self.reduce(kid) for kid in kids])
                case _:
                    pruned.append(self.reduce(kid))
        return op_Or(pruned)

    def reduce(self, op: op_Any):
        match op:
            case op_And():
                return self._prune_and(op)
            case op_Or():
                return self._prune_or(op)
            case _:
                return op
