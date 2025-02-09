from datetime import datetime
from typing import Iterable, Unpack
from kubeq.storage._features import CacheFeatures
from kubeq.utils._custom_dunder import dunder_invoker
from ._getters import _get_cache


class CacheInfo:
    object: "object"
    key: str
    features: CacheFeatures

    def __init__(
        self,
        key: str,
        value: "object",
        /,
        **features: Unpack[CacheFeatures],
    ):
        global last_index
        self.key = key
        self.object = value
        self.features = features

    @staticmethod
    def from_(o: "object"):
        instance_value = _get_cache(o)
        match instance_value:
            case None:
                return None
            case str():
                return CacheInfo(instance_value, o)
            case CacheInfo():
                return instance_value
            case _:
                raise ValueError(f"Unexpected value {instance_value}")

    @property
    def _short_key_str(self):
        return f"{self.object.__class__.__name__}[{self.key[:3]}⋯]"

    def __str__(self):
        return self._short_key_str
