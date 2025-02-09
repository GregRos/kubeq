from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Unpack, overload

from kubeq.storage._info import CacheInfo
from kubeq.storage._features import CacheFeatures
from humanize import naturaldelta


class CacheEntry:
    when: datetime
    info: CacheInfo

    def __init__(
        self,
        base: CacheInfo,
        value: "object",
        /,
        **features: Unpack[CacheFeatures],
    ):
        global last_index
        self.info = base
        self.info.features = {
            **self.info.features,
            **features,
        }
        self.value = value
        self.when = datetime.now()

    @property
    def key(self):
        return self.info.key

    @property
    def object(self):
        return self.info.object

    @property
    def features(self):
        return self.info.features

    @staticmethod
    def from_(key: "object", value: "object", /, **features: Unpack[CacheFeatures]):
        base = CacheInfo.from_(key)
        if not base:
            return
        return CacheEntry(base, value, **features)

    @property
    def age(self):
        return datetime.now() - self.when

    @property
    def _short_val_str(self):
        return str(self.value)

    def __str__(self):
        return f"{self.info._short_key_str}' ⇒ '{self._short_val_str}({naturaldelta(self.age)})"
