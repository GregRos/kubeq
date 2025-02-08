from abc import ABC
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, Mapping

from box import Box

from ._names import KubeNames
from .._core._kind import KubeKind
from ._verbs import Verbs


@dataclass
class KubeResourceBase(ABC):
    kind: KubeKind
    verbs: Verbs

    @property
    def fqn(self):
        return self.kind.fqn

    def _compose_uri(self, *parts: str):
        return parts


@dataclass
class KubeResource(KubeResourceBase):
    names: KubeNames
    is_namespaced: bool
    categories: tuple[str, ...] = field(default=())
    kids: Mapping[str, "KubeSubResource"] = field(default_factory=dict)

    def __getitem__(self, item: str) -> "KubeSubResource":
        return self.kids[item]

    def list_uri(self):
        return self.kind.base_uri + (self.names.plural,)

    def get_uri(self, name: str):
        return self.list_uri() + (name,)


@dataclass
class KubeSubResource(KubeResourceBase):
    name: str
    parent: KubeResource = field(init=False, repr=False)

    def list_uri(self, of: KubeResource | str):
        return self.parent.list_uri() + (of, self.name)

    def get_uri(self, of: KubeResource | str, name: str):
        return self.list_uri(of) + (name,)
