from itertools import groupby
from typing import Iterable, ReadOnly

from kubeq.query import _attr
from kubeq.query import _operators as oprs

from kr8s.objects import APIObject


from dataclasses import dataclass


@dataclass
class Selector:
    attr: _attr.Any
    operator: oprs.Op

    def __call__(self, object: object) -> bool:
        return self.operator(self.attr.get(object))

    def with_op(self, operator: oprs.Op) -> "Selector":
        return Selector(self.attr, operator)
