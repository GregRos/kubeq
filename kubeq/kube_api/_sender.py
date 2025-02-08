from typing import Iterable
from kr8s import Api
from kubeq.version import __version__
from kubeq.kube_api._requests import KubeRequest, KubeDiscoveryRequest, KubeListRequest
from kubeq.kube_api._requests._list_request import KubeSelector


class KubeApiRequestSender:
    def __init__(self, api_client: Api):
        self.api_client = api_client

    def _shared_headers(self):
        return {
            "User-Agent": f"{__package__}/v{__version__}",
        }

    def _send_list(self, req: KubeListRequest):
        return self.api_client.async_get(
            kind=req.what,
            namespace=req.namespace,
            label_selector=self._splat_selectors(req.label_selectors),
            field_selector=self._splat_selectors(req.field_selectors),
        )
