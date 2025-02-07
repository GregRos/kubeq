from box import Box
from kr8s import api_resources


from dataclasses import dataclass

from kubeq.aliases._resource import APIResource


@dataclass
class Kind:
    __match_args__ = ("name",)
    name: str

    def get(self, object: APIResource) -> str:
        return object.get(self.name)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Kind)

    def __hash__(self) -> int:
        return hash("kind")
