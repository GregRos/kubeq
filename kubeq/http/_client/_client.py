from dataclasses import dataclass

from kr8s import Api

from kubeq.http._client._kr8s.wrapper import PatchedApiWrapper
from ._user_agent import get_user_agent
from kubeq.http._requests import KubeRequest


class KubeClient:
    def __init__(self, api: Api):
        self._api = PatchedApiWrapper(api)

    def _header_user_agent(self) -> str:
        return get_user_agent()

    def send[V](self, request: KubeRequest[V]) -> V:
        url = request.url
        headers = request.headers()
        headers.update({"User-Agent": self._header_user_agent()})
        x = self._api.send(
            method=request.http_method,
            url=str(url),
            headers=headers,
            payload=request._payload(),
        )

        return request.parse(x)
