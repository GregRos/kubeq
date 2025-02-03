from kubeq.operators.core import Op


class Always(Op):
    def __call__(self, what: str) -> bool:
        return True


class Never(Op):
    def __call__(self, what: str) -> bool:
        return False
