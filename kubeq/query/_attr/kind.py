from box import Box
from kr8s import api_resources

from kr8s.objects import APIObject

from dataclasses import dataclass

from kubeq.entities._resource._resource import KubeResource


@dataclass
class Kind:
    __match_args__ = ("name",)
    name: str

    def get(self, object: KubeResource) -> str:
        return getattr(object, self.name)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Kind)

    def __hash__(self) -> int:
        return hash("kind")
