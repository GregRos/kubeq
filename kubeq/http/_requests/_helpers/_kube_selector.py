from dataclasses import dataclass
from typing import Iterable


@dataclass
class KubeSelector:
    name: str
    operator: str
    value: str

    def __str__(self):
        return f"{self.name} {self.operator} {self.value}"

    @staticmethod
    def splat(selectors: Iterable["KubeSelector"]):
        return ",".join(str(x) for x in selectors)
