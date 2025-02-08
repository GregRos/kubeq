from abc import abstractmethod
from typing import AsyncIterable, Awaitable
from box import Box
from httpx import Response
from kubeq.http._requests._base_request import KubeRequest
import aioreactive as rx


class KubeRxRequest[V](KubeRequest[rx.AsyncObservable[V]]):

    @abstractmethod
    def _parse_json_object(self, body: Box) -> rx.AsyncObservable[V]: ...

    def parse(self, response: Awaitable[Response]) -> rx.AsyncObservable[V]:
        return rx.pipe(
            rx.from_async(response),
            rx.map(lambda r: r.json()),
            rx.map(Box),
            rx.flat_map(self._parse_json_object),
        )
