from .kubeq_ops import InOp, NotInOp, GlobOp, NotGlobOp, RegexOp, NotRegexOp

type AnyOp = InOp | NotInOp | GlobOp | NotGlobOp | RegexOp | NotRegexOp
