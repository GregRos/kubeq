from itertools import groupby
from typing import Iterable, ReadOnly

from kubeq.entities._resource._resource import KubeResource
from kubeq.query import _attr
from kubeq.query import _operators as oprs


from dataclasses import dataclass

from kubeq.query._operators._value_ops.op_in import In
from kubeq.selection._selector import Selector


type KindSelector = Selector[_attr.Kind]
