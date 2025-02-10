from typing import Iterable, overload

from kubeq.entities._resource._sub_resource import KubeSubResource
from kubeq.entities._resource._resource import KubeResource
from kubeq.logging import sources

init_count = 0
logger = sources.r_db.logger


class KubeResourceDB:
    _by_name: dict[str, KubeResource]
    _list: list[KubeResource]

    def __init__(self, resources: Iterable[KubeResource]):
        global init_count

        self._by_name = {}
        logger.info(f"Initializing KubeRDB #{init_count}")
        init_count += 1
        self._list = []
        self._load(resources)

    def _load(self, resources: Iterable[KubeResource]):
        loaded = [*resources]
        logger.debug(f"Loading {len(loaded)} resources")
        loaded_count = 0
        for x in loaded:
            self._by_name[x.names.main] = x
            self._by_name[x.names.plural] = x
            for y in x.names.short:
                self._by_name[y] = x
            self._by_name[x.fqn] = x
            self._list.append(x)
            loaded_count += 1
            if loaded_count % 10 == 0:
                logger.debug(f"... Loading {x.id} ... [{loaded_count}/{len(loaded)}]")

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

    @property
    def resources(self) -> Iterable[KubeResource]:
        return self._list

    def subresource(self, parent: str, kid: str) -> KubeSubResource:
        resource = self.resource(parent)
        return resource[kid]

    def subresources(self, parent: str) -> Iterable[KubeSubResource]:
        resource = self.resource(parent)
        return resource.kids.values()

    def __iter__(self):
        return iter(self._list)
