from kubeq.query import *
from kubeq.query._reducers._base_reducer import BaseReducer


class KubeLeafReducer(BaseReducer):
    def __init__(self, attr: _attr.Any):
        self.attr = attr
        super().__init__()

    def reduce(self, op: oprs.Op) -> oprs.Op:
        match self.attr, op:
            case (
                _attr.Label(),
                oprs.In() | oprs.NotIn() | oprs.Missing() | oprs.Exists(),
            ):
                # in, notin, exists, missing: allowed for labels
                return op
            case _, oprs.In(kids):
                self.increment()
                return oprs.Or([oprs.Eq(kid) for kid in kids])
            case _, oprs.NotIn(kids):
                self.increment()
                return oprs.Or([oprs.Eq(kid) for kid in kids])
            case (
                _,
                oprs.Regex()
                | oprs.Glob()
                | oprs.NotGlob()
                | oprs.NotRegex()
                | oprs.Missing()
                | oprs.Exists(),
            ):
                self.increment()
                return oprs.Always()
            case _, oprs.And(kids):
                return oprs.And([self.reduce(kid) for kid in kids])
            case _, oprs.Or(kids):
                raise ValueError("Or should not be here")
            case _, r:
                return r
