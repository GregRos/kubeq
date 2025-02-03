from attr import dataclass

from dictum.selection.selectors.operators.functions import ApiOperator, must_be_operator
from kr8s import Api
from kubernetes import client

field_aliases = {
    "name": "metadata.name",
    "namespace": "metadata.namespace",
    "n": "metadata.name",
    "ns": "metadata.namespace",
}


class ApiFieldSelector:
    key: str
    op: ApiOperator
    value: str

    def __init__(self, key: str, op: str, value: str):
        self.op = must_be_operator(op)
        self.key = field_aliases.get(key, key)
        self.value = value

    def to_query(self) -> dict[str, str]:
        return {"field_selector": f"{self.key}{self.op}{self.value}"}
