from dataclasses import dataclass
from typing import Literal

from box import Box

type ResourceClass = Literal["core", "builtin", "k8s", "custom"]


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
    def classify(self) -> ResourceClass:
        match self.version, self.group:
            case "v1" | "", "":
                return "core"
            case _, grp if "." not in grp:
                return "builtin"
            case _, grp if grp.endswith(".k8s.io"):
                return "k8s"
            case _:
                return "custom"

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
    def origin(self) -> ResourceClass:
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

    @property
    def is_core(self):
        return self.origin == "core"

    @property
    def is_builtin(self):
        match self.origin:
            case "core" | "builtin":
                return True
        return False

    @property
    def is_k8s(self):
        match self.origin:
            case "core" | "builtin" | "extension":
                return True
        return False

    @property
    def is_external(self):
        return not self.is_k8s
