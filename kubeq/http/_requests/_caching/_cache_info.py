from dataclasses import dataclass
from typing import Literal, Unpack, overload

from kubeq.http._requests._caching._cache_features import CacheFeatures


class CacheEntry:
    key: str
    features: CacheFeatures

    def __init__(self, key: str, /, **features: Unpack[CacheFeatures]):
        self.key = key
        self.features = features
