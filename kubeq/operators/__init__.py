from .kube_ops import ApiOp, EqOp, NotEqOp
from .query_ops import InOp, NotInOp, GlobOp, NotGlobOp, RegexOp, NotRegexOp

type AnyOp = ApiOp | InOp | NotInOp | GlobOp | NotGlobOp | RegexOp | NotRegexOp
