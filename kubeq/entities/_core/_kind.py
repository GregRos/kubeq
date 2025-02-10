from dataclasses import dataclass
from typing import Literal

from box import Box

type ResourceOrigin = Literal["core", "builtin", "custom"]


@dataclass
class KubeKind:
    group: str
    version: str
    name: str

    @property
    def fqn(self):
        parts = []
        if self.group:
            parts.append(self.group)
        parts.append(self.version)
        parts.append(self.name)
        return "/".join(parts)

    @property
    def parent(self):
        [*parent, name] = self.fqn.split("/")
        return "/".join(parent)

    @staticmethod
    def parse_object(data: Box):
        return KubeKind(
            group=data.group,
            version=data.version or "v1",
            name=data.kind,
        )

    def __str__(self):
        return self.fqn

    @property
    def origin(self) -> ResourceOrigin:
        match self.version, self.group:
            case "v1", "":
                return "core"
            case "v1", _:
                return "builtin"
            case _, _:
                return "custom"

    @property
    def base_uri(self):
        if self.origin == "core":
            return ("api", self.version)
        return ("apis", self.group, self.version)
