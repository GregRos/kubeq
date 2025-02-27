from dataclasses import dataclass
from typing import Any, Awaitable

from httpx import Response
from kr8s import Api

from kubeq.http._client._kr8s.wrapper import PatchedApiWrapper
from kubeq.logging import sources
from kubeq.storage import Storage
from ._user_agent import get_user_agent
from kubeq.http._requests import KubeRequest

logger = sources.api_client.logger


class KubeClient:
    def __init__(self, api: Api, cache=Storage.cache):
        self._api = PatchedApiWrapper(api)
        self._cache = cache

    def _header_user_agent(self) -> str:
        return get_user_agent()

    async def _do_send(self, request: KubeRequest) -> Response:

        response: Response | None = await self._cache.get(request)

        if not response:
            url = request.url
            headers = request.headers()
            headers.update({"User-Agent": self._header_user_agent()})
            log_url = f"/{url.path}"

            response = await self._api.send(
                method=request.method,
                url=str(url),
                headers=headers,
                payload=request._payload(),
            )
            logger.info(
                f"Received response to {str(request)}",
                {
                    "endpoint": f"{request.method} {log_url}",
                    "accept": str(request.header_accept),
                },
            )
            await self._cache.store(request, response)
        else:
            logger.info(
                f"Cache hit for {str(request)}",
                {
                    "endpoint": f"{request.method} /{request.url}",
                    "accept": str(request.header_accept),
                },
            )
        return response

    def send[V](self, request: KubeRequest[V]) -> V:

        headers = request.headers()
        headers.update({"User-Agent": self._header_user_agent()})
        response = self._do_send(request)

        return request.parse(response)
