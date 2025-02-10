from typing import Any, Iterable
from kubeq.entities._db import KubeResourceDB
from kubeq.logging import sources
from kubeq.query import *
from kubeq.query._attr.kind import Kind
import aioreactive as rx
from ._kube_reductions import to_finite_set, To_Kube_Api_Supported

logger = sources.query_d.logger


class QueryDecider:
    def __init__(self, rdb: KubeResourceDB):
        self.rdb = rdb

    def blah(self, selectors: Iterable[Selector]):
        kind_selectors = [
            selector for selector in selectors if isinstance(selector, KindSelector)
        ]
        target_resources = [
            r for r in self.rdb.resources if all(s for s in kind_selectors if s(r))
        ]
        logger.debug(f"Query matching {len(target_resources)} resources")
        urls = rx.pipe(
            rx.from_iterable(target_resources),
        )
