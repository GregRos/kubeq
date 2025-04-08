from dataclasses import dataclass
from typing import Iterable, Unpack, override
from xmlrpc.client import Boolean

from box import Box
from httpx import Response

from kubeq.entities._resource._sub_resource import KubeSubResource
from kubeq.entities._resource._names import KubeNames
from kubeq.entities._resource._resource import KubeResource
from kubeq.http._requests._helpers._parse_stuff import ResourceCtx
from kubeq.http._requests._rx_request import KubeRxRequest
from kubeq.storage._features import CacheFeatures
from ._helpers import (
    ComplexSubclause,
    AcceptHeader,
    parse_names,
    parse_kind,
    parse_resource,
)
from ._base_request import KubeRequest
import aioreactive as rx

_v2_subclause = ComplexSubclause(
    version="v2",
    group="apidiscovery.k8s.io",
    as_="APIGroupDiscoveryList",
    content_type="application/json",
)

_v2_beta_subclause = _v2_subclause.with_(version="v2beta1")

_accept_for_discovery = AcceptHeader(_v2_subclause, _v2_beta_subclause)


class KubeDiscoveryRequest(KubeRxRequest[KubeResource]):
    def __init__(self, is_core_api: bool, **caching: Unpack[CacheFeatures]):
        super().__init__(**caching)
        self.is_core_api = is_core_api

    @property
    @override
    def header_accept(self) -> AcceptHeader:
        return _accept_for_discovery

    @override
    def _url_path(self):
        return ["api"] if self.is_core_api else ["apis"]

    @override
    def _parse_json_object(self, body: Box) -> rx.AsyncObservable[KubeResource]:
        def _iter():
            for item in body.get("items"):
                group = item.metadata.get("name", None)
                for version_box in item.versions:
                    version = version_box.version
                    for resource in version_box.resources:
                        ctx = ResourceCtx(version, group)
                        yield parse_resource(resource, ctx)

        return rx.from_iterable([*_iter()])
