from dataclasses import dataclass
from typing import Iterable


@dataclass
class KubeBinarySelector:
    name: str
    operator: str
    value: str

    def __str__(self):
        return f"{self.name} {self.operator} {self.value}"


@dataclass
class KubeUnarySelector:
    name: str
    operator: str

    def __str__(self):
        return f"{self.operator}{self.name}"


type KubeSelector = KubeBinarySelector | KubeUnarySelector


def splat(selectors: Iterable[KubeSelector]) -> str:
    return ",".join(str(s) for s in selectors)
