from typing import Any
from kr8s import Api

from kubeq.http._client._kr8s._patched import patch_kr8s_for_sending_arbitrary_urls

import aioreactive as rx
from ..._base import Method


class PatchedApiWrapper:
    _api: Api

    def __init__(self, api: Api):
        self._api = patch_kr8s_for_sending_arbitrary_urls(api)

    def send(
        self,
        method: Method,
        url: str,
        headers: dict[str, str],
        payload: Any | None = None,
    ):

        async def _send():
            async with self._api.call_api(
                base="",
                method=method,
                raise_for_status=True,
                namespace=None,
                url=url,
                headers=headers,
                data=payload,
            ) as x:
                yield x

        return _send()
