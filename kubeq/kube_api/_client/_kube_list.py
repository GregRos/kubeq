from kubeq.kube_api._client._kube_client_base import KubeClientBase
from kubeq.kube_api._requests._list_request import KubeListRequest


class KubeList(KubeClientBase):
    def list(self, list_r: KubeListRequest):
        return self.send_parse(
            method="GET",
            url=f"/",
            accept=list_r.accept,
            headers=list_r,
            parser=list_r.parser,
        )
