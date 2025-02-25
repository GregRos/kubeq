from itertools import groupby
from typing import Any, Iterable
from kubeq.entities._db import KubeResourceDB
from kubeq.entities._resource._resource import KubeResource
from kubeq.http._client._client import KubeClient
from kubeq.http._requests._list_request import KubeListRequest
from kubeq.logging import sources
from kubeq.query import *
from kubeq.query._attr import Label
from kubeq.query._attr.field import Field
from kubeq.query._attr.kind import Kind
import aioreactive as rx

from kubeq.query._attr.label import Label
from kubeq.query._selection._squash import (
    SelectorSquash,
    SquashedSelectors,
    squash_selectors,
)
from kubeq.query_plan._kube_reductions._to_kube_api_supported import (
    Min_To_Kube_Api_Supported,
)
from kubeq.query_plan.op_to_str import selector_to_kube_api
from ._kube_reductions import to_finite_set, To_Kube_Api_Supported

logger = sources.query_d.logger


class QueryDecider:
    def __init__(self, rdb: KubeResourceDB, client: KubeClient):
        self.rdb = rdb
        self.client = client

    def _to_kube_api_formula(self, s: SelectorSquash):
        reduced = {
            attr: Min_To_Kube_Api_Supported(attr).reduce(op) for attr, op in s.items()
        }
        return [selector_to_kube_api(attr, op) for attr, op in reduced.items()]

    def _produce_list_request(self, r: KubeResource, selectors: SquashedSelectors):
        label_selectors = self._to_kube_api_formula(selectors[Label])
        field_selectors = self._to_kube_api_formula(selectors[Field])
        return KubeListRequest(
            what=r,
            namespace=None,
            label_selectors=label_selectors,
            field_selectors=field_selectors,
        )

    def _request_resources(self, r: KubeResource, selectors: SquashedSelectors):
        req = self._produce_list_request(r, selectors)
        logger.debug(
            f"Requesting resources for {r.id}",
            {
                "selectors": selectors,
                "request": req,
            },
        )
        return self.client.send(req)

    def query(self, *selectors: Selector):
        squashed = squash_selectors(selectors)
        kind_selectors = squashed.get(Kind, {}).values()
        target_resources = [
            r for r in self.rdb.resources if all(s for s in kind_selectors if s(r))
        ]
        logger.debug(f"Query matching {len(target_resources)} resources")
        r_data = rx.pipe(
            rx.from_iterable(target_resources),
            rx.flat_map(lambda x: self._request_resources(x, squashed)),
        )
        return r_data
