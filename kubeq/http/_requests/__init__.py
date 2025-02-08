from ._api_resources_request import KubeDiscoveryRequest
from ._list_request import KubeListRequest

type KubeRequest = KubeDiscoveryRequest | KubeListRequest
