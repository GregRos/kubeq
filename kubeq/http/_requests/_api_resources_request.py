from dataclasses import dataclass
from typing import Iterable, override

from kubeq.kube_api._requests._base_request import KubeRequestBase
from kubeq.kube_api._requests._utils import AcceptHeader, AcceptSubclause

_v2_subclause = AcceptSubclause(
    version="v2",
    group="apidiscovery.k8s.io",
    as_="APIGroupDiscoveryList",
    content_type="application/json",
)

_v2_beta_subclause = _v2_subclause.with_(version="v2beta1")

_accept_for_discovery = AcceptHeader(
    "application/json", _v2_subclause, _v2_beta_subclause
)


@dataclass
class KubeCoreDiscoveryRequest(KubeRequestBase):
    @override
    def header_accept(self) -> AcceptHeader:
        return _accept_for_discovery

    @override
    def url_path(self):
        return ["api"]


@dataclass
class KubeExtraDiscoveryRequest(KubeCoreDiscoveryRequest):

    @override
    def url_path(self):
        return ["apis"]
