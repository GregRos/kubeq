from dataclasses import dataclass
from typing import Iterable, Unpack, override

from kubeq.entities import KubeResource

from httpx import QueryParams, URL

from kubeq.http._requests._base_request import KubeRequest
from kubeq.http._requests._helpers._accept_header import AcceptHeader
from kubeq.http._requests._helpers import KubeBinarySelector, KubeSelector, splat
from kubeq.storage._features import CacheFeatures


class KubeListRequest(KubeRequest):
    http_method = "GET"

    def __init__(
        self,
        what: KubeResource,
        namespace: str | None = None,
        label_selectors: Iterable[KubeBinarySelector] = (),
        field_selectors: Iterable[KubeSelector] = (),
        **kwargs: Unpack[CacheFeatures]
    ):
        super().__init__(**kwargs)
        self.what = what
        self.namespace = namespace
        self.label_selectors = label_selectors
        self.field_selectors = field_selectors

    def url_path(self):
        parts = self.what.list_uri()
        if self.namespace:
            assert self.what.is_cluster, "Resource is not namespaced!"
            parts += ("namespaces", self.namespace)

        parts += (self.what.names.plural,)
        return parts

    def url_query(self):
        return QueryParams(
            {
                "labelSelector": splat(self.label_selectors),
                "fieldSelector": splat(self.field_selectors),
            }
        )

    @property
    @override
    def header_accept(self):
        return AcceptHeader("application/json")
