from kubeq.kube_api._client._kube_client_base import KubeClientBase
from kubeq.kube_api._requests._api_resources_request import KubeGetApiResources


class KubeClient(KubeGetApiResources, KubeClientBase):
    pass
