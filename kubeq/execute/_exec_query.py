from dataclasses import dataclass
from typing import Sequence

from box import Box
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
from kubeq.utils import rxq

c = Console()


@dataclass
class QueryExecution:
    client: KubeClient
    selectors: SelectionFormula

    async def run(self) -> Sequence[Box]:
        rdb = await construct_rdb(self.client)
        kind_selectors = self.selectors.only(Kind)

        labels_and_fields = self.selectors.without(Kind)
        only_kube_supported = labels_and_fields.reduce(
            lambda x: To_Min_Kube_Api_Supported(x)
        )
        affected = filter(kind_selectors, rdb.resources)
        query_plan = RequestPlan(list(affected), only_kube_supported)
        visualize(query_plan)

        reqs = query_plan.to_requests()
        return await rx.pipe(
            rx.from_iterable(reqs),
            rx.flat_map(lambda r: self.client.send(r)),
            rx.filter(labels_and_fields),
            rxq.to_list(),
            rxq.run,
        )  # type: ignore
