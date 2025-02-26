import kubeq.query._attr as attr
from kubeq.entities._resource._resource import KubeResource
from kubeq.http._requests._helpers._kube_selector import KubeSelector, splat
from kubeq.run_query.op_to_str import formula_to_kube_api


import aioreactive as rx
import kr8s
from kr8s import Api


from typing import Iterable


class KubeListRequest:
    def __init__(
        self,
        target: KubeResource,
        labels: Iterable[KubeSelector],
        fields: Iterable[KubeSelector],
    ):
        self._target = target
        self._labels = labels
        self._fields = fields

    @property
    def kind(self):
        return self._target.kind.fqn

    @property
    def labels(self):
        return splat(self._labels)

    @property
    def fields(self):
        return splat(self._fields)

    def run(self, api: Api):

        return rx.from_async_iterable(
            api.async_get(
                kind=self.kind,
                labels=self.labels,
                fields=self.fields,
                namespace=kr8s.ALL,
            )
        )
