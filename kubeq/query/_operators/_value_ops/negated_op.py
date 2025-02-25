from abc import abstractmethod
from kubeq.query._operators._op_base import Op


class NegatedOp(Op):
    @property
    @abstractmethod
    def positive(self) -> Op: ...

    def __call__(self, input: str) -> bool:
        return not self.positive(input)

    def __repr__(self) -> str:
        return f"!{repr(self.positive)}"
