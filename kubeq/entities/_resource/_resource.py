from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, Mapping

from box import Box

from kubeq.entities._core._kind import KubeKind
from kubeq.entities._resource._base import KubeResourceBase

if TYPE_CHECKING:
    from kubeq.entities._resource._sub_resource import KubeSubResource

from ._names import KubeNames


@dataclass
class KubeResource(KubeResourceBase):
    kind: KubeKind
    names: KubeNames
    is_cluster: bool
    categories: tuple[str, ...] = field(default=())
    kids: Mapping[str, "KubeSubResource"] = field(default_factory=dict, repr=False)

    @property
    def version(self):
        return self.kind.version

    @property
    def classify(self):
        return self.kind.classify

    def __format__(self, format_spec: str) -> str:
        match format_spec:
            case "short":
                return self.ident
            case "fqn":
                return self.fqn
            case "full":
                return super().__str__()
            case _:
                return super().__format__(format_spec)

    @property
    def ident(self):
        return self.kind.name

    @property
    def fqn(self):
        return self.kind.fqn

    @property
    def id(self):
        return self.fqn

    def __getitem__(self, item: str) -> "KubeSubResource":
        return self.kids[item]

    def list_uri(self):

        return self.kind.base_uri + (self.names.plural,)

    def get_uri(self, name: str):
        return self.list_uri() + (name,)

    def __str__(self):
        return self.fqn
