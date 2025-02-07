from abc import ABC
from kubeq.resource._shared import ResourceKind, Verbs


from dataclasses import dataclass


@dataclass
class ResourceBase(ABC):
    name: str
    kind: ResourceKind
    verbs: Verbs
