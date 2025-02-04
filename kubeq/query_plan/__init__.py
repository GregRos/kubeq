from .value_ops.op_regexp import RegexOp
from .value_ops.op_not_glob import NotGlobOp
from .value_ops.op_glob import GlobOp
from .value_ops.op_not_in import NotInOp
from .value_ops.in import InOp
from .value_ops.op_not_regexp import NotRegexOp

type AnyOp = InOp | NotInOp | GlobOp | NotGlobOp | RegexOp | NotRegexOp
