from cProfile import label
from kr8s.objects import APIObject


from dataclasses import dataclass

from kubeq.aliases._resource import APIResource


@dataclass
class Label:
    __match_args__ = ("name",)
    name: str

    def get(self, object: object) -> str:
        match object:
            case APIObject(labels=labels):
                return labels.get(self.name)
            case _:
                raise TypeError(f"Object {object} does not have labels")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Label) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
