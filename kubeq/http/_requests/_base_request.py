from abc import ABC, abstractmethod
import functools
from hashlib import sha256
import json
from typing import Any, AsyncIterable, Awaitable, Iterable, Mapping, Unpack
from box import Box
from httpx import URL, QueryParams, Response

from kubeq.http._requests._caching._cache_features import CacheFeatures
from kubeq.http._requests._caching._cache_info import CacheEntry

from .._base import Method
from ._helpers import AcceptHeader


class KubeRequest[T](ABC):
    method: Method = "GET"

    def __init__(self, **kwargs: Unpack[CacheFeatures]):
        self.caching = kwargs

    def _url_query(self) -> QueryParams | None:
        return None

    @abstractmethod
    def parse(self, response: Awaitable[Response]) -> T: ...

    @abstractmethod
    def _cache_ttl(self) -> float | None: ...

    @abstractmethod
    def _url_path(self) -> Iterable[str]: ...

    def _header_accept(self) -> AcceptHeader:
        return AcceptHeader("application/json")

    def headers(self) -> dict[str, str]:
        return {
            "Accept": str(self._header_accept()),
        }

    def __cache_key__(self) -> CacheEntry | None:
        if self.method != "GET":
            return None
        everything = Box(
            method=self.method,
            url=self.url,
            headers=self.headers(),
        ).to_dict()
        request_json = json.dumps(everything, sort_keys=True)
        key = f"HTTP_{sha256(request_json.encode()).hexdigest()}"
        return CacheEntry(key, **self.caching)

    def _payload(self) -> Any:
        return None

    @property
    def url(self) -> URL:
        return URL(**{"path": "/".join(self._url_path()), "query": self._url_query()})
