from itertools import groupby
from typing import Iterable, ReadOnly

from kubeq.entities._resource._resource import KubeResource
from kubeq.query import _attr
from kubeq.query import _operators as oprs


from dataclasses import dataclass

from kubeq.query._selection._instance_selector import InstanceSelector


@dataclass
class KindSelector:
    attr: _attr.Kind
    operator: oprs.Op

    def __call__(self, object: KubeResource) -> bool:
        return self.operator(self.attr.get(object))
