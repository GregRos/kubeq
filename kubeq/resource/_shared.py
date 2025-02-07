from dataclasses import dataclass
from typing import Literal

from box import Box


type KubeVerb = Literal[
    "get", "list", "watch", "create", "update", "patch", "delete", "deletecollection"
]
type Verbs = tuple[KubeVerb, ...]


@dataclass
class ResourceKind:
    group: str
    version: str
    name: str

    @staticmethod
    def from_(data: Box):
        return ResourceKind(
            group=data.group,
            version=data.version,
            name=data.kind,
        )

    def __str__(self):
        parts = [self.version or "v1"]
        if self.group:
            parts.append(self.group)
        parts.append(self.name)
        return "/".join(parts)
