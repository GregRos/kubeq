from kubeq.query._operators._op_base import Op
from kubeq.query._operators._value_ops.op_multi_value import MultiValueOp
from kubeq.query._operators._value_ops.op_value import ValueOp


class Has(ValueOp[set[str], set[str]], value_type=set[str]):

    def __call__(self, what: set[str]) -> bool:
        return self.value.issubset(what)

    def __repr__(self) -> str:
        return f"in({", ".join(self.value)})"

    def normalize(self) -> Op[set[str]]:
        return self
