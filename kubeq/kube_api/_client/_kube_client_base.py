from dataclasses import dataclass
from http import HTTPMethod
import os
import platform
from typing import Literal, Mapping
from kr8s import Api
from kubeq.kube_api._client._headers._user_agent import get_user_agent
from kubeq.version import __version__

type Method = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]


@dataclass(frozen=True, eq=False, repr=False, match_args=False, kw_only=True)
class KubeClientBase:
    api: Api
    user_agent = get_user_agent()
    x_cache_control = True

    def _get_headers(self, **more: str):
        return {
            "User-Agent": self.user_agent,
            "X-Cache-Control": "1" if self.x_cache_control else "0",
            **more,
        }

    def send(
        self, *, method: Method, url: str, headers: dict, payload: str | None = None
    ):
        return self.api.call_api(
            base=url,
            method=method,
            raise_for_status=True,
            url="",
            headers=self._get_headers(**headers),
            payload=payload,
        )
