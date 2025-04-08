from abc import ABC, abstractmethod
import functools
from hashlib import sha256
import json
from typing import Any, AsyncIterable, Awaitable, Iterable, Mapping, Unpack
from box import Box
from httpx import URL, QueryParams, Response

from kubeq.http._requests._helpers._accept_header import (
    BasicSubclause,
    ComplexSubclause,
)
from kubeq.storage._info import CacheInfo
from kubeq.storage._features import CacheFeatures


from .._base import Method
from ._helpers import AcceptHeader


class KubeRequest[T](ABC):
    method: Method = "GET"

    def __init__(self, **cache_features: Unpack[CacheFeatures]):
        self._features = cache_features

    def _url_query(self) -> QueryParams | None:
        return None

    @abstractmethod
    def parse(self, response: Awaitable[Response]) -> T: ...

    @abstractmethod
    def _url_path(self) -> Iterable[str]: ...

    @property
    def header_accept(self) -> AcceptHeader:
        return AcceptHeader(
            BasicSubclause("application/json"),
        )

    def headers(self) -> dict[str, str]:
        return {
            "Accept": str(self.header_accept),
        }

    def __acache__(self) -> CacheInfo | None:
        if self.method != "GET":
            return None
        everything = Box(
            method=self.method,
            url=str(self.url),
            headers=self.headers(),
        ).to_dict()
        request_json = json.dumps(everything, sort_keys=True)
        key = sha256(request_json.encode()).hexdigest()
        return CacheInfo(key, self, **self._features)

    def _payload(self) -> Any:
        return None

    def _args(self):
        return ()

    def __str__(self) -> str:
        return self.__acache__().__str__()

    @property
    def url(self) -> URL:
        u = URL()
        u = u.copy_with(path="/".join(self._url_path()))
        q = self._url_query()
        if q:
            u = u.copy_with(query=str(q).encode("utf8"))
        return u
