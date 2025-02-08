from dataclasses import dataclass
from typing import Literal

from box import Box


@dataclass
class KubeKind:
    group: str
    version: str
    name: str

    @property
    def fqn(self):
        parts = [self.version]
        if self.group:
            parts.append(self.group)
        parts.append(self.name)
        return "/".join(parts)

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
    def is_core(self):
        return self.version == "v1"

    @property
    def base_uri(self):
        if self.is_core:
            return ("api", self.version)
        return ("apis", self.group, self.version)
