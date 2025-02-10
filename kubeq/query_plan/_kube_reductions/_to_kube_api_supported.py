from kubeq.query import *
from kubeq.query._reductions._base_reduction import BaseReducers
from kubeq.query._reductions._minimizing_reduction import MinimizingReduction


class To_Kube_Api_Supported(BaseReducers):
    def __init__(self, attr: attrs.Any):
        self.attr = attr
        super().__init__()

    def reduce(self, op: oprs.Op) -> oprs.Op:
        match self.attr, op:
            case (
                attrs.Label(),
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


class Min_To_Kube_Api_Supported(MinimizingReduction):
    def __init__(self, attr: attrs.Any):
        self.attr = attr
        super().__init__(normalize_ops=False)

    def make_reducer(self) -> BaseReducers:
        
