from typing import Iterable
from kr8s import Api
from kubeq.version import __version__
from kubeq.kube_api._requests import KubeRequest, KubeGetResourceKinds, KubeGetResources
from kubeq.kube_api._requests._get_resources import KubeSelector


class KubeApiRequestSender:
    def __init__(self, api_client: Api):
        self.api_client = api_client

    def _splat_selectors(self, op: Iterable[KubeSelector]):
        return ",".join([str(s) for s in op]) or None

    def _shared_headers(self):
        return {
            "User-Agent": f"{__package__}/v{__version__}",
        }

    def _send_list(self, req: KubeGetResources):
        return self.api_client.async_get(
            kind=req.kind,
            namespace=req.namespace,
            label_selector=self._splat_selectors(req.label_selector),
            field_selector=self._splat_selectors(req.field_selector),
        )
