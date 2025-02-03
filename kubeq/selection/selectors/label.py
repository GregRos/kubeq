from attr import dataclass

from dictum.selection.selectors.operators.functions import must_be_operator

label_aliases = {}


class ApiLabelSelector:
    key: str
    op: str
    value: str

    def __init__(self, key: str, op: str, value: str):
        self.op = must_be_operator(op)
        self.key = label_aliases.get(key, key)
        self.value = value

    def to_str(self) -> str:
        return f"{self.key}={self.value}"
