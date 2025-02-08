from dataclasses import dataclass
from typing import Iterable

from kubeq.entities import KubeResource

from httpx import QueryParams, URL

from kubeq.kube_api._requests._base_request import KubeRequestBase


@dataclass
class KubeSelector:
    name: str
    operator: str
    value: str

    def __str__(self):
        return f"{self.name} {self.operator} {self.value}"

    @staticmethod
    def splat(selectors: Iterable["KubeSelector"]):
        return ",".join(str(x) for x in selectors)


@dataclass
class KubeListRequest(KubeRequestBase):
    http_method = "GET"
    what: KubeResource
    namespace: str | None
    label_selectors: Iterable[KubeSelector]
    field_selectors: Iterable[KubeSelector]

    def __init__(self, input: dict):
        self.input = input

    def url_path(self):
        parts = [self.what.base_uri]
        if self.namespace:
            assert self.what.is_namespaced, "Resource is not namespaced!"
            parts.append("namespaces")
            parts.append(self.namespace)
        parts.append(self.what.names.plural)
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
