from itertools import groupby
from typing import Iterable, ReadOnly

from kubeq.entities._resource._resource import KubeResource
from kubeq.query import _attr
from kubeq.query import _operators as oprs


from dataclasses import dataclass


@dataclass
class KindSelector:
    attr: _attr.Kind
    operator: oprs.Op

    def __call__(self, object: KubeResource) -> bool:
        return self.operator(self.attr.get(object))

    def __repr__(self) -> str:
        return f"[{self.operator}]"
