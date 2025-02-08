from abc import ABC, abstractmethod
from typing import Any, Iterable
from httpx import URL, QueryParams

from kubeq.kube_api._requests._utils import AcceptHeader, get_user_agent, Method


class KubeRequestBase(ABC):
    http_method: Method = "GET"

    def url_query(self) -> QueryParams | None:
        return None

    @abstractmethod
    def url_path(self) -> Iterable[str]: ...

    def header_accept(self) -> AcceptHeader:
        return AcceptHeader("application/json")

    def payload(self) -> Any:
        return None

    def header_user_agent(self) -> str:
        return get_user_agent()

    @property
    def url(self) -> URL:
        return URL(**{"path": self.url_path(), "query": self.url_query()})
