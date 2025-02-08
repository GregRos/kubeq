from abc import ABC, abstractmethod
from typing import Any, Iterable
from httpx import URL, QueryParams, Response
from .._utils import AcceptHeader, Method, get_user_agent


class KubeRequestBase[T](ABC):
    http_method: Method = "GET"

    def _url_query(self) -> QueryParams | None:
        return None

    @abstractmethod
    def parse(self, response: Response) -> T: ...

    @abstractmethod
    def _url_path(self) -> Iterable[str]: ...

    def _header_accept(self) -> AcceptHeader:
        return AcceptHeader("application/json")

    def headers(self) -> dict[str, str]:
        return {
            "User-Agent": self._header_user_agent(),
            "Accept": str(self._header_accept()),
        }

    def _payload(self) -> Any:
        return None

    def _header_user_agent(self) -> str:
        return get_user_agent()

    @property
    def url(self) -> URL:
        return URL(**{"path": self._url_path(), "query": self._url_query()})
