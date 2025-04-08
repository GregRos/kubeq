from dataclasses import dataclass
from typing import (
    Awaitable,
    Mapping,
    NotRequired,
    Sequence,
    TypedDict,
    Unpack,
    overload,
)

from box import Box
from kr8s import api
from kubeq.entities._db import KubeResourceDB
from kubeq.execute._construct_rdb import construct_rdb
from kubeq.http._client._client import KubeClient
from kubeq.query._attr.kind import Kind
from kubeq.request_plan._kube_reductions._to_kube_api_supported import (
    To_Min_Kube_Api_Supported,
)
from kubeq.request_plan._request_plan import RequestPlan
from kubeq.request_plan._visualize import visualize
from kubeq.selection import Selector
from kubeq.selection._selection_formula import SelectionFormula
import aioreactive as rx
from rich.console import Console
from kubeq.storage._features import CacheFeatures
from kubeq.utils import rxq
import kubeq.query._attr as attrs
import kubeq.query._operators as ops

c = Console()


class KubeQClientOptions(TypedDict):
    url: NotRequired[str | None]
    kubeconfig: NotRequired[str | None]
    serviceaccount: NotRequired[str | None]
    namespace: NotRequired[str | None]
    context: NotRequired[str | None]


class KubeQ:
    _client: KubeClient
    _resources: KubeResourceDB

    @overload
    def __init__(self, /, **options: Unpack[KubeQClientOptions]): ...

    @overload
    def __init__(self, client: KubeClient | None = None, /): ...

    def __init__(
        self, client: KubeClient | None = None, /, **options: Unpack[KubeQClientOptions]
    ):
        self._client = client or KubeClient(api(**options))

    async def init(self, **cache_features: Unpack[CacheFeatures]):
        rdb = await construct_rdb(self._client, **cache_features)
        self._resources = rdb

    @property
    async def resources(self):
        if not self._resources:
            await self.init()
        return self._resources

    async def query(self, formula: Mapping[attrs.Any, ops.Op]) -> Sequence[Box]:
        rdb = await self.resources
        formula = SelectionFormula(formula)
        kind_selectors = formula.only(Kind)

        labels_and_fields = formula.without(Kind)
        only_kube_supported = labels_and_fields.reduce(
            lambda x: To_Min_Kube_Api_Supported(x)
        )
        affected = filter(kind_selectors, rdb.resources)
        query_plan = RequestPlan(list(affected), only_kube_supported)
        visualize(query_plan)

        reqs = query_plan.to_requests()
        return await rx.pipe(
            rx.from_iterable(reqs),
            rx.flat_map(lambda r: self._client.send(r)),
            rx.filter(labels_and_fields),
            rxq.to_list(),
            rxq.run,
        )  # type: ignore
