from kubeq.operators.primitives.op_always import op_Always
from kubeq.operators.primitives.op_never import op_Never
from kubeq.operators.value_ops.op_value import op_ValueOp


type op_LeafOp = op_Always | op_Never | op_ValueOp
