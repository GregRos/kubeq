from ast import NotEq, NotIn
from kubeq.query._operators import *
from ._base_reducer import BaseReducer


class To_Finite_Set(BaseReducer):

    def _reduce_and(self, op: And):
        result = set()

        for x in op.operands:
            x = x.normalize()  # reduce eq to in
            x = self.reduce(x)
            match x:
                case In(value):
                    result.intersection_update(value)
                case Never():
                    return Never()
                case Always():
                    pass
        return In(result)

    def _reduce_or(self, op: Or):
        result = set()

        for x in op.operands:
            x = x.normalize()
            x = self.reduce(x)
            match x:
                case In(value):
                    result.update(value)
                case Never():
                    pass
                case Always():
                    return Always()
        return In(result)

    def reduce(self, op: Op) -> In | Always | Never:
        match op:
            case And():
                return self._reduce_and(op)
            case Or():
                return self._reduce_or(op)
            case In():
                return op
            case Eq():
                return In({op.value})
            case Never() | Missing():
                return Never()
            case Missing():
                return Never()
            case _:
                return Always()


def to_finite_set(x: Op) -> In | Always | Never:
    return To_Finite_Set().reduce(x)
