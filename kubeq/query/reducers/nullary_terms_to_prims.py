from kubeq.query.operators import *
from .base_reducer import BaseReducer


class Nullary_Terms_To_Prims(BaseReducer):

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
