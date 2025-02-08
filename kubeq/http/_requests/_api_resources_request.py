from dataclasses import dataclass
from typing import Iterable, override
from xmlrpc.client import Boolean

from box import Box
from httpx import Response

from kubeq.entities._resource._names import KubeNames
from kubeq.entities._resource._resource import KubeResource, KubeSubResource
from kubeq.http._requests._rx_request import KubeRxRequest
from kubeq.http._utils import (
    AcceptSubclause,
    AcceptHeader,
    parse_names,
    parse_kind,
    parse_resource,
)
from ._base_request import KubeRequest
import aioreactive as rx

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
class KubeDiscoveryRequest(KubeRxRequest):
    def __init__(self, is_core_api: bool):
        self.is_core_api = is_core_api

    @override
    def _header_accept(self) -> AcceptHeader:
        return _accept_for_discovery

    @override
    def _url_path(self):
        return ["api"] if self.is_core_api else ["apis"]

    @override
    def _parse_json_object(self, body: Box) -> rx.AsyncObservable[KubeResource]:
        if not "versions" in body:
            raise ValueError("Invalid discovery response, no versions!")
        result = [parse_resource(version) for version in body.versions.resources]
        return rx.from_iterable(result)
