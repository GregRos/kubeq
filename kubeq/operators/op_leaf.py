from kubeq.operators.primitives.op_exists import op_Exists
from kubeq.operators.primitives.op_never import op_Never
from kubeq.operators.value_ops.op_value import op_ValueOp


type op_LeafOp = op_Exists | op_Never | op_ValueOp
