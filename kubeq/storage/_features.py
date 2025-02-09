from dataclasses import dataclass
from typing import NotRequired, TypedDict


class CacheFeatures(TypedDict):
    cache_ttl: NotRequired[float]
    cache_force: NotRequired[bool]
    cache_skip: NotRequired[bool]
