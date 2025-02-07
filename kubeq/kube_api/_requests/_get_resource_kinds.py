from dataclasses import dataclass
from typing import Iterable


@dataclass
class KubeGetResourceKinds:
    verbs: Iterable[str] | None = None
    api_groups: Iterable[str] | None = None
    namespaced: bool | None = None
