from abc import abstractmethod
from kubeq.query._operators._op_base import Op


class NegatedOp[T = str](Op[T]):
    @property
    @abstractmethod
    def positive(self) -> Op[T]: ...

    def __call__(self, input: T) -> bool:
        return not self.positive(input)

    def __repr__(self) -> str:
        return f"!{repr(self.positive)}"
