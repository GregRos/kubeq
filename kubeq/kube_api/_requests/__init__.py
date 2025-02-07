from ._api_resources_request import KubeGetApiResources
from ._list_request import KubeListRequest

type KubeRequest = KubeGetApiResources | KubeListRequest
