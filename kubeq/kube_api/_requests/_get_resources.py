from dataclasses import dataclass
from typing import Iterable


@dataclass
class KubeSelector:
    name: str
    operator: str
    value: str

    def __str__(self):
        return f"{self.name} {self.operator} {self.value}"


class KubeGetResources:
    kind: str
    namespace: str | None
    label_selector: Iterable[KubeSelector]
    field_selector: Iterable[KubeSelector]

    def __init__(self, input: dict):
        self.input = input
