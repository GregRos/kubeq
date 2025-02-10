from kubeq.entities._core._kind import KubeKind
from kubeq.entities._resource._verbs import KubeVerbTuple


from abc import ABC
from dataclasses import dataclass


@dataclass
class KubeResourceBase(ABC):
    verbs: KubeVerbTuple

    def _compose_uri(self, *parts: str):
        return parts
