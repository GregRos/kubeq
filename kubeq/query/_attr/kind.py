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
        return isinstance(other, Kind)

    def __hash__(self) -> int:
        return hash("kind")

    def eq(self, value: str):
        from kubeq.query._operators import Eq
        from kubeq.query._selection import KindSelector

        return KindSelector(self, Eq(value))

    def in_(self, *values: str):
        from kubeq.query._operators import In
        from kubeq.query._selection import KindSelector

        return KindSelector(self, In(*values))

    def not_eq(self, value: str):
        from kubeq.query._operators import NotEq
        from kubeq.query._selection import KindSelector

        return KindSelector(self, NotEq(value))

    def not_in(self, *values: str):
        from kubeq.query._operators import NotIn
        from kubeq.query._selection import KindSelector

        return KindSelector(self, NotIn(*values))

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()
