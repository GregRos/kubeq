from kubeq.entities._resource._resource import KubeResource
from kubeq.kube_api._client._kube_client_base import KubeClientBase
import aioreactive as rx

from kubeq.kube_api._requests._api_resources_request import KubeDiscoveryRequest

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


class KubeApiResources(KubeClientBase):

    async def api_resources(self, _: KubeDiscoveryRequest):

        core = self.send_parse(
            method="GET",
            url="/api",
            accept=_accept_for_discovery,
            headers={},
            parser=KubeResource.parse_response,
        )

        extra = self.send_parse(
            method="GET",
            url="/apis",
            accept=_accept_for_discovery,
            headers={},
            parser=KubeResource.parse_response,
        )

        return rx.pipe(
            core,
            rx.merge(extra),
            rx.flat_map(rx.from_iterable),
        )
