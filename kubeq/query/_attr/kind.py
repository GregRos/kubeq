from box import Box
from kr8s import api_resources

from kr8s.objects import APIObject

from dataclasses import dataclass

from kubeq.entities._resource._resource import KubeResource
from kubeq.query._attr._base import BaseAttr

from box import Box
from kr8s import api_resources

from kr8s.objects import APIObject

from dataclasses import dataclass

from kubeq.entities._resource._resource import KubeResource
from kubeq.query._attr._base import BaseAttr


@dataclass
class Kind(BaseAttr):
    __match_args__ = ("name",)
    name: str

    def get(self, object: object) -> str:
        assert isinstance(object, KubeResource), f"Expected KubeResource, got {object}"
        return getattr(object, self.name)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Kind) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()
