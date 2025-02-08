from dataclasses import dataclass
from typing import Iterable, Unpack

from kubeq.entities import KubeResource

from httpx import QueryParams, URL

from kubeq.http._requests._base_request import KubeRequest
from kubeq.http._requests._helpers._accept_header import AcceptHeader
from kubeq.http._requests._caching._cache_features import CacheFeatures
from kubeq.http._requests._helpers._kube_selector import KubeSelector


@dataclass
class KubeListRequest(KubeRequest):
    http_method = "GET"
    what: KubeResource
    namespace: str | None
    label_selectors: Iterable[KubeSelector]
    field_selectors: Iterable[KubeSelector]

    def __init__(self, **kwargs: Unpack[CacheFeatures]):
        super().__init__(**kwargs)

    def url_path(self):
        parts = self.what.list_uri()
        if self.namespace:
            assert self.what.is_namespaced, "Resource is not namespaced!"
            parts += ("namespaces", self.namespace)

        parts += (self.what.names.plural,)
        return parts

    def url_query(self):
        return QueryParams(
            {
                "labelSelector": KubeSelector.splat(self.label_selectors),
                "fieldSelector": KubeSelector.splat(self.field_selectors),
            }
        )

    def header_accept(self):
        return AcceptHeader("application/json")
