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


@dataclass
class KubeResource(KubeResourceBase):
    names: KubeNames
    is_namespaced: bool
    categories: tuple[str, ...] = field(default=())
    children: Mapping[str, "KubeSubResource"] = field(default_factory=dict)

    @property
    def base_uri(self):
        base = self.kind.base_uri
        return "/".join([base, self.names.plural])

    @staticmethod
    def parse(res: Box):
        raw_subresources = res.get("subresources", [])
        subresources: dict[str, KubeSubResource] = {
            subres.subresource: KubeSubResource.parse_subresource(subres)
            for subres in raw_subresources
        }
        daddy = KubeResource(
            names=KubeNames.parse_resource(res),
            kind=KubeKind.parse_object(res.responseKind),
            categories=res.get("categories", []),
            is_namespaced=res.scope == "Namespace",
            verbs=res.get("verbs", []),
            children=subresources,
        )
        for x in subresources.values():
            x.parent = daddy

        return daddy

    @staticmethod
    def parse_response(res: Box):
        if not "versions" in res:
            raise ValueError("Invalid discovery response, no versions!")
        return [KubeResource.parse(version) for version in res.versions.resources]


@dataclass
class KubeSubResource(KubeResourceBase):
    name: str
    parent: KubeResource = field(init=False, repr=False)

    @staticmethod
    def parse_subresource(res: Box):
        return KubeSubResource(
            name=res.subresource,
            kind=KubeKind.parse_object(res.responseKind),
            verbs=tuple(res.get("verbs", [])),
        )
