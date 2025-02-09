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
        cache_info = request.__cache__()
        response: Response | None = None
        logger.debug(f"Received request: {request}")
        if cache_info:
            key = cache_info.key
            cached: Response = await self._cache.get(key, default=None)  # type: ignore
            if cached:
                response = cached
        if not response:
            url = request.url
            headers = request.headers()
            headers.update({"User-Agent": self._header_user_agent()})
            response = await self._api.send(
                method=request.method,
                url=str(url),
                headers=headers,
                payload=request._payload(),
            )
            if cache_info and not cache_info.features.get("cache_skip", None):
                await self._cache.set(
                    cache_info.key, response, ttl=cache_info.features["cache_ttl"]
                )

        return response

    def send[V](self, request: KubeRequest[V]) -> V:

        headers = request.headers()
        headers.update({"User-Agent": self._header_user_agent()})
        response = self._do_send(request)

        return request.parse(response)
