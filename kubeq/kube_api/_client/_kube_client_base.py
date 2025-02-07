from dataclasses import dataclass
from http import HTTPMethod
import os
import platform
from typing import (
    AsyncGenerator,
    Callable,
    Literal,
    Mapping,
    NotRequired,
    Optional,
    TypedDict,
    Unpack,
)
from box import Box
import httpx
from kr8s import Api
import aioreactive as rx
from kubeq.kube_api._client._http._accept_header import AcceptHeader
from ._http import get_user_agent, Method
from kubeq.version import __version__


class KubeRequest(TypedDict):
    method: Method
    url: str
    accept: AcceptHeader
    headers: NotRequired[Mapping[str, str]]
    payload: NotRequired[str]


@dataclass(frozen=True, eq=False, repr=False, match_args=False, kw_only=True)
class KubeClientBase:
    api: Api
    user_agent = get_user_agent()
    x_cache_control = True

    def _get_headers_dict(
        self, more: Mapping[str, str] | None = None
    ) -> Mapping[str, str]:
        more = more or {}
        return {
            "User-Agent": self.user_agent,
            "X-Cache-Control": "1" if self.x_cache_control else "0",
            **more,
        }

    def _get_headers(self, **more: str):
        return self._get_headers_dict(more)

    def send(self, **kwargs: Unpack[KubeRequest]):

        async def _send():
            async with self.api.call_api(
                base="",
                method=kwargs.get("method"),
                raise_for_status=True,
                namespace=None,
                url="",
                headers=self._get_headers_dict(kwargs.get("headers", None)),
                data=kwargs.get("payload", None),
            ) as x:
                yield x

        return rx.from_async_iterable(_send())

    def send_parse[
        T
    ](
        self, parser: Callable[[Box], T], **kwargs: Unpack[KubeRequest]
    ) -> rx.AsyncObservable[T]:
        return rx.pipe(
            self.send(**kwargs),
            rx.map(lambda x: x.json()),
            rx.map(lambda x: Box(x)),
            rx.map(parser),
        )
