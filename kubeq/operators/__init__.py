from .value_ops.op_regexp import op_Regex
from .value_ops.op_not_glob import op_NotGlob
from .value_ops.op_glob import op_Glob
from .value_ops.op_not_in import op_NotIn
from .value_ops.op_in import op_In
from .value_ops.op_not_regexp import op_NotRegex
from .boolean.op_and import op_And
from .boolean.op_or import op_Or
from .op_leaf import op_LeafOp

type AnyOp = op_In | op_NotIn | op_Glob | op_NotGlob | op_Regex | op_NotRegex
