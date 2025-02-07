from kubeq.kube_api._client._http import AcceptHeader, AcceptSubclause
from kubeq.kube_api._client._kube_client_base import KubeClientBase

_v2_subclause = AcceptSubclause(
    version="v2",
    group="apidiscovery.k8s.io",
    as_="APIGroupDiscoveryList",
    content_type="application/json",
)

_v2_beta_subclause = _v2_subclause.with_(version="v2beta1")

accept_for_discovery = AcceptHeader(
    "application/json", _v2_subclause, _v2_beta_subclause
)


class KubeApiResourcesClient(KubeClientBase):
    async def api_resources(self):
        core = self.send(
            method="GET", url="/api", accept=accept_for_discovery, headers={}
        )
        extra = self.send(
            method="GET", url="/apis", accept=accept_for_discovery, headers={}
        )
