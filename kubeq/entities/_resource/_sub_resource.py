from kubeq.entities._core._kind import KubeKind
from kubeq.entities._resource._base import KubeResourceBase
from kubeq.entities._resource._resource import KubeResource


from dataclasses import dataclass, field


@dataclass
class KubeSubResource(KubeResourceBase):
    name: str
    kind: KubeKind
    parent: KubeResource = field(init=False, repr=False)
    is_status: bool = False

    @property
    def ident(self):
        is_name_kind = self.kind.name.lower() == self.name
        if not is_name_kind:
            return self.name
        else:
            return self.kind.name

    def list_uri(self, of: KubeResource | str):
        return self.parent.list_uri() + (of, self.name)

    def get_uri(self, of: KubeResource | str, name: str):
        return self.list_uri(of) + (name,)
