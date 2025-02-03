from kubeq.operators import AnyOp
from kubeq.operators.boolean_ops import And, Or
from kubeq.operators.kubeq_ops import NotInOp
from kubeq.operators.leaf_op import ValueOp
from kubeq.selection.selector import Selector


class EqOp(ValueOp, value_type=str):

    def __call__(self, what: str) -> bool:
        return what == self.value


class NotEqOp(ValueOp, value_type=str):

    def __call__(self, what: str) -> bool:
        return what != self.value


def to_normal_form(op: And) -> Or:
    expand_nin = op.meap_leaves(
        lambda parent: (
            And(kid for kid in parent.value)
            if isinstance(parent, NotInOp)
            else [parent]
        )
    )
    eq_operators = [
        EqOp(value) for op in op for value in op.value if isinstance(op, NotInOp)
    ]

    # create queries of each eq operator with all neq operators
    return Or({And({eq, *neq_operators}) for eq in eq_operators})


def delift_selector(selector: Selector):
    return Selector(selector.attr, to_normal_form(selector.operator.kids))
