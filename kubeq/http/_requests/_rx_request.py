from abc import abstractmethod
from box import Box
from httpx import Response
from kubeq.http._requests._base_request import KubeRequestBase
import aioreactive as rx


class KubeRxRequest[V](KubeRequestBase[rx.AsyncObservable[V]]):

    @abstractmethod
    def _parse_json_object(self, body: Box) -> rx.AsyncObservable[V]: ...

    def parse(self, response: Response) -> rx.AsyncObservable[V]:
        return rx.pipe(
            rx.from_async(response.json()),
            rx.map(Box),
            rx.flat_map(self._parse_json_object),
        )
