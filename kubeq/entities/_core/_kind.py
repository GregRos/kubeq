from dataclasses import dataclass
from typing import Literal

from box import Box


@dataclass
class KubeKind:
    group: str
    version: str
    name: str

    @staticmethod
    def parse_object(data: Box):
        return KubeKind(
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

    @property
    def is_core(self):
        return self.version == "v1"
