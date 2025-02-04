from kubeq.operators.op_base import Op
from kubeq.operators.reducers.base_reducer import BaseReducer
from kubeq.operators.value_ops.op_in import op_In


class InToEqReducer(BaseReducer):
    def reduce(self, op: Op) -> Op:
        match op:
            case op_In(kids):
                return op
