from kubeq.query.operators.boolean.op_and import And
from kubeq.query.operators.boolean.op_or import Or
from kubeq.query.operators.op_base import Op
from kubeq.query.operators.prim.op_always import Always
from kubeq.query.operators.prim.op_exists import Exists
from kubeq.query.operators.prim.op_never import Never
from kubeq.query.operators.reducers.base_reducer import BaseReducer


class Prune_Squash_Bools(BaseReducer):

    def _prune_and(self, op: And):
        pruned = []
        for kid in op:
            match kid:
                case Always():
                    self.increment()
                    continue
                case Never():
                    self.increment()
                    return Never()
                case And(kids):
                    self.increment()
                    pruned.extend([self.reduce(kid) for kid in kids])
                case _:
                    pruned.append(self.reduce(kid))
        return And(pruned)

    def _prune_or(self, op: Or):
        pruned = []
        for kid in op:
            match kid:
                case Never():
                    self.increment()
                    continue
                case Always():
                    self.increment()
                    return Always()
                case Or(kids):
                    self.increment()
                    pruned.extend([self.reduce(kid) for kid in kids])
                case _:
                    pruned.append(self.reduce(kid))
        return Or(pruned)

    def reduce(self, op: Op):
        match op:
            case And():
                return self._prune_and(op)
            case Or():
                return self._prune_or(op)
            case _:
                return op
