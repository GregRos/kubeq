from box import Box
from kr8s import api_resources

from kr8s.objects import APIObject

from dataclasses import dataclass

from kubeq.aliases._resource import APIResource


@dataclass
class Kind:
    __match_args__ = ("name",)
    name: str

    def get(self, object: object) -> str:
        match object:
            case APIObject() as o:
                return o.raw[self.name]
            case Box(d):
                return d[self.name]
            case _:
                raise TypeError(f"Object {object} does not have kind")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Kind)

    def __hash__(self) -> int:
        return hash("kind")
