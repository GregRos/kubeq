from typing import Iterable, overload

from kubeq.entities._resource._resource import KubeResource, KubeSubResource


class KubeResourceDb:
    _by_name: dict[str, KubeResource]

    def __init__(self, resources: Iterable[KubeResource]):
        self._by_name = {}
        self._load(resources)

    def _load(self, resources: Iterable[KubeResource]):
        for x in resources:
            self._by_name[x.names.main] = x
            self._by_name[x.names.plural] = x
            for y in x.names.short:
                self._by_name[y] = x
            self._by_name[x.fqn] = x

    @overload
    def __getitem__(self, name: str, /) -> KubeResource: ...
    @overload
    def __getitem__(self, parent: str, kid: str, /) -> KubeSubResource: ...
    def __getitem__(self, *args) -> KubeResource | KubeSubResource:
        if len(args) == 1:
            return self.resource(args[0])
        return self.subresource(*args)

    def resource(self, name: str) -> KubeResource:
        return self._by_name[name]

    def subresource(self, parent: str, kid: str) -> KubeSubResource:
        resource = self.resource(parent)
        return resource[kid]

    def subresources(self, parent: str) -> Iterable[KubeSubResource]:
        resource = self.resource(parent)
        return resource.kids.values()

    def __iter__(self):
        return iter(self._by_name.values())
