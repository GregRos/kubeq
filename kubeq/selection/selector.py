from itertools import groupby
from typing import Iterable, ReadOnly
import kubeq.operators as oprs
from kubeq import attr

from kr8s.objects import APIObject


from dataclasses import dataclass


@dataclass
class Selector:
    attr: attr.Any
    operator: oprs.Op

    def __call__(self, object: APIObject) -> bool:
        return self.operator(self.attr.get(object))

    def with_op(self, operator: oprs.Op) -> "Selector":
        return Selector(self.attr, operator)
