from dataclasses import dataclass, field
from typing import Literal, Mapping

from box import Box

from kubeq.resource._base import ResourceBase
from kubeq.resource._shared import ResourceKind


@dataclass
class ResourceDef(ResourceBase):
    plural: str
    is_namespaced: bool
    short_names: tuple[str, ...] = field(default=())
    categories: tuple[str, ...] = field(default=())
    children: Mapping[str, "ResourceDef"] = field(default_factory=dict)


@dataclass
class SubresourceDef(ResourceBase):
    parent: ResourceDef = field(repr=False)
